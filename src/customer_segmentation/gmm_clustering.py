"""
Gaussian Mixture Model (GMM) clustering for customer segmentation.
Uses probabilistic clustering with Gaussian distributions for soft clustering.
"""
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
from typing import Tuple, Optional, Dict, Any
import json
import yaml
from pathlib import Path
from datetime import datetime


class GMMCustomerSegmentation:
    """Gaussian Mixture Model clustering for customer segmentation."""
    
    def __init__(self, n_clusters: int = 4, covariance_type: str = 'full',
                 max_iter: int = 200, n_init: int = 10, seed: Optional[int] = 42):
        """
        Initialize GMM clustering model.
        
        Args:
            n_clusters: Number of Gaussian components (clusters)
            covariance_type: Type of covariance parameters ('full', 'tied', 'diag', 'spherical')
            max_iter: Maximum number of EM iterations
            n_init: Number of initializations to perform
            seed: Random seed for reproducibility
        """
        self.n_clusters = n_clusters
        self.covariance_type = covariance_type
        self.max_iter = max_iter
        self.n_init = n_init
        self.seed = seed
        self.scaler = StandardScaler()
        self.gmm = None
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
        if config is not None and config.get('gmm_clustering', {}).get('use_enriched_features', False):
            feature_cols = config['gmm_clustering']['features_to_use'] + config['gmm_clustering']['enriched_features_to_use']
        elif config is not None and config.get('fuzzy_clustering', {}).get('use_enriched_features', False):
            # Fallback to fuzzy clustering config if GMM config not available
            feature_cols = config['fuzzy_clustering']['features_to_use'] + config['fuzzy_clustering']['enriched_features_to_use']
        else:
            # Default RFM features
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
    
    def fit(self, data: pd.DataFrame) -> 'GMMCustomerSegmentation':
        """
        Fit GMM clustering model to customer data.
        
        Args:
            data: DataFrame with customer features
            
        Returns:
            Self for method chaining
        """
        # Prepare features
        X_normalized, _ = self.prepare_features(data)
        
        # Initialize and fit Gaussian Mixture Model
        self.gmm = GaussianMixture(
            n_components=self.n_clusters,
            covariance_type=self.covariance_type,
            max_iter=self.max_iter,
            n_init=self.n_init,
            random_state=self.seed
        )
        
        self.gmm.fit(X_normalized)
        
        return self
    
    def predict(self, data: pd.DataFrame) -> np.ndarray:
        """
        Predict cluster assignments (hard clustering).
        
        Args:
            data: DataFrame with customer features
            
        Returns:
            Array of cluster labels
        """
        if self.gmm is None:
            raise ValueError("Model must be fitted before prediction")
        
        X_normalized, _ = self.prepare_features(data)
        cluster_labels = self.gmm.predict(X_normalized)
        
        return cluster_labels
    
    def predict_proba(self, data: pd.DataFrame) -> np.ndarray:
        """
        Predict cluster membership probabilities (soft clustering).
        
        Args:
            data: DataFrame with customer features
            
        Returns:
            Array of shape (n_samples, n_clusters) with probability distributions
        """
        if self.gmm is None:
            raise ValueError("Model must be fitted before prediction")
        
        X_normalized, _ = self.prepare_features(data)
        probabilities = self.gmm.predict_proba(X_normalized)
        
        return probabilities
    
    def fit_predict(self, data: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """
        Fit model and predict cluster assignments.
        
        Args:
            data: DataFrame with customer features
            
        Returns:
            Tuple of (hard cluster labels, probability matrix)
        """
        self.fit(data)
        cluster_labels = self.predict(data)
        probabilities = self.predict_proba(data)
        
        return cluster_labels, probabilities
    
    def get_cluster_centers(self) -> pd.DataFrame:
        """
        Get cluster centers (means) in original feature space.
        
        Returns:
            DataFrame with cluster centers
        """
        if self.gmm is None:
            raise ValueError("Model must be fitted first")
        
        # Transform centers back to original space
        centers_original = self.scaler.inverse_transform(self.gmm.means_)
        
        return pd.DataFrame(
            centers_original,
            columns=self.feature_cols,
            index=[f"Cluster_{i}" for i in range(self.n_clusters)]
        )
    
    def get_covariances(self) -> np.ndarray:
        """
        Get covariance matrices for each cluster.
        
        Returns:
            Covariance matrices (shape depends on covariance_type)
        """
        if self.gmm is None:
            raise ValueError("Model must be fitted first")
        
        return self.gmm.covariances_
    
    def get_weights(self) -> np.ndarray:
        """
        Get mixture weights (prior probabilities) for each cluster.
        
        Returns:
            Array of mixture weights
        """
        if self.gmm is None:
            raise ValueError("Model must be fitted first")
        
        return self.gmm.weights_
    
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
        
        # Calculate BIC (Bayesian Information Criterion) - lower is better
        bic = self.gmm.bic(X_normalized)
        
        # Calculate AIC (Akaike Information Criterion) - lower is better
        aic = self.gmm.aic(X_normalized)
        
        # Calculate Davies-Bouldin Index - lower is better
        db_score = davies_bouldin_score(X_normalized, cluster_labels)
        
        # Calculate Calinski-Harabasz Score - higher is better
        ch_score = calinski_harabasz_score(X_normalized, cluster_labels)
        
        # Calculate log-likelihood
        log_likelihood = self.gmm.score(X_normalized) * len(X_normalized)
        
        return {
            'silhouette_score': sil_score,
            'bic': bic,
            'aic': aic,
            'davies_bouldin_index': db_score,
            'calinski_harabasz_score': ch_score,
            'log_likelihood': log_likelihood,
            'n_clusters': self.n_clusters,
            'converged': self.gmm.converged_,
            'n_iterations': self.gmm.n_iter_
        }
    
    def get_uncertainty_metrics(self, data: pd.DataFrame) -> dict:
        """
        Calculate metrics related to assignment uncertainty.
        
        Args:
            data: DataFrame with customer features
            
        Returns:
            Dictionary with uncertainty metrics
        """
        probabilities = self.predict_proba(data)
        max_proba = probabilities.max(axis=1)
        
        # Calculate entropy for each sample
        entropy = -np.sum(probabilities * np.log(probabilities + 1e-10), axis=1)
        
        return {
            'avg_max_probability': max_proba.mean(),
            'std_max_probability': max_proba.std(),
            'high_confidence_count': (max_proba > 0.9).sum(),
            'high_confidence_pct': (max_proba > 0.9).sum() / len(max_proba) * 100,
            'low_confidence_count': (max_proba < 0.7).sum(),
            'low_confidence_pct': (max_proba < 0.7).sum() / len(max_proba) * 100,
            'avg_entropy': entropy.mean(),
            'max_entropy': entropy.max()
        }
    
    def generate_cluster_profile(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate comprehensive cluster profile for AI LLM analysis.
        
        Args:
            data: DataFrame with customer features and cluster assignments
            
        Returns:
            Dictionary containing detailed cluster analysis
        """
        if self.gmm is None:
            raise ValueError("Model must be fitted first")
        
        # Get cluster labels and probabilities
        cluster_labels = self.predict(data)
        probabilities = self.predict_proba(data)
        data_with_clusters = data.copy()
        data_with_clusters['cluster'] = cluster_labels
        
        # Get evaluation metrics
        metrics = self.evaluate(data)
        uncertainty = self.get_uncertainty_metrics(data)
        
        # Build cluster profile
        profile = {
            'metadata': {
                'method': 'Gaussian Mixture Model (GMM)',
                'timestamp': datetime.now().isoformat(),
                'n_clusters': self.n_clusters,
                'n_samples': len(data),
                'covariance_type': self.covariance_type,
                'max_iterations': self.max_iter,
                'n_initializations': self.n_init,
                'converged': bool(self.gmm.converged_),
                'n_iterations': int(self.gmm.n_iter_)
            },
            'metrics': {
                'silhouette_score': float(metrics['silhouette_score']),
                'bic': float(metrics['bic']),
                'aic': float(metrics['aic']),
                'davies_bouldin_index': float(metrics['davies_bouldin_index']),
                'calinski_harabasz_score': float(metrics['calinski_harabasz_score']),
                'log_likelihood': float(metrics['log_likelihood'])
            },
            'uncertainty_metrics': {
                'avg_max_probability': float(uncertainty['avg_max_probability']),
                'std_max_probability': float(uncertainty['std_max_probability']),
                'high_confidence_count': int(uncertainty['high_confidence_count']),
                'high_confidence_pct': float(uncertainty['high_confidence_pct']),
                'low_confidence_count': int(uncertainty['low_confidence_count']),
                'low_confidence_pct': float(uncertainty['low_confidence_pct']),
                'avg_entropy': float(uncertainty['avg_entropy']),
                'max_entropy': float(uncertainty['max_entropy'])
            },
            'features_used': self.feature_cols,
            'mixture_weights': [float(w) for w in self.gmm.weights_],
            'clusters': {}
        }
        
        # Analyze each cluster
        for cluster_id in range(self.n_clusters):
            cluster_mask = cluster_labels == cluster_id
            cluster_data = data_with_clusters[cluster_mask]
            
            # Get probabilities for this cluster
            cluster_probs = probabilities[cluster_mask, cluster_id]
            
            # Calculate statistics
            cluster_info = {
                'cluster_id': int(cluster_id),
                'size': int(cluster_mask.sum()),
                'percentage': float(cluster_mask.sum() / len(data) * 100),
                'mixture_weight': float(self.gmm.weights_[cluster_id]),
                'probability_stats': {
                    'mean': float(cluster_probs.mean()),
                    'std': float(cluster_probs.std()),
                    'min': float(cluster_probs.min()),
                    'max': float(cluster_probs.max()),
                    'median': float(np.median(cluster_probs))
                },
                'feature_statistics': {},
                'cluster_center': {},
                'covariance_info': {
                    'type': self.covariance_type
                }
            }
            
            # Add cluster center values (means)
            center_original = self.scaler.inverse_transform(self.gmm.means_[cluster_id:cluster_id+1])[0]
            for feat_idx, feat_name in enumerate(self.feature_cols):
                cluster_info['cluster_center'][feat_name] = float(center_original[feat_idx])
            
            # Add covariance diagonal (variances) for interpretability
            if self.covariance_type == 'full':
                # Extract diagonal of covariance matrix
                cov_diag = np.diag(self.gmm.covariances_[cluster_id])
                cluster_info['covariance_info']['feature_variances'] = {
                    feat_name: float(var) for feat_name, var in zip(self.feature_cols, cov_diag)
                }
            elif self.covariance_type == 'diag':
                cluster_info['covariance_info']['feature_variances'] = {
                    feat_name: float(var) for feat_name, var in zip(self.feature_cols, self.gmm.covariances_[cluster_id])
                }
            elif self.covariance_type == 'spherical':
                cluster_info['covariance_info']['variance'] = float(self.gmm.covariances_[cluster_id])
            
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
        json_filename = f'gmm_cluster_profile_{timestamp}.json'
        yaml_filename = f'gmm_cluster_profile_{timestamp}.yaml'
        
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
