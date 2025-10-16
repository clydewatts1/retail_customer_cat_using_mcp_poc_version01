# Data Directory

This directory contains generated customer data and segmentation results.

## Generated Files

When you run `examples/run_segmentation_pipeline.py`, the following files are created:

1. **customer_sales_data.csv** - Synthetic customer sales data with features
2. **customers_with_segments.csv** - Customer data enriched with cluster assignments
3. **customer_segments_for_ai.json** - Enriched segment profiles for AI agent consumption

## Note

These files are generated dynamically and are not tracked in version control. 
Run the example script to generate them:

```bash
cd examples
python run_segmentation_pipeline.py
```
