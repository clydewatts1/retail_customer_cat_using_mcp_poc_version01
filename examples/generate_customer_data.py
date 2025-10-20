"""
Sample script to generate customer sales data using RetailDataGenerator.
Uses configuration from config.yml for all parameters.

NEW FEATURES:
- Persona-based customer generation with 10 realistic customer types
- Full 21-department, 394-class product hierarchy
- Dual dataset generation: basic (clustering) + enriched (analysis)
"""
import sys
import os
from pathlib import Path

# Add src directory to path to import project package
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from customer_segmentation import RetailDataGenerator, get_config
import pandas as pd

if __name__ == "__main__":
    print("=" * 70)
    print("RETAIL CUSTOMER DATA GENERATOR - Enhanced with Personas")
    print("=" * 70)
    
    # Load configuration
    config_path = Path(__file__).parent.parent / "config" / "config.yml"
    config = get_config(str(config_path))
    
    # Get parameters from config
    data_gen_config = config.data_generation
    num_customers = data_gen_config.get('n_customers', 10000)
    seed = data_gen_config['random_seed']
    
    # Get persona and hierarchy paths from config
    use_personas = data_gen_config.get('use_personas', True)
    personas_path = data_gen_config.get('personas_config_file', 'config/personas.yml')
    hierarchy_path = data_gen_config.get('hierarchy_config_file', 'hierarchy_parsed.yml')
    generate_dual = data_gen_config.get('generate_dual_datasets', True)
    # Always use enriched features for clustering (per config)
    use_enriched_features = config.fuzzy_clustering.get('use_enriched_features', True)
    
    # Initialize generator with persona support
    faker_cfg = data_gen_config.get('faker', {})
    
    print(f"\nConfiguration:")
    print(f"  - Config file: {config_path}")
    print(f"  - Customers to generate: {num_customers}")
    print(f"  - Random seed: {seed}")
    print(f"  - Use personas: {use_personas}")
    print(f"  - Generate dual datasets: {generate_dual}")
    print(f"  - Faker enabled: {faker_cfg.get('enabled', True)}")
    
    generator = RetailDataGenerator(
        seed=seed,
        faker_enabled=faker_cfg.get('enabled', True),
        faker_locale=faker_cfg.get('locale', 'en_US'),
        use_personas=use_personas,
        personas_config_path=personas_path,
        hierarchy_config_path=hierarchy_path
    )
    
    # Display loaded configuration
    if generator.use_personas and generator.personas:
        print(f"\n✅ Persona System Loaded:")
        print(f"  - Number of personas: {len(generator.personas)}")
        print(f"  - Personas: {', '.join(generator.personas.keys())}")
        print(f"  - Departments in hierarchy: {len(generator.hierarchy)}")
        print(f"  - Total classes: {sum(len(classes) for classes in generator.hierarchy.values())}")
    else:
        print(f"\n⚠️  Using legacy 4-segment mode (backwards compatibility)")
    
    # Build output paths
    data_dir = Path(__file__).parent.parent / config.paths['data_dir']
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Always generate enriched dataset for clustering, optionally dual for analysis
    if generate_dual:
        print(f"\n{'='*70}")
        print("Generating DUAL DATASETS (Basic + Enriched)")
        print(f"{'='*70}")
        # Always use enriched features for clustering, but generate both datasets for analysis
        enriched_df = generator.generate_customer_data(num_customers, dataset_type='both' if use_enriched_features else 'basic')
        # Basic dataset saved automatically, enriched returned
        basic_path = data_dir / Path(data_gen_config.get('basic_dataset_path', 'customer_sales_data_basic.csv')).name
        enriched_path = data_dir / Path(data_gen_config.get('enriched_dataset_path', 'customer_sales_data_enriched.csv')).name
        # Save enriched dataset
        generator.save_data(enriched_df, str(enriched_path))
        # Load basic dataset to display stats (if exists)
        if basic_path.exists():
            basic_df = pd.read_csv(basic_path)
        else:
            basic_df = None
        print(f"\n📊 BASIC DATASET (for clustering):")
        print(f"  - Path: {basic_path}")
        if basic_df is not None:
            print(f"  - Customers: {len(basic_df)}")
            print(f"  - Features: {len(basic_df.columns)}")
            print(f"  - Columns: {', '.join(basic_df.columns[:10])}...")
        else:
            print("  - Not generated (enriched only mode)")
        print(f"\n📊 ENRICHED DATASET (for analysis):")
        print(f"  - Path: {enriched_path}")
        print(f"  - Customers: {len(enriched_df)}")
        print(f"  - Features: {len(enriched_df.columns)}")
        if 'persona_type' in enriched_df.columns:
            print(f"\n📈 Persona Distribution:")
            persona_counts = enriched_df['persona_type'].value_counts()
            for persona, count in persona_counts.sort_index().items():
                pct = (count / len(enriched_df)) * 100
                print(f"  {persona:30s}: {count:3d} ({pct:5.1f}%)")
        # Show department breakdown
        dept_cols = [col for col in enriched_df.columns if col.startswith('dept_total_value_')]
        if dept_cols:
            print(f"\n💰 Top 5 Departments by Total Value:")
            dept_totals = enriched_df[dept_cols].sum().sort_values(ascending=False).head(5)
            for dept_col, total in dept_totals.items():
                dept_name = dept_col.replace('dept_total_value_', '')
                print(f"  {dept_name:40s}: ${total:,.2f}")
        # Show basic statistics
        print(f"\n📊 RFM Statistics (from enriched dataset):")
        rfm_cols = ['total_revenue', 'recency_days', 'frequency_per_month']
        rfm_stats = enriched_df[rfm_cols].describe()
        print(rfm_stats.to_string())
        
    else:
        # Always use enriched features for clustering
        print(f"\n{'='*70}")
        print("Generating ENRICHED DATASET ONLY (enriched features required for clustering)")
        print(f"{'='*70}")
        enriched_df = generator.generate_customer_data(num_customers, dataset_type='enriched')
        enriched_path = data_dir / Path(data_gen_config.get('enriched_dataset_path', 'customer_sales_data_enriched.csv')).name
        generator.save_data(enriched_df, str(enriched_path))
        print(f"\n📊 ENRICHED DATASET:")
        print(f"  - Path: {enriched_path}")
        print(f"  - Customers: {len(enriched_df)}")
        print(f"  - Features: {len(enriched_df.columns)}")
        print(f"\nFeature breakdown:")
        print(f"  - Department totals: {len([col for col in enriched_df.columns if 'dept_total' in col])} columns")
        print(f"  - Class totals: {len([col for col in enriched_df.columns if 'class_total' in col])} columns")
        print(f"  - Size breakdowns: {len([col for col in enriched_df.columns if 'count_' in col])} columns")
    
    print(f"\n{'='*70}")
    print("✅ DATA GENERATION COMPLETE!")
    print(f"{'='*70}")

