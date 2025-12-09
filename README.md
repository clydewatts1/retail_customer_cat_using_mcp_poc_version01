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

This is a proof of concept project that demonstrates customer segmentation based on retail sales data using fuzzy clustering, neural network, and Gaussian Mixture Model (GMM) approaches. The clustering results are enriched with meaningful descriptions and metadata for AI agent-driven customer interactions.

## NOTE

This project has been cancelled. The POC version 1 worked in principal but the functionality was flawed. 
The synthetic data was flawed. The project will need to start again



## Overview

This POC implements:
- **Synthetic Data Generation**: Creates realistic retail customer sales data with hierarchical product structure
- **Fuzzy C-Means Clustering**: Soft clustering that allows customers to belong to multiple segments with varying degrees
- **Neural Network Clustering**: Deep learning-based clustering using autoencoders
- **GMM Clustering**: Probabilistic clustering using Gaussian Mixture Models with uncertainty quantification
- **Cluster Enrichment**: Adds human-readable descriptions, segment names, and interaction strategies
- **AI Agent Integration**: Exports data in a format suitable for AI agents to perform customer interactions

## Features

### 1. Data Generation (✨ Enhanced with Personas!)
- **Persona-Based Generation**: 10 realistic customer personas with distinct behavioral patterns
  - teenage_girl, teenage_boy, young_woman_fashion, young_man_fashion
  - woman_with_baby, woman_young_family
  - professional_woman, professional_man
  - budget_shopper, mature_shopper
- **Full Product Hierarchy**: 21 departments, 394 product classes
- **Dual Dataset Output**: 
  - **Basic Dataset** (51 columns): Core RFM metrics + department totals for clustering
  - **Enriched Dataset** (757 columns): Full features including persona type, class details, customer profiles
- Generates synthetic customer sales data with realistic patterns
- Includes key RFM (Recency, Frequency, Monetary) metrics
- Hierarchical product structure: Departments → Classes
- Creates multiple customer segments with distinct characteristics
- Optional: Adds realistic profile fields using the Faker library (first_name, last_name, email, phone, address, city, state, zip_code, country, signup_date)

### 2. Fuzzy Clustering
- Uses Fuzzy C-Means (FCM) algorithm for soft clustering
- Provides membership degrees for each customer to each cluster
- Better handles boundary cases where customers exhibit mixed behaviors

### 3. Neural Network Clustering
- Employs autoencoder architecture for feature learning
- Performs dimensionality reduction before clustering
- Can capture complex non-linear relationships

### 4. GMM Clustering (New!)
- Probabilistic clustering with Gaussian distributions
- Provides soft assignments (probability distributions)
- Uncertainty quantification for cluster memberships
- Model selection via BIC/AIC metrics
- Multiple covariance structure options

### 5. Cluster Enrichment
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
6. Optionally include realistic profile fields if enabled in config

### Using Individual Components

#### Generate Customer Data (with Personas)

```python
from customer_segmentation import RetailDataGenerator

# Create generator with persona support (recommended)
generator = RetailDataGenerator(
    seed=42,
    faker_enabled=True,
    faker_locale='en_US',
    use_personas=True,  # Enable persona-based generation
    personas_config_path='config/personas.yml',
    hierarchy_config_path='hierarchy_parsed.yml'
)

# Generate DUAL datasets (basic for clustering, enriched for analysis)
enriched_data = generator.generate_customer_data(
    n_customers=500,
    dataset_type='both'  # Generates both datasets
)
# Basic dataset auto-saved to: data/customer_sales_data_basic.csv
# Enriched dataset returned and can be saved manually

# OR generate only enriched dataset
enriched_data = generator.generate_customer_data(n_customers=500, dataset_type='enriched')

# OR generate only basic dataset (for clustering)
basic_data = generator.generate_customer_data(n_customers=500, dataset_type='basic')

# Legacy mode (backwards compatible - 4 segments without personas)
legacy_generator = RetailDataGenerator(seed=42, use_personas=False)
legacy_data = legacy_generator.generate_customer_data(n_customers=500)
```

#### Fuzzy Clustering (Use Basic Dataset)

```python
from customer_segmentation import FuzzyCustomerSegmentation
import pandas as pd

# Load BASIC dataset (recommended for clustering - prevents overfitting)
basic_data = pd.read_csv('data/customer_sales_data_basic.csv')

# Initialize model
fuzzy_model = FuzzyCustomerSegmentation(n_clusters=4, m=2.0)

# Fit and predict
cluster_labels, membership_matrix = fuzzy_model.fit_predict(basic_data)

# Get cluster centers
centers = fuzzy_model.get_cluster_centers()

# Evaluate clustering quality
metrics = fuzzy_model.evaluate(basic_data)
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

#### GMM Clustering

```python
from customer_segmentation import GMMCustomerSegmentation

# Initialize model
gmm_model = GMMCustomerSegmentation(
    n_clusters=4,
    covariance_type='full',
    max_iter=200,
    n_init=10
)

# Fit and predict (returns both labels and probabilities)
cluster_labels, probabilities = gmm_model.fit_predict(customer_data)

# Get cluster centers
centers = gmm_model.get_cluster_centers()

# Evaluate clustering quality
metrics = gmm_model.evaluate(customer_data)

# Analyze assignment uncertainty
uncertainty = gmm_model.get_uncertainty_metrics(customer_data)
print(f"High Confidence Customers: {uncertainty['high_confidence_pct']:.1f}%")
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

## Persona System

### Overview
The persona system generates realistic customer behavioral patterns based on 10 distinct customer types. Each persona has:
- **Demographics**: Age range, gender, lifestyle characteristics
- **Department Preferences**: Weighted preferences across 21 retail departments
- **Class Preferences**: Preferred product classes within each department
- **Spending Profile**: Average order value ranges and purchase frequency

### Available Personas
1. **teenage_girl** (10%) - Fashion-focused teenager, Ladies Clothing & Accessories
2. **teenage_boy** (10%) - Sports & casual wear enthusiast
3. **young_woman_fashion** (12%) - Trendy young professional, high spender
4. **young_man_fashion** (10%) - Style-conscious male shopper
5. **woman_with_baby** (8%) - New mother, focused on Kids Clothing & Accessories
6. **woman_young_family** (12%) - Family shopper across multiple departments
7. **professional_woman** (10%) - Career-focused, formal wear preference
8. **professional_man** (10%) - Business attire focus
9. **budget_shopper** (10%) - Value-seeking across departments
10. **mature_shopper** (8%) - Gift-focused, Home & Xmas Shop preference

### Customizing Personas
Edit `config/personas.yml` to:
- Adjust persona weights (must sum to 1.0)
- Modify department preferences
- Change spending ranges
- Add new personas

See `PERSONA_IMPLEMENTATION_COMPLETE.md` for detailed documentation.

## Dataset Types

### Basic Dataset (for Clustering)
**51 columns** - Optimized for clustering algorithms
- Core RFM metrics: total_purchases, total_revenue, avg_order_value, recency_days, frequency_per_month
- Customer lifetime: customer_lifetime_months, return_rate
- Department summaries: dept_total_value_* (21 columns), dept_total_units_* (21 columns)
- Ground truth: true_segment

**Use for:** Fuzzy clustering, Neural clustering, GMM clustering

### Enriched Dataset (for Analysis)
**757 columns** - Full customer profiles and detailed analytics
- All basic features PLUS:
- Persona information: persona_type
- Customer profile: first_name, last_name, email, phone, address, city, state, zip_code, country
- Class-level details: class_total_value_* (394 columns), class_total_units_* (394 columns)
- Size/age breakdowns: count_Baby, count_Child, count_size_* (7 columns)

**Use for:** Business intelligence, persona analysis, detailed customer insights, AI agent context

## Example Scripts

### 1. Generate Data with Personas
```bash
python examples/generate_customer_data.py
```
Generates both basic and enriched datasets with persona distribution report.

### 2. Run Complete Segmentation Pipeline
```bash
python examples/run_segmentation_pipeline.py
```
Uses basic dataset for clustering, enriched dataset for analysis.

### 3. Validate Persona Distribution
```bash
python examples/validate_persona_distribution.py
```
Generates 1000 customers and validates persona behavior patterns.

### 4. Test Persona Generation
```bash
python examples/test_persona_generation.py
```
Quick test of persona system with small datasets.

### 5. Run GMM Clustering Only
```bash
python examples/run_gmm_clustering.py
```

### 6. Interactive Jupyter Notebook
```bash
jupyter notebook examples/customer_segmentation_analysis.ipynb
```

The notebook includes all three clustering methods with comprehensive visualizations and comparisons.

## Output Files

After running the pipeline, you'll find these files in the `data/` directory:

1. **customer_sales_data.csv**: Original synthetic customer data
2. **customers_with_segments.csv**: Customer data with cluster assignments
3. **customer_segments_for_ai.json**: Enriched segment profiles for AI agents
4. If Faker is enabled, the enriched CSV will also contain profile columns: first_name, last_name, email, phone, address, city, state, zip_code, country, signup_date

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

## Configuration: Faker profile fields

Faker-driven profile fields are configurable in `config/config.yml`:

```
data_generation:
    n_customers: 500
    random_seed: 42
    faker:
        enabled: true      # Toggle to include profile fields
        locale: "en_US"   # Choose a locale (e.g., en_US, en_GB, fr_FR)
```

The example scripts automatically pick up these settings and pass them to `RetailDataGenerator`.

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
