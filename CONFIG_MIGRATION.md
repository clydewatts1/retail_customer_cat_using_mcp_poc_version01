# Configuration Module Integration

## Overview
All Python scripts have been updated to use the centralized configuration system via `config/config.yml` and the `config_loader` module.

## Changes Made

### 1. Updated Scripts

#### `examples/generate_customer_data.py`
**Before:**
- Hardcoded values: 500 customers, no seed, relative path "../data/"
- Direct CSV save with hardcoded filename

**After:**
- Loads configuration from `config/config.yml`
- Uses `config.data_generation['num_customers']` for customer count
- Uses `config.data_generation['seed']` for reproducibility
- Uses `config.paths['data_dir']` for output directory
- Displays detailed statistics about enriched features

**Key Changes:**
```python
# Old
generator = RetailDataGenerator()
df = generator.generate_customer_data(500)
df.to_csv("../data/customer_sales_data_enriched.csv", index=False)

# New
config = get_config(str(config_path))
generator = RetailDataGenerator(seed=config.data_generation['seed'])
df = generator.generate_customer_data(config.data_generation['num_customers'])
data_dir = Path(__file__).parent.parent / config.paths['data_dir']
generator.save_data(df, str(data_dir / "customer_sales_data_enriched.csv"))
```

#### `examples/run_segmentation_pipeline.py`
**Before:**
- Hardcoded clustering parameters (n_clusters=4, m=2.0, epochs=50, etc.)
- Hardcoded seed=42
- Fixed output paths
- Manual directory creation

**After:**
- All parameters loaded from config
- Fuzzy clustering uses `config.clustering['fuzzy']` section
- Neural clustering uses `config.clustering['neural']` section
- Dynamic path building from `config.paths`
- Consistent seed across all operations

**Key Changes:**
```python
# Old
fuzzy_model = FuzzyCustomerSegmentation(n_clusters=4, m=2.0, seed=42)
neural_model = NeuralCustomerSegmentation(n_clusters=4, encoding_dim=10, 
                                          epochs=50, batch_size=32, seed=42)

# New
config = get_config(str(config_path))
fuzzy_params = config.clustering['fuzzy']
neural_params = config.clustering['neural']
seed = config.data_generation['seed']

fuzzy_model = FuzzyCustomerSegmentation(
    n_clusters=fuzzy_params['n_clusters'],
    m=fuzzy_params['fuzziness'],
    seed=seed
)
neural_model = NeuralCustomerSegmentation(
    n_clusters=neural_params['n_clusters'],
    encoding_dim=neural_params['encoding_dim'],
    epochs=neural_params['epochs'],
    batch_size=neural_params['batch_size'],
    seed=seed
)
```

#### `examples/visualize_segments.py`
**Before:**
- Hardcoded visualization settings (dpi=150, format=png)
- Fixed output directory "../visualizations/"
- Hardcoded data generation parameters

**After:**
- Uses `config.visualization['dpi']` and `config.visualization['format']`
- Uses `config.paths['visualization_dir']` for output
- All generation/clustering parameters from config
- Dynamic filename generation based on config format

**Key Changes:**
```python
# Old
fig.savefig('../visualizations/cluster_distribution.png', dpi=150, bbox_inches='tight')

# New
config = get_config(str(config_path))
viz_config = config.visualization
viz_dir = Path(__file__).parent.parent / config.paths['visualization_dir']
output_path = viz_dir / f"cluster_distribution.{viz_config['format']}"
fig.savefig(output_path, dpi=viz_config['dpi'], bbox_inches='tight')
```

### 2. New Files Created

#### `examples/config_example.py`
A comprehensive example script demonstrating:
- How to load configuration
- Accessing different configuration sections
- Using config values in practice
- All available configuration attributes
- Benefits of centralized configuration

### 3. Configuration Structure

The `config/config.yml` file provides centralized control over:

**Paths:**
- `data_dir`: Where data files are stored
- `visualization_dir`: Where plots are saved
- `config_dir`: Configuration file location

**Data Generation:**
- `num_customers`: Number of customers to generate
- `seed`: Random seed for reproducibility
- `purchase_frequency_range`: Min/max purchases
- `revenue_range`: Min/max revenue values
- `date_range`: Start/end dates for transactions

**Columns:**
- `core_features`: Base customer metrics
- `departments`: Department definitions and metrics
- `classes`: Product class definitions
- `sizes`: Size/age breakdown definitions

**Clustering:**
- `fuzzy`: Fuzzy C-Means parameters (n_clusters, fuzziness, max_iter, error)
- `neural`: Neural network parameters (n_clusters, encoding_dim, epochs, batch_size, learning_rate)

**Visualization:**
- `dpi`: Image resolution
- `format`: Output format (png, jpg, svg, pdf)
- `color_palette`: Color scheme
- `figure_size`: Default figure dimensions
- `style`: Matplotlib style

## Benefits

### 1. **Centralized Management**
- All parameters in one place
- Easy to find and modify settings
- No need to search through multiple files

### 2. **Consistency**
- Same parameters across all scripts
- Reproducible results with fixed seed
- Uniform output formats

### 3. **Flexibility**
- Change parameters without modifying code
- Easy to create different configurations for different scenarios
- Support for environment-specific settings

### 4. **Maintainability**
- Clear documentation of all parameters
- Type information and descriptions in YAML
- Version control friendly

### 5. **Scalability**
- Easy to add new parameters
- Can override config values programmatically if needed
- Supports multiple configuration files

## Usage Examples

### Basic Usage
```python
from customer_segmentation import get_config

config = get_config('config/config.yml')
num_customers = config.data_generation['num_customers']
```

### Using in Data Generation
```python
from customer_segmentation import RetailDataGenerator, get_config

config = get_config('config/config.yml')
generator = RetailDataGenerator(seed=config.data_generation['seed'])
data = generator.generate_customer_data(
    n_customers=config.data_generation['num_customers']
)
```

### Using in Clustering
```python
from customer_segmentation import FuzzyCustomerSegmentation, get_config

config = get_config('config/config.yml')
fuzzy_params = config.clustering['fuzzy']
model = FuzzyCustomerSegmentation(
    n_clusters=fuzzy_params['n_clusters'],
    m=fuzzy_params['fuzziness'],
    seed=config.data_generation['seed']
)
```

### Using for Paths
```python
from pathlib import Path
from customer_segmentation import get_config

config = get_config('config/config.yml')
data_dir = Path(config.paths['data_dir'])
output_file = data_dir / "results.csv"
```

## Testing

The test suite (`tests/test_segmentation.py`) continues to work without modification as it already used parameterized values. Tests can optionally be updated to use config values if desired.

## Migration Guide

For any custom scripts not yet updated:

1. **Import the config loader:**
   ```python
   from customer_segmentation import get_config
   ```

2. **Load configuration:**
   ```python
   config = get_config('path/to/config.yml')
   ```

3. **Replace hardcoded values:**
   - Replace `n_customers=500` → `config.data_generation['num_customers']`
   - Replace `seed=42` → `config.data_generation['seed']`
   - Replace `n_clusters=4` → `config.clustering['fuzzy']['n_clusters']`
   - Replace `dpi=150` → `config.visualization['dpi']`
   - Replace `"../data/"` → `config.paths['data_dir']`

4. **Test your script** to ensure it works with the new configuration system.

## Future Enhancements

Potential improvements to the configuration system:
- Environment-specific configs (dev, prod, test)
- Config validation schemas
- Config inheritance/overrides
- Command-line config overrides
- Dynamic config reloading
- Config versioning

## Files Modified

- ✅ `examples/generate_customer_data.py`
- ✅ `examples/run_segmentation_pipeline.py`
- ✅ `examples/visualize_segments.py`
- ✅ `requirements.txt` (added PyYAML)

## Files Created

- ✅ `config/config.yml` (comprehensive configuration)
- ✅ `src/customer_segmentation/config_loader.py` (config utility)
- ✅ `examples/config_example.py` (usage demonstration)

## Files Not Modified

- `tests/test_segmentation.py` (already parameterized)
- Core modules (`data_generator.py`, `fuzzy_clustering.py`, `neural_clustering.py`, `cluster_enrichment.py`) - these remain parameter-agnostic
