# Retail Customer Categorization using MCP - Proof of Concept

This is a proof of concept project using Python to categorize customers based on a combination of fuzzy clustering using either traditional ML or Neural Networks.

## Project Overview

This project implements customer segmentation using fuzzy clustering techniques to identify distinct customer groups based on their characteristics and behaviors. The project supports two approaches:

1. **Traditional ML Approach**: Using scikit-fuzzy's Fuzzy C-Means algorithm
2. **Neural Network Approach**: Using TensorFlow/Keras for deep learning-based fuzzy clustering

## Project Structure

```
retail_customer_cat_using_mcp_poc/
├── README.md                   # This file
├── README_SETUP.md            # Detailed setup instructions
├── environment.yml            # Conda environment specification
├── requirements.txt           # Python package dependencies
├── pyproject.toml            # Project configuration and build settings
├── .gitignore                # Git ignore rules
├── notebooks/                 # Jupyter notebooks for analysis
│   ├── 01_data_exploration.ipynb
│   ├── 02_fuzzy_clustering_traditional_ml.ipynb
│   ├── 03_fuzzy_clustering_neural_network.ipynb
│   └── README.md
├── data/                      # Data directory
│   ├── raw/                  # Raw, immutable data
│   ├── processed/            # Cleaned and processed data
│   ├── external/             # External data sources
│   └── README.md
├── src/                       # Source code
│   └── retail_customer_cat/  # Main package
│       └── __init__.py
├── tests/                     # Unit tests
│   └── __init__.py
└── config/                    # Configuration files
    └── README.md
```

## Quick Start

### Prerequisites

- [Anaconda](https://www.anaconda.com/products/distribution) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
- Python 3.9 or higher
- Git

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/clydewatts1/retail_customer_cat_using_mcp_poc.git
   cd retail_customer_cat_using_mcp_poc
   ```

2. **Create and activate the Conda environment:**
   ```bash
   conda env create -f environment.yml
   conda activate retail_customer_cat
   ```

3. **Install the package in development mode:**
   ```bash
   pip install -e .
   ```

4. **Launch Jupyter Lab:**
   ```bash
   jupyter lab
   ```

For detailed setup instructions, see [README_SETUP.md](README_SETUP.md).

## Features

- **Fuzzy C-Means Clustering**: Traditional fuzzy logic approach for soft customer segmentation
- **Neural Network Clustering**: Deep learning-based approach for complex pattern recognition
- **Comprehensive Data Pipeline**: From raw data to actionable insights
- **Interactive Notebooks**: Jupyter notebooks for exploratory analysis and model development
- **Modular Architecture**: Well-organized codebase for easy extension and maintenance

## Key Dependencies

- **Python 3.11**: Programming language
- **NumPy & Pandas**: Data manipulation
- **Scikit-learn**: Machine learning utilities
- **Scikit-fuzzy**: Fuzzy logic and clustering
- **TensorFlow & Keras**: Neural network implementation
- **Matplotlib, Seaborn, Plotly**: Data visualization
- **Jupyter Lab**: Interactive development environment

## Usage

1. **Prepare Your Data**: Place raw customer data in `data/raw/`
2. **Data Exploration**: Start with `notebooks/01_data_exploration.ipynb`
3. **Model Development**: 
   - Traditional ML: `notebooks/02_fuzzy_clustering_traditional_ml.ipynb`
   - Neural Networks: `notebooks/03_fuzzy_clustering_neural_network.ipynb`
4. **Compare Results**: Evaluate which approach works best for your data

## Development

### Running Tests

```bash
pytest tests/
```

### Code Formatting

```bash
black src/ tests/
```

### Linting

```bash
flake8 src/ tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is a proof of concept and is provided as-is for educational and research purposes.

## Contact

For questions or feedback, please open an issue on GitHub.

## Acknowledgments

- Scikit-fuzzy library for fuzzy logic implementations
- TensorFlow team for the deep learning framework
- The open-source community for various tools and libraries used in this project
