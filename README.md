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
# Retail Customer Segmentation using Machine Learning POC

This is a proof of concept project that demonstrates customer segmentation based on retail sales data using fuzzy clustering and neural network approaches. The clustering results are enriched with meaningful descriptions and metadata for AI agent-driven customer interactions.

## Overview

This POC implements:
- **Synthetic Data Generation**: Creates realistic retail customer sales data
- **Fuzzy C-Means Clustering**: Soft clustering that allows customers to belong to multiple segments with varying degrees
- **Neural Network Clustering**: Deep learning-based clustering using autoencoders
- **Cluster Enrichment**: Adds human-readable descriptions, segment names, and interaction strategies
- **AI Agent Integration**: Exports data in a format suitable for AI agents to perform customer interactions

## Features

### 1. Data Generation
- Generates synthetic customer sales data with realistic patterns
- Includes key RFM (Recency, Frequency, Monetary) metrics
- Creates multiple customer segments with distinct characteristics

### 2. Fuzzy Clustering
- Uses Fuzzy C-Means (FCM) algorithm for soft clustering
- Provides membership degrees for each customer to each cluster
- Better handles boundary cases where customers exhibit mixed behaviors

### 3. Neural Network Clustering
- Employs autoencoder architecture for feature learning
- Performs dimensionality reduction before clustering
- Can capture complex non-linear relationships

### 4. Cluster Enrichment
- Generates descriptive segment names (e.g., "VIP Champions", "Loyal Regulars")
- Creates detailed descriptions of each segment
- Provides actionable interaction strategies for each segment
- Exports data in JSON format for AI agent consumption

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/clydewatts1/retail_customer_cat_using_mcp_poc.git
cd retail_customer_cat_using_mcp_poc
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Complete Pipeline

Run the example script to see the entire pipeline in action:

```bash
cd examples
python run_segmentation_pipeline.py
```

This will:
1. Generate 500 synthetic customer records
2. Perform fuzzy clustering
3. Perform neural network clustering
4. Enrich clusters with descriptions
5. Export data for AI agents

### Using Individual Components

#### Generate Customer Data

```python
from customer_segmentation import RetailDataGenerator

# Create generator
generator = RetailDataGenerator(seed=42)

# Generate customer data
customer_data = generator.generate_customer_data(n_customers=500)

# Save to file
generator.save_data(customer_data, 'customer_data.csv')
```

#### Fuzzy Clustering

```python
from customer_segmentation import FuzzyCustomerSegmentation

# Initialize model
fuzzy_model = FuzzyCustomerSegmentation(n_clusters=4, m=2.0)

# Fit and predict
cluster_labels, membership_matrix = fuzzy_model.fit_predict(customer_data)

# Get cluster centers
centers = fuzzy_model.get_cluster_centers()

# Evaluate clustering quality
metrics = fuzzy_model.evaluate(customer_data)
```

#### Neural Network Clustering

```python
from customer_segmentation import NeuralCustomerSegmentation

# Initialize model
neural_model = NeuralCustomerSegmentation(
    n_clusters=4,
    encoding_dim=10,
    epochs=100
)

# Fit and predict
cluster_labels = neural_model.fit_predict(customer_data, verbose=0)

# Get cluster centers
centers = neural_model.get_cluster_centers(customer_data)

# Evaluate clustering quality
metrics = neural_model.evaluate(customer_data)
```

#### Cluster Enrichment

```python
from customer_segmentation import ClusterEnrichment

# Initialize enrichment
enrichment = ClusterEnrichment()

# Enrich clusters
enriched_profiles = enrichment.enrich_clusters(
    customer_data,
    cluster_labels,
    cluster_centers
)

# Export for AI agents
enrichment.export_for_ai_agent('customer_segments_for_ai.json')
```

## Output Files

After running the pipeline, you'll find these files in the `data/` directory:

1. **customer_sales_data.csv**: Original synthetic customer data
2. **customers_with_segments.csv**: Customer data with cluster assignments
3. **customer_segments_for_ai.json**: Enriched segment profiles for AI agents

## Customer Segments

The system typically identifies 4 main customer segments:

1. **VIP Champions**: High-value, highly engaged customers with recent purchases
2. **Loyal Regulars**: Medium to high-value customers with consistent purchase patterns
3. **Promising Customers**: Growing customer base with potential for increased engagement
4. **At-Risk/Hibernating**: Customers requiring re-engagement campaigns

Each segment includes:
- Descriptive name and detailed description
- Statistical characteristics (size, revenue, frequency, etc.)
- Recommended interaction strategies
- Membership information (for fuzzy clustering)

## Technical Details

### Fuzzy C-Means Algorithm
- Fuzziness parameter (m): 2.0 (controls degree of fuzziness)
- Maximum iterations: 150
- Convergence threshold: 0.005

### Neural Network Architecture
- Encoder: Dense layers [64, 32, encoding_dim] with ReLU activation
- Decoder: Dense layers [32, 64, input_dim] with ReLU activation
- Batch normalization for stable training
- MSE loss function

### Features Used for Clustering
- Total purchases
- Total revenue
- Average order value
- Recency (days since last purchase)
- Frequency (purchases per month)
- Customer lifetime (months)
- Return rate

## Evaluation Metrics

### Fuzzy Clustering
- **Silhouette Score**: Measures cluster separation (-1 to 1, higher is better)
- **Partition Coefficient**: Fuzzy clustering quality (0 to 1, higher is better)
- **Partition Entropy**: Fuzziness level (lower is better)

### Neural Clustering
- **Silhouette Score**: Measures cluster separation
- **Reconstruction Error**: Autoencoder quality (lower is better)

## Use Cases

This POC can be applied to:
- Customer segmentation for targeted marketing
- Personalized product recommendations
- Customer lifetime value prediction
- Churn prevention strategies
- AI agent-driven customer service
- Dynamic pricing strategies

## Future Enhancements

Potential improvements for production use:
- Real-time clustering updates
- Integration with CRM systems
- Advanced feature engineering
- Temporal analysis (segment evolution over time)
- A/B testing framework for interaction strategies
- Multi-model ensemble approaches

## Contributing

This is a proof of concept project. Feel free to fork and adapt for your needs.

## License

MIT License - Feel free to use and modify for your purposes.

## Contact

For questions or feedback, please open an issue on GitHub.

## Acknowledgments

- Scikit-fuzzy library for fuzzy logic implementations
- TensorFlow team for the deep learning framework
- The open-source community for various tools and libraries used in this project
## Project Structure

```
retail_customer_cat_using_mcp_poc/
├── README.md                          # Main documentation
├── QUICKSTART.md                      # Quick start guide
├── requirements.txt                   # Python dependencies
├── src/
│   └── customer_segmentation/
│       ├── __init__.py               # Package initialization
│       ├── data_generator.py         # Synthetic data generation
│       ├── fuzzy_clustering.py       # Fuzzy C-Means implementation
│       ├── neural_clustering.py      # Neural network clustering
│       └── cluster_enrichment.py     # Cluster enrichment and export
├── examples/
│   ├── run_segmentation_pipeline.py  # Complete pipeline example
│   └── visualize_segments.py         # Visualization example
├── tests/
│   └── test_segmentation.py          # Unit tests
├── data/                              # Generated data (not in git)
│   └── README.md                     # Data directory info
└── visualizations/                    # Generated plots (not in git)
    └── README.md                     # Visualizations info
```
