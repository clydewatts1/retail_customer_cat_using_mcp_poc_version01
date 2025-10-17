"""
Neural network-based clustering for customer segmentation.
Uses an autoencoder with clustering layer for deep clustering.
"""
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from typing import Tuple, Optional, Dict, Any
import json
import yaml
from pathlib import Path
from datetime import datetime


class Autoencoder(nn.Module):
    def __init__(self, input_dim, encoding_dim):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.BatchNorm1d(64),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.BatchNorm1d(32),
            nn.Linear(32, encoding_dim),
            nn.ReLU()
        )
        self.decoder = nn.Sequential(
            nn.Linear(encoding_dim, 32),
            nn.ReLU(),
            nn.BatchNorm1d(32),
            nn.Linear(32, 64),
            nn.ReLU(),
            nn.BatchNorm1d(64),
            nn.Linear(64, input_dim)
        )
    def forward(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded
    def encode(self, x):
        return self.encoder(x)

class NeuralCustomerSegmentation:
    """Deep clustering using autoencoder (PyTorch) for customer segmentation."""
    def __init__(self, n_clusters: int = 4, encoding_dim: int = 10,
                 epochs: int = 100, batch_size: int = 32, seed: Optional[int] = 42, device: Optional[str] = None):
        self.n_clusters = n_clusters
        self.encoding_dim = encoding_dim
        self.epochs = epochs
        self.batch_size = batch_size
        self.seed = seed
        self.scaler = StandardScaler()
        self.autoencoder = None
        self.kmeans = None
        self.feature_cols = None
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        np.random.seed(seed)
        torch.manual_seed(seed)
    
    def prepare_features(self, data: pd.DataFrame) -> Tuple[np.ndarray, list]:
        """
        Prepare and normalize features for clustering.
        
        Args:
            data: DataFrame with customer features
            
        Returns:
            Tuple of (normalized feature array, feature column names)
        """
        # Use config to select hierarchical department/class/size features
        config = getattr(self, 'config', None)
        if config is not None and config.get('neural_clustering', {}).get('use_enriched_features', False):
            feature_cols = config['neural_clustering']['features_to_use'] + config['neural_clustering']['enriched_features_to_use']
        else:
            feature_cols = config['neural_clustering']['features_to_use'] if config else [
                'total_purchases', 'total_revenue', 'avg_order_value',
                'recency_days', 'frequency_per_month', 'customer_lifetime_months',
                'return_rate'
            ]
        # Filter to only existing columns
        feature_cols = [col for col in feature_cols if col in data.columns]
        self.feature_cols = feature_cols
        X = data[feature_cols].values
        X_normalized = self.scaler.fit_transform(X)
        return X_normalized, feature_cols
    
    def build_autoencoder(self, input_dim: int):
        self.autoencoder = Autoencoder(input_dim, self.encoding_dim).to(self.device)
    
    def fit(self, data: pd.DataFrame, verbose: int = 0) -> 'NeuralCustomerSegmentation':
        """
        Fit neural clustering model to customer data.
        
        Args:
            data: DataFrame with customer features
            verbose: Verbosity level for training
            
        Returns:
            Self for method chaining
        """
        # Prepare features
        X_normalized, _ = self.prepare_features(data)
        
        # Build autoencoder
        self.build_autoencoder(X_normalized.shape[1])
        X_tensor = torch.tensor(X_normalized, dtype=torch.float32).to(self.device)
        dataset = TensorDataset(X_tensor)
        loader = DataLoader(dataset, batch_size=self.batch_size, shuffle=True)
        optimizer = optim.Adam(self.autoencoder.parameters(), lr=1e-3)
        criterion = nn.MSELoss()
        self.autoencoder.train()
        for epoch in range(self.epochs):
            epoch_loss = 0.0
            for (batch,) in loader:
                optimizer.zero_grad()
                output = self.autoencoder(batch)
                loss = criterion(output, batch)
                loss.backward()
                optimizer.step()
                epoch_loss += loss.item() * batch.size(0)
            if verbose and (epoch % 10 == 0 or epoch == self.epochs - 1):
                print(f"Epoch {epoch+1}/{self.epochs}, Loss: {epoch_loss / len(dataset):.6f}")
        self.autoencoder.eval()
        with torch.no_grad():
            encoded_features = self.autoencoder.encoder(X_tensor).cpu().numpy()
        self.kmeans = KMeans(n_clusters=self.n_clusters, random_state=self.seed, n_init=10)
        self.kmeans.fit(encoded_features)
        return self
    
    def predict(self, data: pd.DataFrame) -> np.ndarray:
        """
        Predict cluster assignments.
        
        Args:
            data: DataFrame with customer features
            
        Returns:
            Array of cluster labels
        """
        if self.autoencoder is None or self.kmeans is None:
            raise ValueError("Model must be fitted before prediction")
        X_normalized, _ = self.prepare_features(data)
        X_tensor = torch.tensor(X_normalized, dtype=torch.float32).to(self.device)
        self.autoencoder.eval()
        with torch.no_grad():
            encoded_features = self.autoencoder.encoder(X_tensor).cpu().numpy()
        cluster_labels = self.kmeans.predict(encoded_features)
        return cluster_labels
    
    def fit_predict(self, data: pd.DataFrame, verbose: int = 0) -> np.ndarray:
        """
        Fit model and predict cluster assignments.
        
        Args:
            data: DataFrame with customer features
            verbose: Verbosity level for training
            
        Returns:
            Array of cluster labels
        """
        self.fit(data, verbose=verbose)
        return self.predict(data)
    
    def get_cluster_centers(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Get cluster centers in original feature space.
        
        Args:
            data: DataFrame with customer features (used to compute centers)
            
        Returns:
            DataFrame with cluster centers
        """
        if self.kmeans is None:
            raise ValueError("Model must be fitted first")
        
        X_normalized, _ = self.prepare_features(data)
        cluster_labels = self.predict(data)
        
        # Calculate centers in original space
        centers = []
        for i in range(self.n_clusters):
            cluster_mask = cluster_labels == i
            if cluster_mask.sum() > 0:
                center = X_normalized[cluster_mask].mean(axis=0)
                centers.append(center)
            else:
                centers.append(np.zeros(X_normalized.shape[1]))
        
        centers = np.array(centers)
        centers_original = self.scaler.inverse_transform(centers)
        
        return pd.DataFrame(
            centers_original,
            columns=self.feature_cols,
            index=[f"Cluster_{i}" for i in range(self.n_clusters)]
        )
    
    def evaluate(self, data: pd.DataFrame) -> dict:
        """
        Evaluate clustering quality.
        
        Args:
            data: DataFrame with customer features
            
        Returns:
            Dictionary with evaluation metrics
        """
        X_normalized, _ = self.prepare_features(data)
        cluster_labels = self.predict(data)
        
        # Calculate silhouette score
        sil_score = silhouette_score(X_normalized, cluster_labels)
        
        # Calculate reconstruction error
        X_tensor = torch.tensor(X_normalized, dtype=torch.float32).to(self.device)
        self.autoencoder.eval()
        with torch.no_grad():
            X_reconstructed = self.autoencoder(X_tensor).cpu().numpy()
        reconstruction_error = np.mean(np.square(X_normalized - X_reconstructed))
        return {
            'silhouette_score': sil_score,
            'reconstruction_error': reconstruction_error,
            'n_clusters': self.n_clusters
        }
    
    def generate_cluster_profile(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate comprehensive cluster profile for AI LLM analysis.
        
        Args:
            data: DataFrame with customer features and cluster assignments
            
        Returns:
            Dictionary containing detailed cluster analysis
        """
        if self.autoencoder is None or self.kmeans is None:
            raise ValueError("Model must be fitted first")
        
        # Get cluster labels
        cluster_labels = self.predict(data)
        data_with_clusters = data.copy()
        data_with_clusters['cluster'] = cluster_labels
        
        # Get evaluation metrics
        metrics = self.evaluate(data)
        
        # Get encoded features for additional analysis
        X_normalized, _ = self.prepare_features(data)
        X_tensor = torch.tensor(X_normalized, dtype=torch.float32).to(self.device)
        self.autoencoder.eval()
        with torch.no_grad():
            encoded_features = self.autoencoder.encoder(X_tensor).cpu().numpy()
        
        # Build cluster profile
        profile = {
            'metadata': {
                'method': 'Neural Network (Autoencoder + K-Means)',
                'timestamp': datetime.now().isoformat(),
                'n_clusters': self.n_clusters,
                'n_samples': len(data),
                'encoding_dim': self.encoding_dim,
                'epochs': self.epochs,
                'batch_size': self.batch_size
            },
            'metrics': {
                'silhouette_score': float(metrics['silhouette_score']),
                'reconstruction_error': float(metrics['reconstruction_error'])
            },
            'features_used': self.feature_cols,
            'encoding_dimension': self.encoding_dim,
            'clusters': {}
        }
        
        # Analyze each cluster
        for cluster_id in range(self.n_clusters):
            cluster_mask = cluster_labels == cluster_id
            cluster_data = data_with_clusters[cluster_mask]
            cluster_encoded = encoded_features[cluster_mask]
            
            # Calculate statistics
            cluster_info = {
                'cluster_id': int(cluster_id),
                'size': int(cluster_mask.sum()),
                'percentage': float(cluster_mask.sum() / len(data) * 100),
                'encoded_space_stats': {
                    'mean_distance_to_center': float(np.mean(np.linalg.norm(
                        cluster_encoded - self.kmeans.cluster_centers_[cluster_id], axis=1
                    ))),
                    'std_distance_to_center': float(np.std(np.linalg.norm(
                        cluster_encoded - self.kmeans.cluster_centers_[cluster_id], axis=1
                    )))
                },
                'feature_statistics': {},
                'cluster_center': {}
            }
            
            # Add cluster center values in original space
            # Calculate center from actual cluster members
            X_cluster = X_normalized[cluster_mask]
            if len(X_cluster) > 0:
                center_normalized = X_cluster.mean(axis=0)
                center_original = self.scaler.inverse_transform(center_normalized.reshape(1, -1))[0]
                
                for feat_idx, feat_name in enumerate(self.feature_cols):
                    cluster_info['cluster_center'][feat_name] = float(center_original[feat_idx])
            
            # Calculate feature statistics for customers in this cluster
            for feature in self.feature_cols:
                if feature in cluster_data.columns:
                    feat_values = cluster_data[feature].dropna()
                    if len(feat_values) > 0:
                        cluster_info['feature_statistics'][feature] = {
                            'mean': float(feat_values.mean()),
                            'median': float(feat_values.median()),
                            'std': float(feat_values.std()),
                            'min': float(feat_values.min()),
                            'max': float(feat_values.max()),
                            'q25': float(feat_values.quantile(0.25)),
                            'q75': float(feat_values.quantile(0.75))
                        }
            
            profile['clusters'][f'cluster_{cluster_id}'] = cluster_info
        
        return profile
    
    def export_cluster_profile(self, data: pd.DataFrame, output_dir: str = 'data/output') -> Dict[str, str]:
        """
        Export cluster profile to JSON and YAML files.
        
        Args:
            data: DataFrame with customer features
            output_dir: Directory to save output files
            
        Returns:
            Dictionary with paths to saved files
        """
        # Generate profile
        profile = self.generate_cluster_profile(data)
        
        # Create output directory if it doesn't exist
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Generate filenames with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        json_filename = f'neural_cluster_profile_{timestamp}.json'
        yaml_filename = f'neural_cluster_profile_{timestamp}.yaml'
        
        json_path = output_path / json_filename
        yaml_path = output_path / yaml_filename
        
        # Save as JSON
        with open(json_path, 'w') as f:
            json.dump(profile, f, indent=2)
        
        # Save as YAML
        with open(yaml_path, 'w') as f:
            yaml.dump(profile, f, default_flow_style=False, sort_keys=False)
        
        return {
            'json': str(json_path),
            'yaml': str(yaml_path),
            'profile': profile
        }
