# Project Structure Overview

This document provides a visual overview of the complete project structure.

## Complete Directory Tree

```
retail_customer_cat_using_mcp_poc/
│
├── 📄 README.md                          # Main project documentation
├── 📄 README_SETUP.md                    # Detailed setup instructions  
├── 📄 VERIFICATION.md                    # Verification and testing guide
├── 📄 STRUCTURE.md                       # This file - structure overview
├── 📄 .gitignore                         # Git ignore rules
├── 📄 environment.yml                    # Conda environment specification
├── 📄 requirements.txt                   # Python dependencies (pip)
├── 📄 pyproject.toml                     # Project configuration
├── 🔧 verify_setup.sh                    # Setup verification script
│
├── 📁 notebooks/                         # Jupyter notebooks
│   ├── 📄 README.md                      # Notebooks documentation
│   ├── 📓 01_data_exploration.ipynb      # Data exploration workflow
│   ├── 📓 02_fuzzy_clustering_traditional_ml.ipynb  # Traditional ML approach
│   └── 📓 03_fuzzy_clustering_neural_network.ipynb  # Neural network approach
│
├── 📁 data/                              # Data directory
│   ├── 📄 README.md                      # Data guidelines
│   ├── 📁 raw/                          # Raw, immutable data
│   │   └── .gitkeep
│   ├── 📁 processed/                    # Cleaned, processed data
│   │   └── .gitkeep
│   └── 📁 external/                     # External data sources
│       └── .gitkeep
│
├── 📁 src/                               # Source code
│   └── 📁 retail_customer_cat/          # Main package
│       └── 📄 __init__.py                # Package initialization
│
├── 📁 tests/                             # Unit tests
│   └── 📄 __init__.py                    # Test package initialization
│
├── 📁 config/                            # Configuration files
│   └── 📄 README.md                      # Configuration guidelines
│
└── 📁 models/                            # Trained models
    ├── 📄 README.md                      # Model storage guidelines
    └── .gitkeep
```

## Directory Purposes

### 📁 Root Level Files

| File | Purpose |
|------|---------|
| `README.md` | Main project documentation and overview |
| `README_SETUP.md` | Step-by-step environment setup instructions |
| `VERIFICATION.md` | Testing and verification procedures |
| `environment.yml` | Anaconda environment specification with all dependencies |
| `requirements.txt` | Pip-installable Python dependencies |
| `pyproject.toml` | Modern Python project configuration (PEP 518) |
| `.gitignore` | Specifies files to ignore in version control |
| `verify_setup.sh` | Automated verification script |

### 📁 notebooks/

Contains Jupyter notebooks for interactive data analysis and model development:

1. **01_data_exploration.ipynb**: Initial data loading, inspection, and exploratory data analysis
2. **02_fuzzy_clustering_traditional_ml.ipynb**: Fuzzy C-Means clustering using scikit-fuzzy
3. **03_fuzzy_clustering_neural_network.ipynb**: Neural network-based fuzzy clustering

Each notebook includes:
- Setup and imports
- Step-by-step workflow
- Visualization examples
- TODO placeholders for custom code

### 📁 data/

Organized data storage following best practices:

- **raw/**: Immutable original data files (never modify)
- **processed/**: Cleaned and transformed data ready for modeling
- **external/**: Third-party or external datasets

`.gitkeep` files maintain directory structure without committing large data files.

### 📁 src/retail_customer_cat/

Python package for reusable code:

- Utility functions
- Data preprocessing modules
- Custom model implementations
- Feature engineering code

Can be imported in notebooks: `from retail_customer_cat import ...`

### 📁 tests/

Unit tests for the codebase:

- Test data processing functions
- Test model implementations
- Test utility functions

Run with: `pytest tests/`

### 📁 config/

Configuration files for:

- Model hyperparameters
- Data processing parameters
- Application settings
- Environment-specific configurations

### 📁 models/

Storage for trained models:

- Serialized model files (.pkl, .h5, .pt)
- Model checkpoints
- Model metadata and documentation

Note: Large model files are excluded from git via `.gitignore`

## Key Features

### ✅ Anaconda Environment Support
- Complete `environment.yml` with all ML/DS dependencies
- Python 3.11 specified
- Jupyter, Pandas, NumPy, Scikit-learn included
- Fuzzy logic library (scikit-fuzzy)
- Deep learning (TensorFlow, Keras)
- Visualization (Matplotlib, Seaborn, Plotly)

### ✅ Jupyter Notebook Integration
- Three comprehensive starter notebooks
- Follows data science workflow
- Markdown documentation cells
- Code examples and templates
- Consistent structure

### ✅ Professional Project Structure
- Modular code organization
- Separation of concerns
- Version control ready
- Documentation at multiple levels
- Testing infrastructure

### ✅ Best Practices
- `.gitkeep` for empty directories
- `.gitignore` for data/models
- README files in each directory
- Development mode installation support
- Configuration management

## Getting Started

1. **Setup Environment**:
   ```bash
   conda env create -f environment.yml
   conda activate retail_customer_cat
   ```

2. **Install Package**:
   ```bash
   pip install -e .
   ```

3. **Verify Setup**:
   ```bash
   ./verify_setup.sh
   ```

4. **Launch Jupyter**:
   ```bash
   jupyter lab
   ```

5. **Start Working**:
   - Open `notebooks/01_data_exploration.ipynb`
   - Add your data to `data/raw/`
   - Follow the notebook workflow

## Maintenance

### Adding New Notebooks
Place in `notebooks/` with sequential numbering and descriptive names.

### Adding New Dependencies
1. Update `environment.yml` (for conda packages)
2. Update `requirements.txt` (for pip packages)
3. Update `pyproject.toml` dependencies
4. Re-run environment creation/update

### Adding New Modules
1. Create Python files in `src/retail_customer_cat/`
2. Add corresponding tests in `tests/`
3. Update package `__init__.py` if needed

### Documentation Updates
Keep README files up to date as the project evolves.
