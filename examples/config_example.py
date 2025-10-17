"""
Example demonstrating how to use the config module to load and access configuration.
This script shows various ways to access configuration values.
"""
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from customer_segmentation import get_config, Config


def main():
    """Demonstrate config usage."""
    
    print("=" * 80)
    print("Configuration Module Usage Example")
    print("=" * 80)
    print()
    
    # Load configuration
    config_path = Path(__file__).parent.parent / "config" / "config.yml"
    config = get_config(str(config_path))
    
    print(f"Configuration loaded from: {config_path}")
    print()
    
    # Access path settings
    print("1. Accessing Paths:")
    print("-" * 40)
    print(f"   Data directory: {config.paths['data_dir']}")
    print(f"   Visualizations directory: {config.paths['visualizations_dir']}")
    print(f"   Models directory: {config.paths.get('models_dir', 'N/A')}")
    print()
    
    # Access data generation parameters
    print("2. Data Generation Parameters:")
    print("-" * 40)
    print(f"   Number of customers: {config.data_generation.get('n_customers', 10000)}")
    print(f"   Random seed: {config.data_generation['random_seed']}")
    print(f"   Use personas: {config.data_generation.get('use_personas', True)}")
    print(f"   Generate dual datasets: {config.data_generation.get('generate_dual_datasets', True)}")
    print(f"   Child ages: {config.data_generation.get('child_ages', [])}")
    print(f"   Adult sizes: {config.data_generation.get('adult_sizes', [])}")
    print()
    
    # Access core columns
    print("3. Core Feature Columns:")
    print("-" * 40)
    core_cols = config.columns['core_features']
    for col_name, col_config in list(core_cols.items())[:5]:  # Show first 5
        print(f"   - {col_name}")
        print(f"     Type: {col_config['type']}")
        print(f"     Description: {col_config['description']}")
    print(f"   ... and {len(core_cols) - 5} more columns")
    print()
    
    # Access department definitions
    print("4. Department Definitions:")
    print("-" * 40)
    dept_features = config.columns.get('department_features', {})
    departments = dept_features.get('departments', [])
    print(f"   Total departments: {len(departments)}")
    print(f"   First 5 departments: {departments[:5]}")
    print()
    
    # Access clustering parameters
    print("5. Fuzzy Clustering Parameters:")
    print("-" * 40)
    fuzzy_params = config.fuzzy_clustering
    print(f"   Number of clusters: {fuzzy_params.get('n_clusters', 13)}")
    print(f"   Fuzziness parameter: {fuzzy_params.get('fuzziness_parameter', 2.0)}")
    print(f"   Max iterations: {fuzzy_params.get('max_iterations', 150)}")
    print(f"   Tolerance: {fuzzy_params.get('tolerance', 1e-5)}")
    print(f"   Random seed: {fuzzy_params.get('random_seed', 42)}")
    print(f"   Use enriched features: {fuzzy_params.get('use_enriched_features', True)}")
    print()
    
    print("6. Neural Clustering Parameters:")
    print("-" * 40)
    neural_params = config.neural_clustering
    print(f"   Number of clusters: {neural_params.get('n_clusters', 13)}")
    print(f"   Encoding dimension: {neural_params.get('encoding_dim', 10)}")
    print(f"   Epochs: {neural_params.get('epochs', 50)}")
    print(f"   Batch size: {neural_params.get('batch_size', 32)}")
    print(f"   Learning rate: {neural_params.get('learning_rate', 0.001)}")
    print(f"   Use enriched features: {neural_params.get('use_enriched_features', True)}")
    print()
    
    # Access visualization settings
    print("7. Visualization Settings:")
    print("-" * 40)
    viz_config = config.visualization
    print(f"   DPI: {viz_config.get('dpi', 150)}")
    print(f"   Format: {viz_config.get('figure_format', 'png')}")
    print(f"   Color palette: {viz_config.get('color_palette', 'Set2')}")
    print(f"   Style: {viz_config.get('style', 'seaborn-v0_8')}")
    print()
    
    # Demonstrate direct property access
    print("8. Direct Property Access:")
    print("-" * 40)
    print(f"   config.paths -> {type(config.paths)}")
    print(f"   config.data_generation -> {type(config.data_generation)}")
    print(f"   config.fuzzy_clustering -> {type(config.fuzzy_clustering)}")
    print(f"   config.neural_clustering -> {type(config.neural_clustering)}")
    print(f"   config.columns -> {type(config.columns)}")
    print(f"   config.visualization -> {type(config.visualization)}")
    print()
    
    # Show how to use config values in practice
    print("9. Practical Usage Example:")
    print("-" * 40)
    print("   Building file paths:")
    data_dir = Path(__file__).parent.parent / config.paths['data_dir']
    output_file = data_dir / "example_output.csv"
    print(f"   Output path: {output_file}")
    print()
    print("   Instantiating models with config parameters:")
    print(f"   RetailDataGenerator(seed={config.data_generation['random_seed']})")
    print(f"   FuzzyCustomerSegmentation(n_clusters={fuzzy_params.get('n_clusters', 13)}, m={fuzzy_params.get('fuzziness_parameter', 2.0)})")
    print(f"   NeuralCustomerSegmentation(n_clusters={neural_params.get('n_clusters', 13)}, encoding_dim={neural_params.get('encoding_dim', 10)})")
    print()
    
    # Show all available attributes
    print("10. All Available Configuration Sections:")
    print("-" * 40)
    print(f"   Available attributes: {[attr for attr in dir(config) if not attr.startswith('_')]}")
    print()
    
    print("=" * 80)
    print("Configuration loaded successfully!")
    print("=" * 80)
    print()
    print("Key Benefits of Using Config:")
    print("  ✓ Centralized parameter management")
    print("  ✓ Easy to modify without changing code")
    print("  ✓ Version control friendly")
    print("  ✓ Clear documentation of all parameters")
    print("  ✓ Consistent settings across all scripts")
    print()


if __name__ == '__main__':
    main()
