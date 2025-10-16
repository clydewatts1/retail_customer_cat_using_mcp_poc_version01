"""
Sample script to generate enriched customer sales data using RetailDataGenerator.
Uses configuration from config.yml for all parameters.
"""
import sys
import os
from pathlib import Path

# Add src directory to path to import project package
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from customer_segmentation import RetailDataGenerator, get_config
import pandas as pd

if __name__ == "__main__":
    # Load configuration
    config_path = Path(__file__).parent.parent / "config" / "config.yml"
    config = get_config(str(config_path))
    
    # Get parameters from config
    num_customers = config.data_generation['n_customers']
    seed = config.data_generation['random_seed']
    
    # Initialize generator with config seed and faker settings
    faker_cfg = config.data_generation.get('faker', {}) if isinstance(config.data_generation, dict) else {}
    generator = RetailDataGenerator(
        seed=seed,
        faker_enabled=faker_cfg.get('enabled', True),
        faker_locale=faker_cfg.get('locale', 'en_US')
    )
    
    # Generate data with configured number of customers
    df = generator.generate_customer_data(num_customers)
    
    # Build output path from config
    data_dir = Path(__file__).parent.parent / config.paths['data_dir']
    data_dir.mkdir(parents=True, exist_ok=True)
    output_path = data_dir / "customer_sales_data_enriched.csv"
    
    # Save data
    generator.save_data(df, str(output_path))
    
    print(f"Configuration loaded from: {config_path}")
    print(f"Generated {len(df)} customer records with {len(df.columns)} features")
    print(f"Saved to: {output_path}")
    print(f"\nEnriched features include:")
    print(f"  - Department totals: {len([col for col in df.columns if 'dept_total' in col])} columns")
    print(f"  - Class totals: {len([col for col in df.columns if 'class_total' in col])} columns")
    print(f"  - Size breakdowns: {len([col for col in df.columns if 'count_' in col])} columns")
