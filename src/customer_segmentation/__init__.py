"""
Customer Segmentation POC Package
Provides fuzzy clustering, neural network-based clustering, and GMM clustering for retail customer segmentation.
"""

from .data_generator import RetailDataGenerator
from .fuzzy_clustering import FuzzyCustomerSegmentation
from .neural_clustering import NeuralCustomerSegmentation
from .gmm_clustering import GMMCustomerSegmentation
from .cluster_enrichment import ClusterEnrichment
from .config_loader import Config, get_config, reload_config

__version__ = '0.1.0'
__all__ = [
    'RetailDataGenerator',
    'FuzzyCustomerSegmentation',
    'NeuralCustomerSegmentation',
    'GMMCustomerSegmentation',
    'ClusterEnrichment',
    'Config',
    'get_config',
    'reload_config'
]
