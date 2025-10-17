# Testing Guide - Retail Customer Segmentation POC

## Date: October 17, 2025
## Branch: CHANGES_03_ENHANCE_SAMPLE_GENERATION

---

## Quick Start

### Option 1: Run Batch Script (Recommended)
```cmd
QUICK_TEST.bat          # Fast validation (3 tests, ~30 seconds)
RUN_ALL_TESTS.bat       # Full test suite (7 tests, ~5 minutes)
```

### Option 2: Manual Testing
Open a terminal with Python available and run:

```cmd
cd c:\projects\retail_clustering_poc\retail_customer_cat_using_mcp_poc
python examples\test_config.py
python examples\test_persona_generation.py
python examples\validate_persona_distribution.py
python examples\generate_customer_data.py
python examples\run_gmm_clustering.py
python examples\run_segmentation_pipeline.py
python examples\visualize_segments.py
```

---

## Test Suite Overview

### 1. Configuration Test (`test_config.py`)
**Purpose:** Validate config.yml loads correctly and has all required settings
**Expected Output:**
- ✓ Config loaded successfully
- ✓ All paths defined
- ✓ Persona config available
- ✓ Clustering parameters set
- ✓ No legacy segment settings used

**Status:** Should PASS after legacy removal

---

### 2. Persona Generation Test (`test_persona_generation.py`)
**Purpose:** Verify persona-based customer generation works
**Expected Output:**
- ✓ Generates 100 test customers
- ✓ All 10 personas represented
- ✓ Persona-specific behavior patterns present
- ✓ Department preferences align with personas
- ✓ Faker fields populated (name, email, address, etc.)

**Status:** Should PASS

---

### 3. Persona Distribution Validation (`validate_persona_distribution.py`)
**Purpose:** Validate 1000-customer dataset has proper persona distribution
**Expected Output:**
- ✓ All personas present
- ✓ Reasonable distribution across personas
- ✓ Department spending patterns match persona profiles
- ✓ Statistical validation passes

**Status:** Should PASS

---

### 4. Customer Data Generation (`generate_customer_data.py`)
**Purpose:** Generate dual datasets (basic + enriched)
**Expected Output:**
- ✓ Creates `data/customer_sales_data_basic.csv` (51 columns)
- ✓ Creates `data/customer_sales_data_enriched.csv` (757 columns)
- ✓ All 21 departments included
- ✓ All 394 classes included
- ✓ Size/age breakdowns present

**Status:** Should PASS

---

### 5. GMM Clustering (`run_gmm_clustering.py`)
**Purpose:** Test Gaussian Mixture Model clustering
**Expected Output:**
- ✓ Clusters 500 customers into 4 segments
- ✓ Calculates silhouette score
- ✓ Generates cluster centers
- ✓ Exports cluster profile JSON

**Status:** Should PASS

---

### 6. Full Segmentation Pipeline (`run_segmentation_pipeline.py`)
**Purpose:** Run all 3 clustering methods (Fuzzy, Neural, GMM)
**Expected Output:**
- ✓ Fuzzy C-Means clustering completed
- ✓ Neural Network clustering completed
- ✓ GMM clustering completed
- ✓ All cluster profiles exported
- ✓ Metrics comparison table displayed
- ✓ Customer data with segments saved

**Status:** Should PASS

---

### 7. Visualization Generation (`visualize_segments.py`)
**Purpose:** Generate all visualization plots
**Expected Output:**
- ✓ `visualizations/cluster_distribution.png`
- ✓ `visualizations/segment_characteristics.png`
- ✓ `visualizations/rfm_scatter.png`
- ✓ `visualizations/membership_heatmap.png`
- ✓ `visualizations/department_preferences.png`
- ✓ `visualizations/size_distribution.png`
- ✓ `visualizations/persona_type_by_cluster.png` (NEW)

**Status:** Should PASS

---

## Key Changes from Legacy System

### ✅ Removed:
- `use_legacy_segments` flag
- `segment_probabilities` (4 hardcoded segments)
- `segments` definitions (high_value_frequent, etc.)
- `departments_legacy` (simple 3-department hierarchy)

### ✅ Now Using:
- 10 persona types from `config/personas.yml`
- Full 21-department, 394-class product hierarchy
- Dual dataset architecture (basic for clustering, enriched for analysis)
- Faker integration for realistic customer profiles

---

## Expected Final Outputs

### Data Files
```
data/
  ├── customer_sales_data_basic.csv          (500 rows, 51 cols)
  ├── customer_sales_data_enriched.csv       (500 rows, 757 cols)
  ├── customers_with_segments.csv            (500 rows + cluster cols)
  └── output/
      ├── fuzzy_cluster_profile_*.json
      ├── neural_cluster_profile_*.json
      └── gmm_cluster_profile_*.json
```

### Visualizations
```
visualizations/
  ├── cluster_distribution.png
  ├── segment_characteristics.png
  ├── rfm_scatter.png
  ├── membership_heatmap.png
  ├── department_preferences.png
  ├── size_distribution.png
  └── persona_type_by_cluster.png           (NEW)
```

---

## Troubleshooting

### Issue: "python not found"
**Solution:** Make sure you run from a terminal with Python in PATH, or use the Python terminal in VS Code

### Issue: "Config file not found"
**Solution:** Ensure you're running from the project root directory

### Issue: "Module not found"
**Solution:** Install requirements:
```cmd
pip install -r requirements.txt
```

### Issue: "KeyError" in clustering
**Solution:** Make sure legacy config has been removed from config.yml

---

## Success Criteria

All tests should pass with:
- ✓ No errors or exceptions
- ✓ All expected output files created
- ✓ All visualizations generated
- ✓ Cluster profiles exported
- ✓ Persona distribution validated

---

## Next Steps After Testing

1. Review generated visualizations in `visualizations/` folder
2. Examine cluster profiles in `data/output/` folder
3. Analyze customer segments in `customers_with_segments.csv`
4. Review persona distribution in validation output
5. Compare clustering methods using metrics table

---

## Manual Verification Checklist

- [ ] Config loads without errors
- [ ] All 10 personas generate customers
- [ ] Dual datasets created with correct column counts
- [ ] All 3 clustering methods complete successfully
- [ ] All 7 visualizations created
- [ ] Cluster profiles exported to JSON
- [ ] No legacy segment references in any output
- [ ] Persona types appear in enriched dataset
- [ ] Department preferences align with persona definitions
- [ ] New persona_type_by_cluster plot shows all personas

---

**Test Status:** Ready to run
**Configuration:** Cleaned (legacy removed)
**Branch:** CHANGES_03_ENHANCE_SAMPLE_GENERATION
