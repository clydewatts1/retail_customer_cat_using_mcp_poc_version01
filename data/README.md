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
```
