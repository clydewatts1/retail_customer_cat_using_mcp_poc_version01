# Config Key Mapping - CORRECTED

## Issue Identified
The scripts were using incorrect key names that didn't match the actual `config.yml` structure.

## Correct Config Structure and Access Patterns

### Data Generation
**Config Structure:**
```yaml
data_generation:
  n_customers: 500              # NOT num_customers
  random_seed: 42               # NOT seed
  departments: [...]
  classes: [...]
  child_ages: [...]
  adult_sizes: [...]
```

**Correct Access:**
```python
num_customers = config.data_generation['n_customers']
seed = config.data_generation['random_seed']
departments = config.data_generation['departments']
```

**WRONG (will cause KeyError):**
```python
num_customers = config.data_generation['num_customers']  # ❌
seed = config.data_generation['seed']  # ❌
```

---

### Clustering Parameters
**Config Structure:**
```yaml
# Top-level keys, NOT nested under 'clustering'
fuzzy_clustering:
  n_clusters: 4
  fuzziness_parameter: 2.0      # NOT fuzziness
  max_iterations: 150
  tolerance: 1e-5
  random_seed: 42

neural_clustering:
  n_clusters: 4
  encoding_dim: 10
  epochs: 50
  batch_size: 32
  learning_rate: 0.001
  random_seed: 42
```

**Correct Access:**
```python
# Access fuzzy clustering params
fuzzy_params = config._config.get('fuzzy_clustering', {})
n_clusters = fuzzy_params.get('n_clusters', 4)
fuzziness = fuzzy_params.get('fuzziness_parameter', 2.0)

# Access neural clustering params
neural_params = config._config.get('neural_clustering', {})
encoding_dim = neural_params.get('encoding_dim', 10)
```

**WRONG (will cause KeyError):**
```python
fuzzy_params = config.clustering['fuzzy']  # ❌ No 'clustering' key
fuzziness = fuzzy_params['fuzziness']  # ❌ Should be 'fuzziness_parameter'
```

---

### Paths
**Config Structure:**
```yaml
paths:
  data_dir: "data"
  visualizations_dir: "visualizations"    # NOT visualization_dir
  models_dir: "models"
```

**Correct Access:**
```python
data_dir = config.paths['data_dir']
viz_dir = config.paths['visualizations_dir']
```

**WRONG (will cause KeyError):**
```python
viz_dir = config.paths['visualization_dir']  # ❌ Should be 'visualizations_dir'
```

---

### Visualization Settings
**Config Structure:**
```yaml
visualization:
  dpi: 150
  figure_format: "png"          # NOT format
  style: "seaborn-v0_8"
  color_palette: "Set2"
  figure_sizes: {...}
```

**Correct Access:**
```python
viz_config = config.visualization
dpi = viz_config.get('dpi', 150)
format = viz_config.get('figure_format', 'png')
style = viz_config.get('style', 'seaborn-v0_8')
```

**WRONG (will cause KeyError):**
```python
format = viz_config['format']  # ❌ Should be 'figure_format'
```

---

## Complete Corrected Examples

### Example 1: Data Generation
```python
from customer_segmentation import RetailDataGenerator, get_config

config = get_config('config/config.yml')

# ✅ CORRECT
num_customers = config.data_generation['n_customers']
seed = config.data_generation['random_seed']

generator = RetailDataGenerator(seed=seed)
data = generator.generate_customer_data(n_customers=num_customers)
```

### Example 2: Fuzzy Clustering
```python
from customer_segmentation import FuzzyCustomerSegmentation, get_config

config = get_config('config/config.yml')

# ✅ CORRECT
fuzzy_params = config._config.get('fuzzy_clustering', {})
seed = config.data_generation['random_seed']

model = FuzzyCustomerSegmentation(
    n_clusters=fuzzy_params.get('n_clusters', 4),
    m=fuzzy_params.get('fuzziness_parameter', 2.0),
    seed=seed
)
```

### Example 3: Neural Clustering
```python
from customer_segmentation import NeuralCustomerSegmentation, get_config

config = get_config('config/config.yml')

# ✅ CORRECT
neural_params = config._config.get('neural_clustering', {})
seed = config.data_generation['random_seed']

model = NeuralCustomerSegmentation(
    n_clusters=neural_params.get('n_clusters', 4),
    encoding_dim=neural_params.get('encoding_dim', 10),
    epochs=neural_params.get('epochs', 50),
    batch_size=neural_params.get('batch_size', 32),
    seed=seed
)
```

### Example 4: Visualization
```python
from pathlib import Path
from customer_segmentation import get_config

config = get_config('config/config.yml')

# ✅ CORRECT
viz_dir = Path(config.paths['visualizations_dir'])
viz_config = config.visualization
dpi = viz_config.get('dpi', 150)
format = viz_config.get('figure_format', 'png')

output_path = viz_dir / f"plot.{format}"
fig.savefig(output_path, dpi=dpi, bbox_inches='tight')
```

---

## Summary of Key Differences

| Category | WRONG Key | CORRECT Key |
|----------|-----------|-------------|
| Data Generation | `num_customers` | `n_customers` |
| Data Generation | `seed` | `random_seed` |
| Clustering | `config.clustering['fuzzy']` | `config._config.get('fuzzy_clustering')` |
| Clustering | `config.clustering['neural']` | `config._config.get('neural_clustering')` |
| Clustering | `fuzziness` | `fuzziness_parameter` |
| Paths | `visualization_dir` | `visualizations_dir` |
| Visualization | `format` | `figure_format` |

---

## Why Use `.get()` for Clustering Params?

Since `fuzzy_clustering` and `neural_clustering` are top-level keys in the YAML file, they're not available as properties on the Config object. We access them via:

```python
config._config.get('fuzzy_clustering', {})
```

This safely returns the dictionary or an empty dict if the key doesn't exist.

---

## Files Updated

1. ✅ `examples/generate_customer_data.py` - Fixed `n_customers` and `random_seed`
2. ✅ `examples/run_segmentation_pipeline.py` - Fixed clustering param access
3. ✅ `examples/visualize_segments.py` - Fixed all config access patterns

---

## Testing

The scripts should now work correctly:

```powershell
python examples/generate_customer_data.py
python examples/run_segmentation_pipeline.py
python examples/visualize_segments.py
```

No more KeyError exceptions!
