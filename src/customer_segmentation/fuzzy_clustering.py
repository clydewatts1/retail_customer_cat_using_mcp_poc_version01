"""
Fuzzy clustering implementation for customer segmentation.
Uses Fuzzy C-Means (FCM) algorithm for soft clustering.
"""
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import skfuzzy as fuzz
from typing import Tuple, Optional, Dict, Any
import json
import yaml
from pathlib import Path
from datetime import datetime


class FuzzyCustomerSegmentation:
    """Fuzzy C-Means clustering for customer segmentation."""
    
    def __init__(self, n_clusters: int = 4, m: float = 2.0, 
                 max_iter: int = 150, error: float = 0.005, seed: Optional[int] = 42):
        """
        Initialize fuzzy clustering model.
        
        Args:
            n_clusters: Number of clusters to create
            m: Fuzziness parameter (1.0 = hard clustering, >1.0 = fuzzy)
            max_iter: Maximum number of iterations
            error: Convergence threshold
            seed: Random seed for reproducibility
        """
        self.n_clusters = n_clusters
        self.m = m
        self.max_iter = max_iter
        self.error = error
        self.seed = seed
        self.scaler = StandardScaler()
        self.cntr = None  # Cluster centers
        self.u = None  # Membership matrix
        self.feature_cols = None
        
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
        if config is not None and config.get('fuzzy_clustering', {}).get('use_enriched_features', False):
            feature_cols = config['fuzzy_clustering']['features_to_use'] + config['fuzzy_clustering']['enriched_features_to_use']
        else:
            feature_cols = config['fuzzy_clustering']['features_to_use'] if config else [
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
    
    def fit(self, data: pd.DataFrame) -> 'FuzzyCustomerSegmentation':
        """
        Fit fuzzy clustering model to customer data.
        
        Args:
            data: DataFrame with customer features
            
        Returns:
            Self for method chaining
        """
        # Prepare features
        X_normalized, _ = self.prepare_features(data)
        
        # Transpose for skfuzzy format (features x samples)
        X_T = X_normalized.T
        
        # Perform fuzzy c-means clustering
        self.cntr, self.u, _, _, _, _, _ = fuzz.cluster.cmeans(
            X_T,
            c=self.n_clusters,
            m=self.m,
            error=self.error,
            maxiter=self.max_iter,
            seed=self.seed
        )
        
        return self
    
    def predict(self, data: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """
        Predict cluster assignments and membership degrees.
        
        Args:
            data: DataFrame with customer features
            
        Returns:
            Tuple of (hard cluster labels, membership matrix)
        """
        if self.cntr is None or self.u is None:
            raise ValueError("Model must be fitted before prediction")
        
        X_normalized, _ = self.prepare_features(data)
        X_T = X_normalized.T
        
        # Predict membership for new data
        u_pred, _, _, _, _, _ = fuzz.cluster.cmeans_predict(
            X_T, self.cntr, self.m, error=self.error, maxiter=self.max_iter
        )
        
        # Get hard cluster assignments (highest membership)
        cluster_labels = np.argmax(u_pred, axis=0)
        
        return cluster_labels, u_pred
    
    def fit_predict(self, data: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """
        Fit model and predict cluster assignments.
        
        Args:
            data: DataFrame with customer features
            
        Returns:
            Tuple of (hard cluster labels, membership matrix)
        """
        self.fit(data)
        cluster_labels = np.argmax(self.u, axis=0)
        return cluster_labels, self.u
    
    def get_cluster_centers(self) -> pd.DataFrame:
        """
        Get cluster centers in original feature space.
        
        Returns:
            DataFrame with cluster centers
        """
        if self.cntr is None:
            raise ValueError("Model must be fitted first")
        
        # Transform centers back to original space
        centers_original = self.scaler.inverse_transform(self.cntr)
        
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
        cluster_labels = np.argmax(self.u, axis=0)
        
        # Calculate silhouette score
        sil_score = silhouette_score(X_normalized, cluster_labels)
        
        # Calculate partition coefficient (fuzzy clustering metric)
        pc = np.sum(self.u ** 2) / self.u.shape[1]
        
        # Calculate partition entropy (lower is better)
        pe = -np.sum(self.u * np.log(self.u + 1e-10)) / self.u.shape[1]
        
        return {
            'silhouette_score': sil_score,
            'partition_coefficient': pc,
            'partition_entropy': pe,
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
        if self.cntr is None or self.u is None:
            raise ValueError("Model must be fitted first")
        
        # Get cluster labels
        cluster_labels = np.argmax(self.u, axis=0)
        data_with_clusters = data.copy()
        data_with_clusters['cluster'] = cluster_labels
        
        # Get evaluation metrics
        metrics = self.evaluate(data)
        
        # Build cluster profile
        profile = {
            'metadata': {
                'method': 'Fuzzy C-Means (FCM)',
                'timestamp': datetime.now().isoformat(),
                'n_clusters': self.n_clusters,
                'n_samples': len(data),
                'fuzziness_parameter': self.m,
                'max_iterations': self.max_iter,
                'convergence_threshold': self.error
            },
            'metrics': {
                'silhouette_score': float(metrics['silhouette_score']),
                'partition_coefficient': float(metrics['partition_coefficient']),
                'partition_entropy': float(metrics['partition_entropy'])
            },
            'features_used': self.feature_cols,
            'clusters': {}
        }
        
        # Analyze each cluster
        for cluster_id in range(self.n_clusters):
            cluster_mask = cluster_labels == cluster_id
            cluster_data = data_with_clusters[cluster_mask]
            
            # Get membership degrees for this cluster
            cluster_memberships = self.u[cluster_id, cluster_mask]
            
            # Calculate statistics
            cluster_info = {
                'cluster_id': int(cluster_id),
                'size': int(cluster_mask.sum()),
                'percentage': float(cluster_mask.sum() / len(data) * 100),
                'membership_stats': {
                    'mean': float(cluster_memberships.mean()),
                    'std': float(cluster_memberships.std()),
                    'min': float(cluster_memberships.min()),
                    'max': float(cluster_memberships.max())
                },
                'feature_statistics': {},
                'cluster_center': {}
            }
            
            # Add cluster center values
            center_original = self.scaler.inverse_transform(self.cntr[cluster_id:cluster_id+1])[0]
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
        json_filename = f'fuzzy_cluster_profile_{timestamp}.json'
        yaml_filename = f'fuzzy_cluster_profile_{timestamp}.yaml'
        
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
