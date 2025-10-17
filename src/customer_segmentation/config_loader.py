"""
Configuration loader and utility functions for the retail customer segmentation POC.
"""
import yaml
import os
from pathlib import Path
from typing import Dict, Any, List, Optional


class Config:
    """Configuration manager for the segmentation project."""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration from YAML file.
        
        Args:
            config_path: Path to config.yml file. If None, uses default location.
        """
        if config_path is None:
            # Default to config/config.yml relative to project root
            # __file__ is in src/customer_segmentation/config_loader.py
            # So parent.parent.parent gets us to project root
            project_root = Path(__file__).parent.parent.parent
            config_path = project_root / "config" / "config.yml"
        
        self.config_path = Path(config_path)
        self._config = self._load_config()
        self._project_root = self.config_path.parent.parent
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        
        with open(self.config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        return config
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by key (supports dot notation).
        
        Args:
            key: Configuration key (e.g., 'paths.data_dir')
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def get_path(self, key: str, create_if_missing: bool = False) -> Path:
        """
        Get path from configuration and resolve relative to project root.
        
        Args:
            key: Configuration key for path
            create_if_missing: Create directory if it doesn't exist
            
        Returns:
            Absolute path
        """
        path_str = self.get(key)
        if path_str is None:
            raise ValueError(f"Path not found in config: {key}")
        
        path = self._project_root / path_str
        
        if create_if_missing and not path.exists():
            path.mkdir(parents=True, exist_ok=True)
        
        return path
    
    @property
    def project_info(self) -> Dict[str, str]:
        """Get project information."""
        return self._config.get('project', {})
    
    @property
    def paths(self) -> Dict[str, str]:
        """Get all paths configuration."""
        return self._config.get('paths', {})
    
    @property
    def data_generation(self) -> Dict[str, Any]:
        """Get data generation configuration."""
        return self._config.get('data_generation', {})
    
    @property
    def columns(self) -> Dict[str, Any]:
        """Get columns configuration."""
        return self._config.get('columns', {})
    
    @property
    def clustering(self) -> Dict[str, Any]:
        """Get clustering configuration."""
        return self._config.get('clustering', {})
    
    @property
    def visualization(self) -> Dict[str, Any]:
        """Get visualization configuration."""
        return self._config.get('visualization', {})
    
    @property
    def fuzzy_clustering(self) -> Dict[str, Any]:
        """Get fuzzy clustering configuration."""
        return self._config.get('fuzzy_clustering', {})
    
    @property
    def neural_clustering(self) -> Dict[str, Any]:
        """Get neural clustering configuration."""
        return self._config.get('neural_clustering', {})
    
    @property
    def data_dir(self) -> Path:
        """Get data directory path."""
        return self.get_path('paths.data_dir', create_if_missing=True)
    
    @property
    def output_dir(self) -> Path:
        """Get output directory path."""
        return self.get_path('paths.output_dir', create_if_missing=True)
    
    @property
    def visualizations_dir(self) -> Path:
        """Get visualizations directory path."""
        return self.get_path('paths.visualizations_dir', create_if_missing=True)
    
    @property
    def models_dir(self) -> Path:
        """Get models directory path."""
        return self.get_path('paths.models_dir', create_if_missing=True)
    
    def get_source_data_path(self, key: str) -> Path:
        """Get path to source data file."""
        return self.get_path(f'paths.source_data.{key}')
    
    def get_output_file_path(self, key: str) -> Path:
        """Get path to output file."""
        return self.get_path(f'paths.output_files.{key}')
    
    def get_visualization_path(self, key: str) -> Path:
        """Get path to visualization file."""
        return self.get_path(f'paths.visualization_files.{key}')
    
    @property
    def departments(self) -> List[str]:
        """Get list of departments."""
        dept_config = self.get('data_generation.departments', {})
        if isinstance(dept_config, dict):
            # New hierarchical format
            return list(dept_config.keys())
        else:
            # Legacy list format
            return dept_config
    
    @property
    def classes(self) -> List[str]:
        """Get list of product classes."""
        dept_config = self.get('data_generation.departments', {})
        if isinstance(dept_config, dict):
            # New hierarchical format - extract all classes from all departments
            all_classes = []
            for dept, dept_data in dept_config.items():
                if isinstance(dept_data, dict) and 'classes' in dept_data:
                    all_classes.extend(dept_data['classes'])
            return all_classes
        else:
            # Legacy list format
            return self.get('data_generation.classes', [])
    
    def get_classes_for_department(self, department: str) -> List[str]:
        """Get list of classes that belong to a specific department."""
        dept_config = self.get('data_generation.departments', {})
        if isinstance(dept_config, dict) and department in dept_config:
            dept_data = dept_config[department]
            if isinstance(dept_data, dict) and 'classes' in dept_data:
                return dept_data['classes']
        return []
    
    @property
    def child_ages(self) -> List[str]:
        """Get list of child age groups."""
        return self.get('data_generation.child_ages', [])
    
    @property
    def adult_sizes(self) -> List[str]:
        """Get list of adult sizes."""
        return self.get('data_generation.adult_sizes', [])
    
    @property
    def core_feature_columns(self) -> List[str]:
        """Get list of core feature column names."""
        core_features = self.get('columns.core_features', {})
        return list(core_features.keys())
    
    def get_department_value_columns(self) -> List[str]:
        """Get list of department value column names."""
        pattern = self.get('columns.department_features.pattern', 'dept_total_value_{department_name}')
        departments = self.departments
        return [pattern.replace('{department_name}', dept.replace(' ', '_').replace('&', 'and'))
                for dept in departments]
    
    def get_department_unit_columns(self) -> List[str]:
        """Get list of department unit column names."""
        pattern = self.get('columns.department_units.pattern', 'dept_total_units_{department_name}')
        departments = self.departments
        return [pattern.replace('{department_name}', dept.replace(' ', '_').replace('&', 'and'))
                for dept in departments]
    
    def get_class_value_columns(self) -> List[str]:
        """Get list of class value column names."""
        pattern = self.get('columns.class_features.pattern', 'class_total_value_{class_name}')
        classes = self.classes
        return [pattern.replace('{class_name}', cls.replace(' ', '_').replace('&', 'and'))
                for cls in classes]
    
    def get_class_unit_columns(self) -> List[str]:
        """Get list of class unit column names."""
        pattern = self.get('columns.class_units.pattern', 'class_total_units_{class_name}')
        classes = self.classes
        return [pattern.replace('{class_name}', cls.replace(' ', '_').replace('&', 'and'))
                for cls in classes]
    
    def get_size_columns(self) -> List[str]:
        """Get list of all size/age column names."""
        child_pattern = self.get('columns.child_age_features.pattern', 'count_{age_group}')
        adult_pattern = self.get('columns.adult_size_features.pattern', 'count_size_{size}')
        
        child_cols = [child_pattern.replace('{age_group}', age) for age in self.child_ages]
        adult_cols = [adult_pattern.replace('{size}', size) for size in self.adult_sizes]
        
        return child_cols + adult_cols
    
    def get_enriched_columns(self) -> List[str]:
        """Get all enriched feature column names."""
        return (self.get_department_value_columns() + 
                self.get_department_unit_columns() +
                self.get_class_value_columns() +
                self.get_class_unit_columns() +
                self.get_size_columns())
    
    def get_clustering_features(self, method: str = 'fuzzy') -> List[str]:
        """
        Get list of features to use for clustering.
        
        Args:
            method: 'fuzzy' or 'neural'
            
        Returns:
            List of feature column names
        """
        key = f'{method}_clustering.features_to_use'
        return self.get(key, self.core_feature_columns)
    
    @property
    def fuzzy_params(self) -> Dict[str, Any]:
        """Get fuzzy clustering parameters."""
        return {
            'n_clusters': self.get('fuzzy_clustering.n_clusters', 4),
            'm': self.get('fuzzy_clustering.fuzziness_parameter', 2.0),
            'max_iter': self.get('fuzzy_clustering.max_iterations', 150),
            'error': self.get('fuzzy_clustering.tolerance', 1e-5),
            'seed': self.get('fuzzy_clustering.random_seed', 42)
        }
    
    @property
    def neural_params(self) -> Dict[str, Any]:
        """Get neural clustering parameters."""
        return {
            'n_clusters': self.get('neural_clustering.n_clusters', 4),
            'encoding_dim': self.get('neural_clustering.encoding_dim', 10),
            'epochs': self.get('neural_clustering.epochs', 50),
            'batch_size': self.get('neural_clustering.batch_size', 32),
            'seed': self.get('neural_clustering.random_seed', 42)
        }
    
    @property
    def visualization_params(self) -> Dict[str, Any]:
        """Get visualization parameters."""
        return self.get('visualization', {})
    
    def __repr__(self) -> str:
        """String representation."""
        return f"Config(config_path='{self.config_path}')"


# Global config instance
_config_instance = None


def get_config(config_path: Optional[str] = None) -> Config:
    """
    Get or create global configuration instance.
    
    Args:
        config_path: Path to config file. If None, uses default.
        
    Returns:
        Config instance
    """
    global _config_instance
    
    if _config_instance is None or config_path is not None:
        _config_instance = Config(config_path)
    
    return _config_instance


def reload_config(config_path: Optional[str] = None) -> Config:
    """
    Force reload of configuration.
    
    Args:
        config_path: Path to config file. If None, uses default.
        
    Returns:
        New Config instance
    """
    global _config_instance
    _config_instance = Config(config_path)
    return _config_instance
