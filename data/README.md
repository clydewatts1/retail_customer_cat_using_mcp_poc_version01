# Data Directory

This directory contains all data files for the Retail Customer Categorization project.

## Structure

- **raw/**: Store raw, immutable data dumps here. Never modify files in this directory.
- **processed/**: Store cleaned and processed data ready for analysis and modeling.
- **external/**: Store external data sources or third-party datasets.

## Data Guidelines

1. **Never commit large data files to git**
   - Use `.gitignore` to exclude data files
   - Consider using Git LFS for large files if necessary
   - Use data version control tools like DVC for data versioning

2. **Document your data**
   - Add README files in subdirectories describing the data
   - Include data dictionaries and metadata
   - Document data sources and collection dates

3. **Keep raw data immutable**
   - Never modify files in the `raw/` directory
   - All transformations should create new files in `processed/`
   - Keep a record of all data processing steps

## Example Data Files

Place your customer data CSV, Excel, or other format files here:

```
data/
├── raw/
│   ├── customers.csv
│   ├── transactions.csv
│   └── products.csv
├── processed/
│   ├── customers_cleaned.csv
│   └── customer_features.csv
└── external/
    └── demographic_data.csv
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
