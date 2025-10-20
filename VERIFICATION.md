# Setup Verification and Testing

This document provides information about verifying and testing the environment setup.

## Quick Verification

Run the verification script to check the environment setup:

```bash
./verify_setup.sh
```

This script checks:
- Directory structure completeness
- Configuration files presence
- Jupyter notebooks validity
- Documentation completeness
- Python package structure
- Package import functionality

## Manual Verification Steps

### 1. Verify Directory Structure

```bash
tree -L 2
```

Expected structure:
- `notebooks/` - Jupyter notebooks
- `data/` - Data directories (raw, processed, external)
- `src/` - Source code
- `tests/` - Unit tests
- `config/` - Configuration files
- `models/` - Trained models

### 2. Verify Configuration Files

Check that these files exist and are valid:
- `environment.yml` - Conda environment
- `requirements.txt` - Python dependencies
- `pyproject.toml` - Project configuration

### 3. Test Conda Environment Creation

```bash
# Create environment (dry run)
conda env create -f environment.yml --dry-run

# Actually create the environment
conda env create -f environment.yml

# Activate and verify
conda activate retail_customer_cat
python --version
conda list | grep jupyter
```

### 4. Test Package Installation

```bash
# Install in development mode
pip install -e .

# Test import
python -c "import retail_customer_cat; print(retail_customer_cat.__version__)"
```

### 5. Test Jupyter Setup

```bash
# List Jupyter kernels
jupyter kernelspec list

# Start Jupyter Lab
jupyter lab --no-browser

# Or start Jupyter Notebook
jupyter notebook --no-browser
```

### 6. Verify Notebooks

Check that notebooks can be opened and executed:
- `notebooks/01_data_exploration.ipynb`
- `notebooks/02_fuzzy_clustering_traditional_ml.ipynb`
- `notebooks/03_fuzzy_clustering_neural_network.ipynb`

## Troubleshooting

### Conda Environment Issues

If conda environment creation fails:
```bash
# Update conda
conda update conda

# Try with only essential packages first
conda create -n retail_customer_cat python=3.11 jupyter

# Then install additional packages
conda activate retail_customer_cat
pip install -r requirements.txt
```

### Jupyter Kernel Not Found

If the kernel doesn't appear in Jupyter:
```bash
conda activate retail_customer_cat
python -m ipykernel install --user --name=retail_customer_cat --display-name="Python (retail_customer_cat)"
```

### Package Import Errors

If package import fails:
```bash
# Ensure you're in the project root
cd /path/to/retail_customer_cat_using_mcp_poc

# Install in development mode
pip install -e .

# Or add to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
```

## Testing Checklist

- [ ] All directories created
- [ ] Configuration files present and valid
- [ ] Conda environment can be created
- [ ] Python package can be imported
- [ ] Jupyter Lab/Notebook starts successfully
- [ ] All notebooks open without errors
- [ ] Documentation is complete and accurate

## Performance Verification

Test that key libraries are available:

```python
import numpy
import pandas
import sklearn
import skfuzzy
import tensorflow
import matplotlib
import seaborn
import plotly

print("All libraries imported successfully!")
```

## Next Steps After Verification

1. Add your customer data to `data/raw/`
2. Start with `01_data_exploration.ipynb`
3. Follow the workflow through the notebooks
4. Customize models for your specific use case
