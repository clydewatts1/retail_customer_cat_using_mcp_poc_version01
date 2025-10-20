# Fix: visualize_segments.py Unpacking Error

## Issue
**Error:** `ValueError: too many values to unpack (expected 2)`  
**Location:** `visualize_segments.py`, line 291

```python
# This was incorrect:
customer_data_basic, customer_data_enriched = generator.generate_customer_data(
    n_customers=num_customers,
    dataset_type='both'
)
```

## Root Cause

The `generate_customer_data()` method with `dataset_type='both'` does NOT return a tuple of two DataFrames. Instead, it:
1. Saves the basic dataset to `data/customer_sales_data_basic.csv`
2. Returns only the enriched dataset

This is by design in the `RetailDataGenerator` implementation:

```python
# From src/customer_segmentation/data_generator.py, lines 445-459
if dataset_type == 'both':
    # Save basic dataset (clustering features only)
    basic_cols = ['customer_id', 'total_purchases', 'total_revenue', ...]
    dept_cols = [col for col in df.columns if col.startswith('dept_total_')]
    basic_cols.extend(dept_cols)
    
    basic_df = df[basic_cols].copy()
    basic_df.to_csv('data/customer_sales_data_basic.csv', index=False)
    print("✅ Basic dataset saved to data/customer_sales_data_basic.csv")
    
    # Return enriched dataset
    return df  # Returns single DataFrame, NOT a tuple!
```

## Solution

Updated `visualize_segments.py` to:
1. Accept only the enriched dataset from the return value
2. Read the basic dataset from the CSV file it was auto-saved to
3. Use both datasets for the appropriate tasks

### Fixed Code (Lines 290-307)

```python
# Generate both datasets
customer_data_enriched = generator.generate_customer_data(
    n_customers=num_customers,
    dataset_type='both'  # This saves basic dataset and returns enriched
)

# Save enriched dataset and load basic dataset
data_dir = Path(__file__).parent.parent / config.paths['data_dir']
data_dir.mkdir(parents=True, exist_ok=True)
basic_path = data_dir / "customer_sales_data_basic.csv"
enriched_data_path = data_dir / "customer_sales_data_enriched.csv"

# Read the basic dataset that was auto-saved
customer_data_basic = pd.read_csv(basic_path)

# Save enriched dataset
generator.save_data(customer_data_enriched, str(enriched_data_path))

print(f"Generated {len(customer_data_basic)} customer records")
print(f"  - Basic dataset: {len(customer_data_basic.columns)} features (for clustering)")
print(f"  - Enriched dataset: {len(customer_data_enriched.columns)} features (for visualization)")
```

## Correct Usage Patterns for generate_customer_data()

### Pattern 1: Generate BASIC dataset only
```python
basic_df = generator.generate_customer_data(
    n_customers=1000,
    dataset_type='basic'
)
# Returns: DataFrame with 51 columns
```

### Pattern 2: Generate ENRICHED dataset only
```python
enriched_df = generator.generate_customer_data(
    n_customers=1000,
    dataset_type='enriched'
)
# Returns: DataFrame with 757 columns
```

### Pattern 3: Generate BOTH datasets ⚠️ IMPORTANT
```python
# Method saves basic dataset and returns enriched
enriched_df = generator.generate_customer_data(
    n_customers=1000,
    dataset_type='both'
)
# Returns: DataFrame (enriched) - NOT a tuple!
# Side effect: Saves 'data/customer_sales_data_basic.csv'

# To get both DataFrames:
basic_df = pd.read_csv('data/customer_sales_data_basic.csv')
enriched_df = enriched_df  # Already have this from return
```

### Pattern 4: For run_segmentation_pipeline.py (correct usage)
```python
# Check if files exist first
if basic_data_path.exists() and enriched_data_path.exists():
    customer_data_basic = pd.read_csv(basic_data_path)
    customer_data_enriched = pd.read_csv(enriched_data_path)
else:
    # Generate new data
    customer_data_enriched = data_generator.generate_customer_data(
        n_customers=num_customers, 
        dataset_type='both'
    )
    data_generator.save_data(customer_data_enriched, str(enriched_data_path))
    customer_data_basic = pd.read_csv(basic_data_path)
```

## Why This Design?

The `dataset_type='both'` pattern auto-saves the basic dataset because:
1. **Performance:** Basic dataset is saved immediately to disk
2. **Memory:** Only one large DataFrame in memory at a time
3. **Convenience:** Most common workflow is to generate both and save both
4. **Compatibility:** The basic dataset path is consistent across all scripts

## Related Files

### Works Correctly (Already Fixed)
- ✅ `examples/run_segmentation_pipeline.py` - Uses the correct pattern
- ✅ `examples/generate_customer_data.py` - Uses the correct pattern
- ✅ `examples/test_persona_generation.py` - Uses separate calls

### Just Fixed
- ✅ `examples/visualize_segments.py` - Now uses the correct pattern

## Testing

Run the visualization script to verify the fix:
```bash
python examples/visualize_segments.py
```

Expected output:
```
✅ Basic dataset saved to data/customer_sales_data_basic.csv
Generated 500 customer records
  - Basic dataset: 51 features (for clustering)
  - Enriched dataset: 757 features (for visualization)
Creating visualizations...
✓ Saved: visualizations/cluster_distribution.png
...
```

---

**Fixed by:** AI Assistant  
**Date:** October 17, 2025  
**Status:** ✅ Resolved
