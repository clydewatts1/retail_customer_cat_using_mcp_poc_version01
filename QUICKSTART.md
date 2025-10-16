# Customer Segmentation POC - Quick Start Guide

## Installation

1. **Clone the repository:**
```bash
git clone https://github.com/clydewatts1/retail_customer_cat_using_mcp_poc.git
cd retail_customer_cat_using_mcp_poc
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## Running the Example

```bash
cd examples
python run_segmentation_pipeline.py
```

This will generate sample data, perform clustering, and create enriched segment profiles.

## Understanding the Output

After running the pipeline, check the `data/` directory for:

### 1. customer_sales_data.csv
Raw customer data with features like:
- Total purchases
- Total revenue
- Average order value
- Recency (days since last purchase)
- Purchase frequency
- Customer lifetime
- Return rate

### 2. customers_with_segments.csv
Customer data enriched with:
- Fuzzy cluster assignment
- Neural cluster assignment
- Membership degrees for each cluster
- Segment name

### 3. customer_segments_for_ai.json
Enriched segment profiles containing:
- Segment name (e.g., "VIP Champions")
- Description
- Key characteristics
- Recommended interaction strategies

## Using with Your Own Data

1. **Prepare your data** with columns:
   - `customer_id`
   - `total_purchases`
   - `total_revenue`
   - `avg_order_value`
   - `recency_days`
   - `frequency_per_month`
   - `customer_lifetime_months`
   - `return_rate`

2. **Load and cluster:**
```python
import pandas as pd
from customer_segmentation import FuzzyCustomerSegmentation, ClusterEnrichment

# Load your data
data = pd.read_csv('your_customer_data.csv')

# Perform clustering
model = FuzzyCustomerSegmentation(n_clusters=4)
labels, membership = model.fit_predict(data)

# Enrich clusters
enrichment = ClusterEnrichment()
centers = model.get_cluster_centers()
profiles = enrichment.enrich_clusters(data, labels, centers)

# Export for AI agents
enrichment.export_for_ai_agent('segments_for_ai.json')
```

## Adjusting Parameters

### Number of Clusters
```python
# Try different numbers of clusters
model = FuzzyCustomerSegmentation(n_clusters=5)
```

### Fuzziness Level
```python
# m=1.0 is hard clustering, m>1.0 is fuzzy
# Higher m = more fuzzy (customers can belong to multiple segments)
model = FuzzyCustomerSegmentation(n_clusters=4, m=2.5)
```

### Neural Network Training
```python
# Adjust training parameters
model = NeuralCustomerSegmentation(
    n_clusters=4,
    encoding_dim=10,  # Dimensionality of learned features
    epochs=100,       # More epochs = better learning
    batch_size=32
)
```

## Troubleshooting

**Issue:** TensorFlow warnings about GPU
- **Solution:** These are informational only. The code runs fine on CPU.

**Issue:** Poor clustering results
- **Solution:** Try adjusting the number of clusters or fuzziness parameter.
- **Solution:** Ensure your data has enough variability in the features.

**Issue:** Module not found errors
- **Solution:** Make sure you're running from the correct directory and have installed all dependencies.

## Next Steps

1. Review the generated segment profiles
2. Customize interaction strategies for your business
3. Integrate with your AI agent system
4. Apply to real customer data
5. Set up automated re-clustering pipeline

## Support

For issues or questions, please open an issue on GitHub.
