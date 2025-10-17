# Data Directory

This directory contains generated customer data and segmentation results.

## Dataset Types

### Basic Dataset: `customer_sales_data_basic.csv`
**51 columns** - Optimized for clustering algorithms

**Core RFM Metrics (8 columns):**
- `customer_id` - Unique customer identifier
- `total_purchases` - Total number of purchases
- `total_revenue` - Total revenue from customer
- `avg_order_value` - Average order value
- `recency_days` - Days since last purchase
- `frequency_per_month` - Purchase frequency per month
- `customer_lifetime_months` - Customer lifetime in months
- `return_rate` - Product return rate

**Department Summaries (42 columns):**
- `dept_total_value_<department>` - Total spend per department (21 columns)
- `dept_total_units_<department>` - Total units per department (21 columns)

**Departments:** Ladies Clothing, Uwear & Nwear, Accessories, Sports, Kids Clothing, Shoes, Kids Accessories, Nursery, Lingerie, Gifts, Mens Toiletries & Grooming, Beauty, Home, Xmas Shop, Ladies Toiletries & Cosmetics, Toys, Electricals, Babywear & Nursery Accessories, Menswear, Womens Clothing, Clothing & Footwear

**Ground Truth (1 column):**
- `true_segment` - True segment assignment for validation

### Enriched Dataset: `customer_sales_data_enriched.csv`
**757 columns** - Full customer profiles and detailed analytics

**All basic features (51 columns) PLUS:**

**Persona Information (1 column):**
- `persona_type` - Assigned persona (teenage_girl, young_woman_fashion, woman_with_baby, professional_woman, budget_shopper, etc.)

**Customer Profile (10 columns):**
- `first_name`, `last_name`, `email`, `phone`
- `address`, `city`, `state`, `zip_code`, `country`

**Class-Level Details (788 columns):**
- `class_total_value_<class>` - Total spend per product class (394 columns)
- `class_total_units_<class>` - Total units per product class (394 columns)

**Size/Age Breakdowns (8 columns):**
- `count_Baby`, `count_Child` - Baby/child item counts
- `count_size_*` - Size-specific counts (XXS, XS, S, M, L, XL, XXL)

## Persona Types

### 10 Customer Personas
1. **teenage_girl** (10%) - Fashion-focused teenager
2. **teenage_boy** (10%) - Sports & casual wear
3. **young_woman_fashion** (12%) - Trendy, high spender
4. **young_man_fashion** (10%) - Style-conscious
5. **woman_with_baby** (8%) - New mother focus
6. **woman_young_family** (12%) - Family shopper
7. **professional_woman** (10%) - Career wear
8. **professional_man** (10%) - Business attire
9. **budget_shopper** (10%) - Value-seeking
10. **mature_shopper** (8%) - Gift-focused

Each persona has weighted preferences across 21 departments and 394 product classes. See `config/personas.yml` for detailed specifications.

## Product Hierarchy

### 21 Departments → 394 Product Classes

**Top Departments by Class Count:**
- Ladies Clothing (43 classes)
- Uwear & Nwear (36 classes)
- Accessories (35 classes)
- Sports (34 classes)
- Kids Clothing (29 classes)
- Shoes (27 classes)
- Kids Accessories (23 classes)
- Nursery (22 classes)

Full hierarchy available in `hierarchy_parsed.yml`.

## Generated Files

When you run example scripts, the following files are created:

### Core Datasets
1. **customer_sales_data_basic.csv** - 51 columns for clustering
2. **customer_sales_data_enriched.csv** - 757 columns with full profiles

### Segmentation Results
3. **customers_with_segments.csv** - Customer data with cluster assignments (Fuzzy, Neural, GMM)
4. **customer_segments_for_ai.json** - Enriched segment profiles for AI agents

### Validation Datasets
5. **validation_1000_customers.csv** - Validated persona distribution dataset (1000 customers)
6. **test_basic.csv** - Test dataset (basic format)
7. **test_enriched.csv** - Test dataset (enriched format)

### Cluster Profiles (output/ directory)
- `fuzzy_cluster_profile_<timestamp>.json/yaml`
- `neural_cluster_profile_<timestamp>.json/yaml`
- `gmm_cluster_profile_<timestamp>.json/yaml`

## Generating Data

### Generate Both Datasets
```bash
python examples/generate_customer_data.py
```

### Generate in Python
```python
from customer_segmentation import RetailDataGenerator

generator = RetailDataGenerator(config_path='config/config.yml')

# Both datasets
basic_df, enriched_df = generator.generate_customer_data(
    num_customers=1000, 
    dataset_type='both'
)

# Just basic
basic_df = generator.generate_customer_data(
    num_customers=1000, 
    dataset_type='basic'
)

# Just enriched
enriched_df = generator.generate_customer_data(
    num_customers=1000, 
    dataset_type='enriched'
)
```

## Note

Generated files are not tracked in version control. Run example scripts to create them:

```bash
# Generate data
python examples/generate_customer_data.py

# Run full pipeline
python examples/run_segmentation_pipeline.py

# Validate persona distribution
python examples/validate_persona_distribution.py
```
