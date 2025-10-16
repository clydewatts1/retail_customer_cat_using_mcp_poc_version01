# Examples Directory

This directory contains example scripts demonstrating the retail customer segmentation system with the centralized configuration module.

## Available Scripts

### 1. `test_config.py` - Configuration Validation ✓
**Purpose:** Test that the configuration module is working correctly

**Usage:**
```powershell
python examples/test_config.py
```

**Output:**
- Verifies all config attributes are accessible
- Tests nested value access
- Confirms configuration structure

**When to run:** After modifying `config/config.yml` or `config_loader.py`

---

### 2. `config_example.py` - Configuration Usage Demo 📚
**Purpose:** Comprehensive demonstration of how to use the config module

**Usage:**
```powershell
python examples/config_example.py
```

**Output:**
- Shows all configuration sections
- Demonstrates access patterns
- Displays actual config values
- Provides usage examples

**When to run:** When learning how to use the configuration system

---

### 3. `generate_customer_data.py` - Data Generation 📊
**Purpose:** Generate synthetic retail customer data with enriched features

**Usage:**
```powershell
python examples/generate_customer_data.py
```

**Output:**
- Creates `data/customer_sales_data_enriched.csv`
- Includes department/class totals
- Includes size/age breakdowns

**Configuration used:**
- `config.data_generation['num_customers']` - Number of records (default: 1000)
- `config.data_generation['seed']` - Random seed (default: 42)
- `config.paths['data_dir']` - Output directory (default: "data")

---

### 4. `run_segmentation_pipeline.py` - Complete Pipeline 🎯
**Purpose:** Run the complete customer segmentation workflow

**Usage:**
```powershell
python examples/run_segmentation_pipeline.py
```

**What it does:**
1. Generates synthetic customer data with enriched features
2. Performs Fuzzy C-Means clustering
3. Performs Neural Network clustering
4. Enriches clusters with descriptions and strategies
5. Analyzes department, class, and size preferences per segment
6. Exports results for AI agent interaction

**Output files:**
- `data/customer_sales_data_enriched.csv` - Raw enriched data
- `data/customers_with_segments.csv` - Data with cluster assignments
- `data/customer_segments_for_ai.json` - Enriched segment profiles

**Configuration used:**
- `config.data_generation` - Data generation parameters
- `config.clustering['fuzzy']` - Fuzzy clustering parameters
- `config.clustering['neural']` - Neural network parameters
- `config.paths['data_dir']` - Output directory

**Runtime:** ~30-60 seconds depending on configuration

---

### 5. `visualize_segments.py` - Visualization Generation 📈
**Purpose:** Create visualizations of customer segments

**Usage:**
```powershell
python examples/visualize_segments.py
```

**What it does:**
1. Generates customer data and performs segmentation
2. Creates 6 different visualization types:
   - Cluster distribution (bar chart and pie chart)
   - Segment characteristics (revenue, frequency, recency, AOV)
   - RFM scatter plots
   - Fuzzy membership heatmap
   - Department preferences by segment
   - Size/age distribution by segment

**Output files:** (in `visualizations/` directory)
- `cluster_distribution.png` - Customer distribution across segments
- `segment_characteristics.png` - Key metrics comparison
- `rfm_scatter.png` - RFM analysis scatter plots
- `membership_heatmap.png` - Fuzzy membership visualization
- `department_preferences.png` - Department spending patterns
- `size_distribution.png` - Size/age breakdowns

**Configuration used:**
- `config.data_generation` - Data parameters
- `config.clustering['fuzzy']` - Clustering parameters
- `config.visualization` - Plot settings (DPI, format, colors)
- `config.paths['visualization_dir']` - Output directory

**Runtime:** ~30-45 seconds

---

## Quick Start

### 1. First Time Setup
```powershell
# Install dependencies
pip install -r requirements.txt

# Verify configuration works
python examples/test_config.py
```

### 2. Learn About Configuration
```powershell
# See how to use config
python examples/config_example.py
```

### 3. Generate Data
```powershell
# Create customer dataset
python examples/generate_customer_data.py
```

### 4. Run Analysis
```powershell
# Complete segmentation pipeline
python examples/run_segmentation_pipeline.py

# Create visualizations
python examples/visualize_segments.py
```

---

## Configuration

All scripts use `config/config.yml` for parameters. To customize:

1. **Edit config file:**
   ```yaml
   data_generation:
     num_customers: 2000  # Change number of customers
     seed: 123           # Change random seed
   
   clustering:
     fuzzy:
       n_clusters: 5     # Change number of clusters
   ```

2. **Run scripts** - They will automatically use new values

**No code changes required!**

---

## Common Workflows

### Workflow 1: Quick Demo
```powershell
# See config in action
python examples/config_example.py

# Generate and visualize
python examples/visualize_segments.py
```

### Workflow 2: Full Analysis
```powershell
# Complete pipeline with all outputs
python examples/run_segmentation_pipeline.py

# Then create visualizations
python examples/visualize_segments.py
```

### Workflow 3: Custom Configuration
```powershell
# 1. Edit config/config.yml (change parameters)
# 2. Validate config
python examples/test_config.py

# 3. Run with new settings
python examples/generate_customer_data.py
python examples/run_segmentation_pipeline.py
```

---

## Output Directory Structure

After running the scripts:

```
data/
├── customer_sales_data_enriched.csv      # Generated data
├── customers_with_segments.csv           # Data with clusters
└── customer_segments_for_ai.json         # AI agent export

visualizations/
├── cluster_distribution.png
├── segment_characteristics.png
├── rfm_scatter.png
├── membership_heatmap.png
├── department_preferences.png
└── size_distribution.png
```

---

## Troubleshooting

### "Config object has no attribute..."
**Solution:** Make sure `config_loader.py` has been updated with all property accessors. Run `test_config.py` to verify.

### "ModuleNotFoundError: No module named 'yaml'"
**Solution:** Install PyYAML:
```powershell
pip install pyyaml>=6.0
```

### Scripts can't find config file
**Solution:** Make sure you're running from the correct directory or use absolute paths:
```powershell
cd c:\projects\retail_clustering_poc\retail_customer_cat_using_mcp_poc
python examples/run_segmentation_pipeline.py
```

### Import errors
**Solution:** The scripts add parent directory to path automatically. If issues persist, check your Python path.

---

## Documentation

- **CONFIG_STATUS.md** - Overall configuration system status
- **CONFIG_MIGRATION.md** - Detailed migration guide
- **CONFIG_REFERENCE.md** - Quick reference for config usage
- **CONFIG_FIX.md** - Bug fix documentation
- **config/config.yml** - The actual configuration file

---

## Next Steps

1. ✅ Run `test_config.py` to verify setup
2. ✅ Explore `config_example.py` to learn config usage
3. ✅ Generate data with `generate_customer_data.py`
4. ✅ Run complete pipeline with `run_segmentation_pipeline.py`
5. ✅ Create visualizations with `visualize_segments.py`
6. 📝 Customize `config/config.yml` for your needs
7. 🚀 Adapt scripts for your own use cases
