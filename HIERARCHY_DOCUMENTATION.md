# Product Hierarchy: Department-Class Relationship

## Overview
The retail customer segmentation system now properly models the hierarchical relationship between departments and classes, where **classes belong to departments**.

## Hierarchical Structure

### Departments and Their Classes

```yaml
Accessories & Footwear:
  - Bags & Wallets
  - Soft & Hard Accessories

Health & Wellness:
  - Consumables
  - Personal Care

Home & Lifestyle:
  - Bedding
```

## Data Generation Logic

When generating synthetic customer purchase data, the system now:

1. **Selects a department first** (e.g., "Health & Wellness")
2. **Then selects a class within that department** (e.g., "Consumables" or "Personal Care")
3. **Records the purchase value** in both the department total and the specific class total

This ensures data integrity where:
- **Department totals = Sum of their class totals**
- Each purchase is consistently attributed to both the parent department and specific class

## Example Purchase Flow

```
Purchase #1: $50.00
├─ Department: "Accessories & Footwear" (+$50)
└─ Class: "Bags & Wallets" (+$50)

Purchase #2: $75.00
├─ Department: "Health & Wellness" (+$75)
└─ Class: "Consumables" (+$75)

Purchase #3: $30.00
├─ Department: "Accessories & Footwear" (+$30)
└─ Class: "Soft & Hard Accessories" (+$30)
```

**Result for this customer:**
- Accessories & Footwear total: $80 = Bags & Wallets ($50) + Soft & Hard Accessories ($30) ✓
- Health & Wellness total: $75 = Consumables ($75) ✓

## Configuration

### YAML Format (config/config.yml)

```yaml
data_generation:
  # Product hierarchy - classes belong to departments
  departments:
    "Accessories & Footwear":
      classes:
        - "Bags & Wallets"
        - "Soft & Hard Accessories"
    "Health & Wellness":
      classes:
        - "Consumables"
        - "Personal Care"
    "Home & Lifestyle":
      classes:
        - "Bedding"
```

### Accessing in Code

```python
from customer_segmentation import get_config

config = get_config()

# Get all departments
departments = config.departments
# ['Accessories & Footwear', 'Health & Wellness', 'Home & Lifestyle']

# Get all classes (flattened)
all_classes = config.classes
# ['Bags & Wallets', 'Soft & Hard Accessories', 'Consumables', 'Personal Care', 'Bedding']

# Get classes for a specific department
accessories_classes = config.get_classes_for_department("Accessories & Footwear")
# ['Bags & Wallets', 'Soft & Hard Accessories']
```

## Generated Data Columns

Each customer record includes:

### Department-Level Columns
- `dept_total_value_Accessories & Footwear` - Total spend in this department
- `dept_total_value_Health & Wellness`
- `dept_total_value_Home & Lifestyle`
- `dept_total_units_Accessories & Footwear` - Total units purchased
- `dept_total_units_Health & Wellness`
- `dept_total_units_Home & Lifestyle`

### Class-Level Columns (within their parent departments)
- `class_total_value_Bags & Wallets` (→ Accessories & Footwear)
- `class_total_value_Soft & Hard Accessories` (→ Accessories & Footwear)
- `class_total_value_Consumables` (→ Health & Wellness)
- `class_total_value_Personal Care` (→ Health & Wellness)
- `class_total_value_Bedding` (→ Home & Lifestyle)
- Plus corresponding `class_total_units_*` columns

## Data Integrity Validation

The system ensures:

✅ **Hierarchical Consistency**: `dept_total = sum(classes_in_dept)`

✅ **No Orphan Classes**: Every class belongs to exactly one department

✅ **Complete Coverage**: All purchases are attributed to both department and class

## Benefits

1. **Realistic Modeling**: Mirrors actual retail product hierarchies
2. **Analytical Accuracy**: Department-level analysis automatically includes all child classes
3. **Segmentation Insights**: Can analyze customer preferences at both department and class granularity
4. **Scalability**: Easy to add new classes to existing departments or create new departments

## Use Cases

### Department-Level Analysis
```python
# Which department is most popular with VIP customers?
vip_data = customers[customers['segment_name'] == 'VIP Champions']
dept_cols = [col for col in vip_data.columns if 'dept_total_value_' in col]
avg_dept_spend = vip_data[dept_cols].mean()
```

### Class-Level Analysis
```python
# Which specific classes drive Health & Wellness spend?
hw_classes = ['Consumables', 'Personal Care']
class_cols = [f'class_total_value_{c}' for c in hw_classes]
class_breakdown = customers[class_cols].sum()
```

### Hierarchy-Aware Recommendations
```python
# Customer bought heavily in "Consumables" → Recommend other Health & Wellness classes
if customer['class_total_value_Consumables'] > threshold:
    recommend_classes = config.get_classes_for_department("Health & Wellness")
    # Returns: ['Consumables', 'Personal Care']
```

## Migration from Flat Structure

The config_loader supports both formats:

**Old Format** (flat list):
```yaml
departments:
  - "Accessories & Footwear"
  - "Health & Wellness"
classes:
  - "Bags & Wallets"
  - "Consumables"
```

**New Format** (hierarchical):
```yaml
departments:
  "Accessories & Footwear":
    classes:
      - "Bags & Wallets"
```

The system automatically detects the format and provides a consistent API.

## Testing

All tests pass with the hierarchical structure:
- ✅ Data generation creates valid hierarchy
- ✅ Config loader handles both old and new formats
- ✅ Department totals equal sum of class totals
- ✅ Clustering algorithms work with enriched hierarchical data

---

**Updated:** October 16, 2025
**Status:** ✅ Implemented and Validated
