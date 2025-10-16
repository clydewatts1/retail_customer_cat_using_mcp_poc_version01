"""
Fuzzy clustering implementation for customer segmentation.
Uses Fuzzy C-Means (FCM) algorithm for soft clustering.
"""
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import skfuzzy as fuzz
from typing import Tuple, Optional


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
