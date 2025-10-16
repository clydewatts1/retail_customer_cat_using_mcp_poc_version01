# Configuration Quick Reference Guide

## Loading Configuration

```python
from customer_segmentation import get_config

# Load default config
config = get_config('config/config.yml')
```

## Common Configuration Access Patterns

### Paths
```python
# Access directory paths
data_dir = config.paths['data_dir']              # "data"
viz_dir = config.paths['visualization_dir']      # "visualizations"
config_dir = config.paths['config_dir']          # "config"
```

### Data Generation
```python
# Customer generation parameters
num_customers = config.data_generation['num_customers']           # 1000
seed = config.data_generation['seed']                             # 42
freq_range = config.data_generation['purchase_frequency_range']   # [1, 20]
revenue_range = config.data_generation['revenue_range']           # [50, 5000]

# Date range
start_date = config.data_generation['date_range']['start']        # "2023-01-01"
end_date = config.data_generation['date_range']['end']            # "2024-12-31"

# Distribution parameters
revenue_dist = config.data_generation['revenue_distribution']
freq_dist = config.data_generation['frequency_distribution']
```

### Fuzzy Clustering
```python
fuzzy_params = config.clustering['fuzzy']

n_clusters = fuzzy_params['n_clusters']          # 4
fuzziness = fuzzy_params['fuzziness']            # 2.0
max_iter = fuzzy_params['max_iter']              # 150
error = fuzzy_params['error']                    # 0.005

# Usage
from customer_segmentation import FuzzyCustomerSegmentation

model = FuzzyCustomerSegmentation(
    n_clusters=fuzzy_params['n_clusters'],
    m=fuzzy_params['fuzziness'],
    seed=config.data_generation['seed']
)
```

### Neural Clustering
```python
neural_params = config.clustering['neural']

n_clusters = neural_params['n_clusters']         # 4
encoding_dim = neural_params['encoding_dim']     # 10
epochs = neural_params['epochs']                 # 50
batch_size = neural_params['batch_size']         # 32
learning_rate = neural_params['learning_rate']   # 0.001

# Usage
from customer_segmentation import NeuralCustomerSegmentation

model = NeuralCustomerSegmentation(
    n_clusters=neural_params['n_clusters'],
    encoding_dim=neural_params['encoding_dim'],
    epochs=neural_params['epochs'],
    batch_size=neural_params['batch_size'],
    seed=config.data_generation['seed']
)
```

### Column Definitions
```python
# Core features
core_features = config.columns['core_features']
# Access specific column info
revenue_col = core_features['total_revenue']
print(revenue_col['type'])          # "float"
print(revenue_col['description'])   # "Total revenue..."

# Department definitions
depts = config.columns['departments']['names']   # ["Apparel", "Footwear", ...]
dept_metrics = config.columns['departments']['metrics']

# Class definitions
classes = config.columns['classes']['names']
class_metrics = config.columns['classes']['metrics']

# Size definitions
child_ages = config.columns['sizes']['child_ages']
adult_sizes = config.columns['sizes']['adult_sizes']
```

### Visualization
```python
viz_config = config.visualization

dpi = viz_config['dpi']                          # 150
format = viz_config['format']                    # "png"
color_palette = viz_config['color_palette']      # "Set2"
figure_size = viz_config['figure_size']          # [12, 8]
style = viz_config['style']                      # "seaborn-v0_8-darkgrid"

# Usage
import matplotlib.pyplot as plt
plt.style.use(viz_config['style'])

output_path = f"plot.{viz_config['format']}"
fig.savefig(output_path, dpi=viz_config['dpi'], bbox_inches='tight')
```

## Complete Examples

### Example 1: Generate Data with Config
```python
from pathlib import Path
from customer_segmentation import RetailDataGenerator, get_config

# Load config
config = get_config('config/config.yml')

# Initialize with config parameters
generator = RetailDataGenerator(seed=config.data_generation['seed'])

# Generate data
data = generator.generate_customer_data(
    n_customers=config.data_generation['num_customers']
)

# Save to configured directory
data_dir = Path(config.paths['data_dir'])
data_dir.mkdir(exist_ok=True)
generator.save_data(data, str(data_dir / "customer_data.csv"))

print(f"Generated {len(data)} customers")
```

### Example 2: Run Clustering Pipeline
```python
from customer_segmentation import (
    RetailDataGenerator,
    FuzzyCustomerSegmentation,
    get_config
)

# Load config
config = get_config('config/config.yml')

# Generate data
generator = RetailDataGenerator(seed=config.data_generation['seed'])
data = generator.generate_customer_data(
    n_customers=config.data_generation['num_customers']
)

# Fuzzy clustering
fuzzy_params = config.clustering['fuzzy']
model = FuzzyCustomerSegmentation(
    n_clusters=fuzzy_params['n_clusters'],
    m=fuzzy_params['fuzziness'],
    seed=config.data_generation['seed']
)
labels, membership = model.fit_predict(data)

print(f"Created {fuzzy_params['n_clusters']} clusters")
```

### Example 3: Create Visualizations
```python
import matplotlib.pyplot as plt
from pathlib import Path
from customer_segmentation import get_config

# Load config
config = get_config('config/config.yml')

# Set visualization style
viz_config = config.visualization
plt.style.use(viz_config['style'])

# Create plot
fig, ax = plt.subplots(figsize=tuple(viz_config['figure_size']))
# ... plotting code ...

# Save to configured directory
viz_dir = Path(config.paths['visualization_dir'])
viz_dir.mkdir(exist_ok=True)
output_path = viz_dir / f"my_plot.{viz_config['format']}"
fig.savefig(output_path, dpi=viz_config['dpi'], bbox_inches='tight')

print(f"Saved visualization to {output_path}")
```

### Example 4: Custom Configuration Override
```python
from customer_segmentation import Config

# Load base config
config = Config('config/config.yml')

# Override specific values programmatically
config._config['data_generation']['num_customers'] = 2000
config._config['clustering']['fuzzy']['n_clusters'] = 5

# Use modified config
num_customers = config.data_generation['num_customers']  # 2000
n_clusters = config.clustering['fuzzy']['n_clusters']    # 5
```

## Configuration File Location

The default configuration file is located at:
```
config/config.yml
```

## Reloading Configuration

```python
from customer_segmentation import reload_config

# Reload if config.yml has been modified
reload_config('config/config.yml')
config = get_config('config/config.yml')
```

## Tips

1. **Always use config for parameters**: Avoid hardcoding values in scripts
2. **Use relative imports**: Import from `customer_segmentation` module
3. **Path construction**: Use `pathlib.Path` for cross-platform compatibility
4. **Seed consistency**: Use `config.data_generation['seed']` everywhere
5. **Documentation**: Config is self-documenting with descriptions

## Troubleshooting

### Config not loading?
```python
# Check if file exists
from pathlib import Path
config_path = Path('config/config.yml')
print(f"Config exists: {config_path.exists()}")

# Check current directory
import os
print(f"Current dir: {os.getcwd()}")
```

### Missing PyYAML?
```bash
# Install dependency
pip install pyyaml>=6.0
```

### Attribute error?
```python
# Check available sections
config = get_config('config/config.yml')
print(dir(config))  # See all available attributes

# Check config structure
print(config._config.keys())  # See top-level keys
```

## See Also

- `CONFIG_MIGRATION.md` - Detailed migration guide
- `examples/config_example.py` - Comprehensive usage examples
- `config/config.yml` - Full configuration file with all options
- `src/customer_segmentation/config_loader.py` - Config implementation
