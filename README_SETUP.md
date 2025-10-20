# Environment Setup Instructions

This document provides instructions for setting up the Python environment with Anaconda and Jupyter Notebooks for the Retail Customer Categorization project.

## Prerequisites

- [Anaconda](https://www.anaconda.com/products/distribution) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html) installed on your system
- Git (for cloning the repository)

## Quick Start

### 1. Create and Activate the Conda Environment

Using the `environment.yml` file:

```bash
# Create the environment
conda env create -f environment.yml

# Activate the environment
conda activate retail_customer_cat
```

### 2. Alternative: Using pip with requirements.txt

If you prefer to use pip:

```bash
# Create a virtual environment (optional but recommended)
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Install the Package in Development Mode

```bash
# From the project root directory
pip install -e .
```

### 4. Set up Jupyter Notebook Extensions (Optional)

```bash
# Install and enable jupyter notebook extensions
jupyter contrib nbextension install --user
jupyter nbextensions_configurator enable --user
```

### 5. Launch Jupyter Lab or Notebook

```bash
# Launch JupyterLab (recommended)
jupyter lab

# Or launch Jupyter Notebook
jupyter notebook
```

The Jupyter interface will open in your default web browser, and you can navigate to the `notebooks/` directory to start working.

## Project Structure

```
retail_customer_cat_using_mcp_poc/
├── environment.yml          # Conda environment specification
├── requirements.txt         # Python package dependencies
├── README.md               # Project overview
├── README_SETUP.md         # This file - setup instructions
├── notebooks/              # Jupyter notebooks for analysis
├── data/                   # Data directory
│   ├── raw/               # Raw, immutable data
│   ├── processed/         # Cleaned and processed data
│   └── external/          # External data sources
├── src/                    # Source code
│   └── retail_customer_cat/  # Main package
├── tests/                  # Unit tests
└── config/                 # Configuration files
```

## Managing the Environment

### Updating the Environment

If you modify `environment.yml`:

```bash
conda env update -f environment.yml --prune
```

If you modify `requirements.txt`:

```bash
pip install -r requirements.txt --upgrade
```

### Exporting the Environment

To share your environment with others:

```bash
# Export conda environment
conda env export > environment.yml

# Export pip requirements
pip freeze > requirements.txt
```

### Removing the Environment

If you need to remove the environment:

```bash
conda deactivate
conda env remove -n retail_customer_cat
```

## Key Dependencies

- **Python 3.11**: Programming language
- **Jupyter Lab/Notebook**: Interactive development environment
- **NumPy & Pandas**: Data manipulation and analysis
- **Scikit-learn**: Traditional machine learning algorithms
- **Scikit-fuzzy**: Fuzzy logic and clustering
- **TensorFlow & Keras**: Neural network implementations
- **Matplotlib, Seaborn, Plotly**: Data visualization

## Troubleshooting

### Kernel Not Found in Jupyter

If the kernel is not showing up in Jupyter:

```bash
python -m ipykernel install --user --name=retail_customer_cat
```

### Import Errors

Make sure the environment is activated:

```bash
conda activate retail_customer_cat
```

And the package is installed in development mode:

```bash
pip install -e .
```

### Permission Issues

On some systems, you may need to run commands without `--user` flag or with appropriate permissions.

## Getting Started

1. Check out the example notebooks in the `notebooks/` directory
2. Place your raw data in the `data/raw/` directory
3. Start developing your customer categorization models!

## Additional Resources

- [Jupyter Documentation](https://jupyter.org/documentation)
- [Conda Cheat Sheet](https://docs.conda.io/projects/conda/en/latest/user-guide/cheatsheet.html)
- [Scikit-fuzzy Documentation](https://pythonhosted.org/scikit-fuzzy/)
- [TensorFlow Documentation](https://www.tensorflow.org/guide)
