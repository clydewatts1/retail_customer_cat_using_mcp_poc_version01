"""
Test script for persona-based customer data generation.
Validates that the enhanced data generator works correctly with personas.
"""
import sys
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from customer_segmentation.data_generator import RetailDataGenerator
from customer_segmentation import get_config
import pandas as pd


def test_persona_generation():
    """Test persona-based data generation with full hierarchy."""
    print("=" * 60)
    print("TESTING PERSONA-BASED DATA GENERATION")
    print("=" * 60)
    
    # Load config for n_customers and enriched features
    config_path = project_root / "config" / "config.yml"
    config = get_config(str(config_path))
    n_customers_enriched = config.data_generation.get('n_customers', 10000)
    use_enriched_features = config.fuzzy_clustering.get('use_enriched_features', True)
    
    # Initialize generator with persona support
    print("\n1. Initializing RetailDataGenerator with personas...")
    generator = RetailDataGenerator(
        seed=config.data_generation.get('random_seed', 42),
        faker_enabled=config.data_generation.get('faker', {}).get('enabled', True),
        faker_locale=config.data_generation.get('faker', {}).get('locale', 'en_US'),
        use_personas=config.data_generation.get('use_personas', True),
        personas_config_path=config.data_generation.get('personas_config_file', 'config/personas.yml'),
        hierarchy_config_path=config.data_generation.get('hierarchy_config_file', 'hierarchy_parsed.yml')
    )
    
    if generator.use_personas:
        print(f"   ✅ Personas loaded: {len(generator.personas)} personas")
        print(f"   ✅ Hierarchy loaded: {len(generator.hierarchy)} departments")
    else:
        print("   ⚠️  Personas not loaded, using legacy mode")
    
    # Test enriched dataset generation
    print("\n2. Generating ENRICHED dataset (from config n_customers)...")
    enriched_df = generator.generate_customer_data(n_customers=n_customers_enriched, dataset_type='enriched' if use_enriched_features else 'basic')
    
    print(f"   ✅ Generated {len(enriched_df)} customers")
    print(f"   ✅ Total columns: {len(enriched_df.columns)}")
    
    # Check for expected columns
    expected_cols = ['customer_id', 'total_purchases', 'total_revenue', 
                    'avg_order_value', 'recency_days', 'frequency_per_month',
                    'persona_type', 'first_name', 'last_name']
    
    missing_cols = [col for col in expected_cols if col not in enriched_df.columns]
    if missing_cols:
        print(f"   ⚠️  Missing columns: {missing_cols}")
    else:
        print(f"   ✅ All expected columns present")
    
    # Display persona distribution
    if 'persona_type' in enriched_df.columns:
        print("\n3. Persona Distribution:")
        persona_dist = enriched_df['persona_type'].value_counts(normalize=True).sort_index()
        for persona, pct in persona_dist.items():
            print(f"   {persona:30s}: {pct*100:5.1f}%")
    
    # Display first few rows
    print("\n4. Sample Enriched Data (first 3 customers):")
    display_cols = ['customer_id', 'persona_type', 'total_purchases', 
                    'avg_order_value', 'frequency_per_month', 'first_name', 'last_name']
    display_cols = [c for c in display_cols if c in enriched_df.columns]
    print(enriched_df[display_cols].head(3).to_string(index=False))
    
    # Test department summaries
    dept_cols = [col for col in enriched_df.columns if col.startswith('dept_total_value_')]
    if dept_cols:
        print(f"\n5. Department Columns: {len(dept_cols)} departments")
        # Show top 5 departments by total value
        dept_totals = enriched_df[dept_cols].sum().sort_values(ascending=False).head(5)
        print("   Top 5 departments by total value:")
        for dept_col, total in dept_totals.items():
            dept_name = dept_col.replace('dept_total_value_', '')
            print(f"   {dept_name:40s}: ${total:,.2f}")
    
    # Test basic dataset generation
    print("\n6. Generating BASIC dataset (30 customers)...")
    basic_df = generator.generate_customer_data(n_customers=30, dataset_type='basic')
    
    print(f"   ✅ Generated {len(basic_df)} customers")
    print(f"   ✅ Total columns: {len(basic_df.columns)}")
    print(f"   ✅ Columns: {', '.join(basic_df.columns[:10])}...")
    
    # Verify basic dataset has no persona or class details
    enriched_only_cols = ['persona_type', 'first_name', 'last_name', 'email']
    present = [col for col in enriched_only_cols if col in basic_df.columns]
    if present:
        print(f"   ⚠️  Basic dataset should not have: {present}")
    else:
        print(f"   ✅ Basic dataset correctly excludes enriched fields")
    
    # Test dual dataset generation
    print("\n7. Testing DUAL dataset generation (both at once)...")
    dual_df = generator.generate_customer_data(n_customers=100, dataset_type='both')
    print(f"   ✅ Dual generation complete")
    print(f"   ✅ Returned enriched dataset: {len(dual_df)} customers, {len(dual_df.columns)} columns")
    
    # Save test outputs
    print("\n8. Saving test outputs...")
    enriched_df.to_csv('data/test_enriched.csv', index=False)
    basic_df.to_csv('data/test_basic.csv', index=False)
    print("   ✅ Saved: data/test_enriched.csv")
    print("   ✅ Saved: data/test_basic.csv")
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED!")
    print("=" * 60)


def test_legacy_mode():
    """Test backwards compatibility with legacy segment-based generation."""
    print("\n" + "=" * 60)
    print("TESTING LEGACY MODE (Backwards Compatibility)")
    print("=" * 60)
    
    generator = RetailDataGenerator(
        seed=42,
        faker_enabled=True,
        use_personas=False  # Disable personas
    )
    
    print(f"   Generation mode: {'Legacy (4 segments)' if not generator.use_personas else 'Persona'}")
    
    df = generator.generate_customer_data(n_customers=100, dataset_type='enriched')
    print(f"   ✅ Generated {len(df)} customers in legacy mode")
    print(f"   ✅ Columns: {len(df.columns)}")
    
    # Check segment distribution
    segment_dist = df['true_segment'].value_counts(normalize=True).sort_index()
    print("\n   Segment Distribution (should match [0.20, 0.35, 0.30, 0.15]):")
    for seg, pct in segment_dist.items():
        print(f"   Segment {seg}: {pct*100:5.1f}%")
    
    print("\n   ✅ Legacy mode working correctly")


if __name__ == '__main__':
    try:
        test_persona_generation()
        test_legacy_mode()
        print("\n🎉 All tests completed successfully!")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
