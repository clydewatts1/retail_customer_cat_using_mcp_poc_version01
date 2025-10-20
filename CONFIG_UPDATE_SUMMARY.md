# Configuration Update Summary

## Date: October 17, 2025
## Purpose: Update config.yml to reflect new dual-dataset customer data format

---

## Key Changes Made

### 1. Source Data Files
**Updated:**
```yaml
source_data:
  product_hierarchy: "data/product_hierarchy.csv"
  customer_sales_basic: "data/customer_sales_data_basic.csv"      # NEW
  customer_sales_enriched: "data/customer_sales_data_enriched.csv"
  # REMOVED: customer_sales_legacy: "data/customer_sales_data.csv"
```

### 2. Visualization Outputs
**Added:**
```yaml
persona_type_by_cluster: "visualizations/persona_type_by_cluster.png"
```

### 3. Core Customer Features
**Added Persona and Faker Fields:**
- `persona_type`: Customer persona (10 types)
- `signup_date`: Customer registration date
- `first_name`, `last_name`: Faker-generated names
- `email`, `phone`: Faker-generated contact info
- `address`, `city`, `state`, `zip_code`, `country`: Faker-generated location

### 4. Department Features (21 Departments)
**Updated from 3 simplified departments to full 21-department hierarchy:**
```yaml
departments:
  - "Accessories"
  - "Bag Levy"
  - "Concessions"
  - "Dummy"
  - "Dummy Dept for TBC order"
  - "Gift Cards"
  - "Goods Not For Resale"
  - "Health & Beauty"
  - "Home"
  - "In-Store Charity"
  - "Kids Accessories"
  - "Kids Clothing"
  - "Ladies Clothing"
  - "Ladies Footwear"
  - "Ladies Hosiery"
  - "Mens Accessories"
  - "Mens Clothing"
  - "Primarket"
  - "Sports Shop"
  - "Uwear & Nwear"
  - "Xmas Shop"
```

**Removed Legacy:**
```yaml
# OLD (removed):
- "Accessories & Footwear"
- "Health & Wellness"
- "Home & Lifestyle"
```

### 5. Class Features (394 Classes)
**Updated to reference full hierarchy:**
```yaml
class_features:
  pattern: "class_total_value_{class_name}"
  type: "float"
  description: "Total value of purchases in this class (394 total classes)"
  note: "All 394 classes from hierarchy_parsed.yml are included in enriched dataset"
```

**Removed Legacy:**
```yaml
# OLD (removed):
classes:
  - "Bags & Wallets"
  - "Soft & Hard Accessories"
  - "Consumables"
  - "Personal Care"
  - "Bedding"
```

### 6. Dataset Format Documentation
**Added detailed dataset structure info:**
```yaml
# BASIC DATASET (51 columns):
#   - Core RFM features
#   - 21 dept_total_value columns
#   - 21 dept_total_units columns
#   - Size/age counts
#   - Used for: Clustering algorithms

# ENRICHED DATASET (757 columns):
#   - All BASIC columns PLUS:
#   - Persona & Faker fields
#   - 394 class_total_value columns
#   - 394 class_total_units columns
#   - Used for: Visualization, analysis
```

### 7. Clustering Configuration
**Simplified and clarified:**
- Removed `enriched_features_to_use` list (with old simplified names)
- Set `use_enriched_features: false` 
- Added clear notes that clustering uses BASIC dataset (51 cols)
- Enriched dataset (757 cols) used only for visualization

**Both Fuzzy and Neural clustering now specify:**
```yaml
# Feature selection for clustering (uses BASIC dataset - 51 columns)
features_to_use:
  - "total_purchases"
  - "total_revenue"
  - "avg_order_value"
  - "recency_days"
  - "frequency_per_month"
  - "customer_lifetime_months"
  - "return_rate"

# Note: Clustering uses basic dataset (51 cols) for performance
# Enriched dataset (757 cols) used for visualization and analysis only
use_enriched_features: false
```

---

## Removed Legacy Elements

### From Data Generation:
- ❌ `use_legacy_segments` flag
- ❌ `segment_probabilities` (4 hardcoded segments)
- ❌ `segments` definitions (high_value_frequent, medium_value_regular, etc.)
- ❌ `departments_legacy` (simple 3-department hierarchy)

### From Clustering Config:
- ❌ `enriched_features_to_use` with old simplified department/class names
- ❌ References to "Accessories & Footwear", "Health & Wellness", "Home & Lifestyle"

---

## Data Architecture

### Dual Dataset System

```
┌─────────────────────────────────────────────────────┐
│         Data Generation (Persona-Based)             │
│         RetailDataGenerator                         │
└──────────────────┬──────────────────────────────────┘
                   │
         ┌─────────┴─────────┐
         ▼                   ▼
┌────────────────┐   ┌───────────────────┐
│ BASIC DATASET  │   │ ENRICHED DATASET  │
│   51 columns   │   │   757 columns     │
├────────────────┤   ├───────────────────┤
│ • RFM features │   │ • All BASIC cols  │
│ • 21 dept vals │   │ • Persona info    │
│ • 21 dept units│   │ • 394 class vals  │
│ • Size/age     │   │ • 394 class units │
└────────┬───────┘   │ • Faker profiles  │
         │           └─────────┬─────────┘
         │                     │
         ▼                     ▼
┌────────────────┐   ┌───────────────────┐
│  CLUSTERING    │   │  VISUALIZATION    │
│   (Fuzzy,      │   │   (All plots,     │
│   Neural, GMM) │   │   analysis,       │
│                │   │   reporting)      │
└────────────────┘   └───────────────────┘
```

### Column Breakdown

**BASIC (51 columns):**
- Core: 9 columns (customer_id, total_purchases, total_revenue, avg_order_value, recency_days, frequency_per_month, customer_lifetime_months, return_rate, true_segment)
- Department values: 21 columns (dept_total_value_*)
- Department units: 21 columns (dept_total_units_*)

**ENRICHED (757 columns):**
- All BASIC: 51 columns
- Persona/profile: 11 columns (persona_type, signup_date, first_name, last_name, email, phone, address, city, state, zip_code, country)
- Class values: 394 columns (class_total_value_*)
- Class units: 394 columns (class_total_units_*)
- Size/age: 7 columns (count_Baby, count_Child, count_size_XS/S/M/L/XL)

**Total: 51 + 11 + 394 + 394 + 7 = 857** (some overlap with basic, net 757 unique)

---

## Persona System

### 10 Persona Types (from personas.yml):
1. `professional_woman` - Career-focused women shoppers
2. `professional_man` - Career-focused men shoppers
3. `woman_young_family` - Mothers with young children
4. `man_young_family` - Fathers with young children
5. `young_woman_fashion` - Fashion-conscious young women
6. `young_man_fashion` - Fashion-conscious young men
7. `teenage_girl` - Teen female shoppers
8. `teenage_boy` - Teen male shoppers
9. `mature_shopper` - Older demographic shoppers
10. `budget_shopper` - Price-conscious shoppers

Each persona has:
- Unique shopping patterns
- Department preferences
- Age/size distributions
- Purchase frequency and value ranges

---

## Configuration Best Practices

### For Clustering:
- ✅ Use BASIC dataset (51 columns)
- ✅ Core RFM features only
- ✅ Fast, clean, focused on behavior
- ✅ Set `use_enriched_features: false`

### For Visualization:
- ✅ Use ENRICHED dataset (757 columns)
- ✅ Access to all department and class details
- ✅ Persona type for segmentation analysis
- ✅ Faker fields for realistic reports

### For Analysis:
- ✅ Use ENRICHED dataset
- ✅ Deep dive into product preferences
- ✅ Cross-reference persona types with clusters
- ✅ Export detailed customer profiles

---

## Testing After Configuration Update

Run the test suite to validate:
```cmd
QUICK_TEST.bat        # Fast validation
RUN_ALL_TESTS.bat     # Full suite
```

All tests should pass with:
- ✅ No errors loading config
- ✅ All 10 personas generate correctly
- ✅ Both datasets created with correct column counts
- ✅ All clustering methods work
- ✅ All visualizations generate (including new persona plot)
- ✅ No legacy references in any output

---

## Migration Notes

### From Legacy System:
**Before:**
- 4 hardcoded segments (high_value_frequent, etc.)
- 3 simplified departments
- ~100 columns total
- Segment-based generation

**After:**
- 10 dynamic personas
- 21 real departments, 394 real classes
- 51 basic / 757 enriched columns
- Persona-based generation
- Dual dataset architecture

### Breaking Changes:
None for clustering code (still uses same 7 core features), but:
- Configuration structure updated
- Department names changed (real names vs. simplified)
- New persona_type field in enriched data
- Legacy segment config removed

---

## Status

✅ Configuration updated
✅ Legacy elements removed
✅ Dataset format documented
✅ Clustering config simplified
✅ Persona system integrated
✅ Ready for testing

---

**Next Steps:**
1. Run QUICK_TEST.bat to validate config
2. Review generated datasets for correct column counts
3. Verify clustering uses basic dataset
4. Check visualizations use enriched dataset
5. Confirm persona_type_by_cluster plot generates
