# Retail Customer Segmentation using Machine Learning POC

This is a proof of concept project that demonstrates customer segmentation based on retail sales data using fuzzy clustering, neural network, and Gaussian Mixture Model (GMM) approaches. The clustering results are enriched with meaningful descriptions and metadata for AI agent-driven customer interactions.

## Overview

This POC implements:
- **Synthetic Data Generation**: Creates realistic retail customer sales data with hierarchical product structure
- **Fuzzy C-Means Clustering**: Soft clustering that allows customers to belong to multiple segments with varying degrees
- **Neural Network Clustering**: Deep learning-based clustering using autoencoders
- **GMM Clustering**: Probabilistic clustering using Gaussian Mixture Models with uncertainty quantification
- **Cluster Enrichment**: Adds human-readable descriptions, segment names, and interaction strategies
- **AI Agent Integration**: Exports data in a format suitable for AI agents to perform customer interactions

## Features

### 1. Data Generation
- Generates synthetic customer sales data with realistic patterns
- Includes key RFM (Recency, Frequency, Monetary) metrics
- Hierarchical product structure: Departments → Classes
- Creates multiple customer segments with distinct characteristics

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

## Example Scripts

### 1. Run Complete Segmentation Pipeline
```bash
cd examples
python run_segmentation_pipeline.py
```

### 2. Run GMM Clustering Only
```bash
cd examples
python run_gmm_clustering.py
```

### 3. Interactive Jupyter Notebook
```bash
cd examples
jupyter notebook customer_segmentation_analysis.ipynb
```

The notebook includes all three clustering methods with comprehensive visualizations and comparisons.

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
