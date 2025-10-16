"""
Customer Segmentation POC Package
Provides fuzzy clustering and neural network-based clustering for retail customer segmentation.
"""

from .data_generator import RetailDataGenerator
from .fuzzy_clustering import FuzzyCustomerSegmentation
from .neural_clustering import NeuralCustomerSegmentation
from .cluster_enrichment import ClusterEnrichment
from .config_loader import Config, get_config, reload_config

__version__ = '0.1.0'
__all__ = [
    'RetailDataGenerator',
    'FuzzyCustomerSegmentation',
    'NeuralCustomerSegmentation',
    'ClusterEnrichment',
    'Config',
    'get_config',
    'reload_config'
]
