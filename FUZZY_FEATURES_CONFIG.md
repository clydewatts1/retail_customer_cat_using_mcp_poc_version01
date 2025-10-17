# Fuzzy Clustering Features Configuration Guide

## Overview
The configuration now includes comprehensive options for fuzzy clustering features, allowing you to customize which features are used for customer segmentation.

## Configuration Location
File: `config/config.yml`

Section: `fuzzy_clustering`

## Configuration Options

### Basic Configuration

```yaml
fuzzy_clustering:
  n_clusters: 4                    # Number of clusters to create
  fuzziness_parameter: 2.0         # Fuzziness parameter (m) - typically 1.5-3.0
  max_iterations: 150              # Maximum iterations for convergence
  tolerance: 1e-5                  # Convergence tolerance
  random_seed: 42                  # Random seed for reproducibility
```

### Core Features (Default)

By default, fuzzy clustering uses these core RFM (Recency, Frequency, Monetary) features:

```yaml
features_to_use:
  - "total_purchases"              # Total number of purchases
  - "total_revenue"                # Total revenue generated
  - "avg_order_value"              # Average order value
  - "recency_days"                 # Days since last purchase
  - "frequency_per_month"          # Purchase frequency per month
  - "customer_lifetime_months"     # Customer lifetime in months
  - "return_rate"                  # Return rate percentage
```

### Enriched Features (Optional)

You can optionally include enriched product hierarchy features:

```yaml
use_enriched_features: false       # Set to true to enable
enriched_features_to_use:
  # Department value features (spending by department)
  - "dept_total_value_Accessories & Footwear"
  - "dept_total_value_Health & Wellness"
  - "dept_total_value_Home & Lifestyle"
  
  # Department unit features (units purchased by department)
  - "dept_total_units_Accessories & Footwear"
  - "dept_total_units_Health & Wellness"
  - "dept_total_units_Home & Lifestyle"
  
  # Class value features (spending by product class)
  - "class_total_value_Bags & Wallets"
  - "class_total_value_Soft & Hard Accessories"
  - "class_total_value_Consumables"
  - "class_total_value_Personal Care"
  - "class_total_value_Bedding"
  
  # Size/age features (purchase patterns)
  - "count_Baby"
  - "count_Child"
  - "count_size_XS"
  - "count_size_S"
  - "count_size_M"
  - "count_size_L"
  - "count_size_XL"
```

### Output Columns

Define the column names for clustering results:

```yaml
output_columns:
  cluster_label: "fuzzy_cluster"                           # Main cluster assignment
  membership_prefix: "fuzzy_membership_cluster_"           # Membership degree columns
  cluster_center_distance_prefix: "fuzzy_distance_to_cluster_"  # Distance to centers
```

## Usage Examples

### Example 1: Default Configuration (RFM Only)

```yaml
fuzzy_clustering:
  n_clusters: 4
  features_to_use:
    - "total_purchases"
    - "total_revenue"
    - "avg_order_value"
    - "recency_days"
    - "frequency_per_month"
    - "customer_lifetime_months"
    - "return_rate"
  use_enriched_features: false
```

**Result:** Segments based purely on purchase behavior (RFM)

### Example 2: With Department Features

```yaml
fuzzy_clustering:
  n_clusters: 4
  features_to_use:
    - "total_purchases"
    - "total_revenue"
    - "recency_days"
  use_enriched_features: true
  enriched_features_to_use:
    - "dept_total_value_Accessories & Footwear"
    - "dept_total_value_Health & Wellness"
    - "dept_total_value_Home & Lifestyle"
```

**Result:** Segments based on both behavior AND department preferences

### Example 3: Full Feature Set

```yaml
fuzzy_clustering:
  n_clusters: 5
  use_enriched_features: true
  # Uses all core features + all enriched features
```

**Result:** Detailed segments considering purchase patterns, department preferences, and product categories

## Feature Selection Guidelines

### When to Use Core Features Only
- ✅ General customer segmentation
- ✅ RFM-based analysis
- ✅ High-level strategic planning
- ✅ Cross-category business

### When to Add Department Features
- ✅ Multi-department retailers
- ✅ Understanding shopping patterns across categories
- ✅ Department-specific marketing campaigns
- ✅ Cross-selling opportunities

### When to Add Class Features
- ✅ Detailed product affinity analysis
- ✅ Fine-grained recommendation systems
- ✅ Product category optimization
- ✅ Inventory planning

### When to Add Size/Age Features
- ✅ Fashion/apparel retailers
- ✅ Family lifecycle segmentation
- ✅ Children's product targeting
- ✅ Size-based inventory planning

## Impact on Clustering

### More Features = More Dimensions

**Pros:**
- More detailed customer profiles
- Better capture of shopping preferences
- Improved personalization opportunities

**Cons:**
- Increased computational complexity
- Risk of overfitting
- More data required for stable results

### Recommended Approach

1. **Start Simple:** Use core features only
2. **Validate:** Check silhouette scores and business relevance
3. **Add Gradually:** Add enriched features one category at a time
4. **Compare:** Evaluate improvement in segmentation quality
5. **Optimize:** Remove features that don't improve results

## Feature Scaling

All features are automatically normalized (StandardScaler) before clustering to ensure:
- Equal weight for all features
- No domination by high-value features
- Proper distance calculations

## Output Columns Explained

### `fuzzy_cluster`
The primary cluster assignment (0 to n_clusters-1)

### `fuzzy_membership_cluster_0`, `fuzzy_membership_cluster_1`, etc.
The degree of membership (0.0 to 1.0) for each cluster.
- Higher values = stronger belonging to that cluster
- Sum of all memberships = 1.0 for each customer

### `fuzzy_distance_to_cluster_0`, `fuzzy_distance_to_cluster_1`, etc.
Euclidean distance from customer to each cluster center
- Lower values = closer to cluster center
- Useful for identifying boundary customers

## Python API Usage

```python
from customer_segmentation import FuzzyCustomerSegmentation, get_config

# Load configuration
config = get_config()

# Get fuzzy clustering parameters
fuzzy_config = config.fuzzy_clustering

# Create model with config
model = FuzzyCustomerSegmentation(
    n_clusters=fuzzy_config['n_clusters'],
    m=fuzzy_config['fuzziness_parameter'],
    seed=fuzzy_config['random_seed']
)

# Fit and predict
labels, membership = model.fit_predict(customer_data)

# Access output column names
cluster_col = fuzzy_config['output_columns']['cluster_label']
membership_prefix = fuzzy_config['output_columns']['membership_prefix']
```

## Neural Clustering Consistency

The same enriched features configuration is available for `neural_clustering` to ensure consistency across clustering methods:

```yaml
neural_clustering:
  use_enriched_features: false
  enriched_features_to_use:
    # Same as fuzzy clustering
```

## Best Practices

1. **Version Control:** Document which features were used for each model version
2. **A/B Testing:** Compare results with and without enriched features
3. **Business Validation:** Ensure segments make business sense
4. **Monitoring:** Track segment stability over time
5. **Documentation:** Record rationale for feature selection

## Troubleshooting

### Problem: Poor Silhouette Scores
**Solution:** Try different feature combinations or adjust n_clusters

### Problem: Segments Don't Make Business Sense
**Solution:** Reduce enriched features, focus on core RFM metrics

### Problem: Too Many Small Segments
**Solution:** Reduce n_clusters or use fewer features

### Problem: Segments Are Too Similar
**Solution:** Add enriched features to increase differentiation

---

**Last Updated:** October 16, 2025
**Configuration Version:** 0.1.0
