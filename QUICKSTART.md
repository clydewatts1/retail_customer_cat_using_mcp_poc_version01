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

## Quick Start: Generate Data with Personas

### Generate Customer Data (5 minutes)

```bash
python examples/generate_customer_data.py
```

This generates:
- **Basic dataset** (`customer_sales_data_basic.csv`) - 51 columns for clustering
- **Enriched dataset** (`customer_sales_data_enriched.csv`) - 757 columns with full profiles
- 10 persona types with realistic shopping patterns
- Report showing persona distribution

### Run Segmentation Pipeline

```bash
python examples/run_segmentation_pipeline.py
```

This will:
- Load basic dataset for clustering
- Perform Fuzzy, Neural, and GMM clustering
- Use enriched dataset for analysis
- Generate cluster profiles for AI agents

## Understanding the Output

After running the pipeline, check the `data/` directory for:

### 1. customer_sales_data_basic.csv
**51 columns** - Optimized for clustering algorithms:
- Core RFM metrics: total_purchases, total_revenue, avg_order_value, recency_days, frequency_per_month
- Customer lifetime metrics: customer_lifetime_months, return_rate
- Department summaries: dept_total_value_* (21 columns), dept_total_units_* (21 columns)
- Ground truth: true_segment

### 2. customer_sales_data_enriched.csv
**757 columns** - Full customer profiles:
- All basic features PLUS:
- Persona type: persona_type (teenage_girl, young_woman_fashion, etc.)
- Customer profile: first_name, last_name, email, phone, address, city, state, zip_code, country
- Class-level details: class_total_value_* (394 columns), class_total_units_* (394 columns)
- Size/age breakdowns: count_Baby, count_Child, count_size_* (7 columns)

### 3. customers_with_segments.csv
Customer data enriched with:
- Fuzzy cluster assignment
- Neural cluster assignment
- GMM cluster assignment
- Membership degrees for each cluster
- Segment name

### 4. customer_segments_for_ai.json
Enriched segment profiles containing:
- Segment name (e.g., "VIP Champions")
- Description
- Key characteristics
- Recommended interaction strategies

### 5. data/output/ Directory
Cluster profiles for each algorithm:
- `fuzzy_cluster_profile_*.json/yaml` - Fuzzy clustering results
- `neural_cluster_profile_*.json/yaml` - Neural clustering results
- `gmm_cluster_profile_*.json/yaml` - GMM clustering results

## Persona Configuration

### Quick Reference: 10 Customer Personas

| Persona | Weight | Top Departments | AOV Range | Focus |
|---------|--------|-----------------|-----------|-------|
| teenage_girl | 10% | Ladies Clothing, Accessories, Shoes | $30-80 | Fashion trends |
| teenage_boy | 10% | Uwear & Nwear, Accessories, Sports | $30-80 | Sports & casual |
| young_woman_fashion | 12% | Ladies Clothing, Shoes, Accessories | $80-200 | High fashion |
| young_man_fashion | 10% | Uwear & Nwear, Accessories, Sports | $60-150 | Style-conscious |
| woman_with_baby | 8% | Kids Clothing, Kids Accessories, Nursery | $40-100 | New mother |
| woman_young_family | 12% | Kids Clothing, Nursery, Home | $50-120 | Family shopper |
| professional_woman | 10% | Ladies Clothing, Shoes, Accessories | $100-250 | Career wear |
| professional_man | 10% | Uwear & Nwear, Accessories, Sports | $100-250 | Business attire |
| budget_shopper | 10% | Value Shop, Accessories, Basic styles | $20-60 | Value-seeking |
| mature_shopper | 8% | Home, Xmas Shop, Gifts | $60-150 | Gift-focused |

### Customize Personas
Edit `config/personas.yml` to adjust:
```yaml
personas:
  - name: teenage_girl
    weight: 0.10  # Must sum to 1.0 across all personas
    demographics:
      age_range: [13, 19]
      gender: female
    department_preferences:
      "Ladies Clothing": 0.40  # Must sum to 1.0
      "Accessories": 0.25
      "Shoes": 0.20
    spending_profile:
      avg_order_value_range: [30, 80]
      purchases_per_year_range: [12, 24]
```

See `PERSONA_IMPLEMENTATION_COMPLETE.md` for full documentation.

## Using with Your Own Data

### Option 1: Generate Synthetic Data
```python
from customer_segmentation import RetailDataGenerator

# Generate with personas
generator = RetailDataGenerator(config_path='config/config.yml')
basic_df, enriched_df = generator.generate_customer_data(
    num_customers=1000, 
    dataset_type='both'
)

# Generate just basic dataset
basic_df = generator.generate_customer_data(
    num_customers=1000, 
    dataset_type='basic'
)
```

### Option 2: Use Real Data
1. **Prepare your data** with basic columns (51 required):
   - `customer_id`
   - `total_purchases`
   - `total_revenue`
   - `avg_order_value`
   - `recency_days`
   - `frequency_per_month`
   - `customer_lifetime_months`
   - `return_rate`
   - Department summaries: `dept_total_value_*`, `dept_total_units_*` (21 each)

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
