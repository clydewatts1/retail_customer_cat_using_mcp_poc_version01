"""
Neural network-based clustering for customer segmentation.
Uses an autoencoder with clustering layer for deep clustering.
"""
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from typing import Tuple, Optional


class NeuralCustomerSegmentation:
    """Deep clustering using autoencoder for customer segmentation."""
    
    def __init__(self, n_clusters: int = 4, encoding_dim: int = 10,
                 epochs: int = 100, batch_size: int = 32, seed: Optional[int] = 42):
        """
        Initialize neural network clustering model.
        
        Args:
            n_clusters: Number of clusters to create
            encoding_dim: Dimension of encoded representation
            epochs: Number of training epochs
            batch_size: Batch size for training
            seed: Random seed for reproducibility
        """
        self.n_clusters = n_clusters
        self.encoding_dim = encoding_dim
        self.epochs = epochs
        self.batch_size = batch_size
        self.seed = seed
        self.scaler = StandardScaler()
        self.autoencoder = None
        self.encoder = None
        self.kmeans = None
        self.feature_cols = None
        
        # Set random seeds
        np.random.seed(seed)
        tf.random.set_seed(seed)
    
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
        """
        Build autoencoder model for feature learning.
        
        Args:
            input_dim: Number of input features
        """
        # Encoder
        encoder_input = layers.Input(shape=(input_dim,))
        encoded = layers.Dense(64, activation='relu')(encoder_input)
        encoded = layers.BatchNormalization()(encoded)
        encoded = layers.Dense(32, activation='relu')(encoded)
        encoded = layers.BatchNormalization()(encoded)
        encoded = layers.Dense(self.encoding_dim, activation='relu', name='encoding')(encoded)
        
        # Decoder
        decoded = layers.Dense(32, activation='relu')(encoded)
        decoded = layers.BatchNormalization()(decoded)
        decoded = layers.Dense(64, activation='relu')(decoded)
        decoded = layers.BatchNormalization()(decoded)
        decoded = layers.Dense(input_dim, activation='linear')(decoded)
        
        # Autoencoder model
        self.autoencoder = keras.Model(encoder_input, decoded)
        self.autoencoder.compile(optimizer='adam', loss='mse')
        
        # Encoder model for extracting features
        self.encoder = keras.Model(encoder_input, encoded)
    
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
        
        # Train autoencoder
        self.autoencoder.fit(
            X_normalized, X_normalized,
            epochs=self.epochs,
            batch_size=self.batch_size,
            shuffle=True,
            verbose=verbose,
            validation_split=0.1
        )
        
        # Extract encoded features
        encoded_features = self.encoder.predict(X_normalized, verbose=0)
        
        # Perform K-means clustering on encoded features
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
        if self.encoder is None or self.kmeans is None:
            raise ValueError("Model must be fitted before prediction")
        
        X_normalized, _ = self.prepare_features(data)
        
        # Encode features
        encoded_features = self.encoder.predict(X_normalized, verbose=0)
        
        # Predict clusters
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
        X_reconstructed = self.autoencoder.predict(X_normalized, verbose=0)
        reconstruction_error = np.mean(np.square(X_normalized - X_reconstructed))
        
        return {
            'silhouette_score': sil_score,
            'reconstruction_error': reconstruction_error,
            'n_clusters': self.n_clusters
        }
