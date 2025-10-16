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
from typing import Tuple, Optional


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
        # Select numerical features for clustering
        feature_cols = [
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
