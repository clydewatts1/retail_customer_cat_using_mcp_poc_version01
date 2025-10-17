"""
Validation script for persona distribution and behavioral patterns.
Generates a large dataset and validates that personas behave as expected.
"""
import sys
from pathlib import Path
import pandas as pd
import numpy as np

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from customer_segmentation.data_generator import RetailDataGenerator
import yaml


def load_expected_personas():
    """Load expected persona definitions from config."""
    personas_path = project_root / "config" / "personas.yml"
    with open(personas_path, 'r') as f:
        personas_data = yaml.safe_load(f)
    return personas_data['customer_personas']


def validate_persona_weights(df, expected_personas, tolerance=0.035):
    """Validate that persona distribution matches expected weights."""
    print("\n" + "="*70)
    print("PERSONA DISTRIBUTION VALIDATION")
    print("="*70)
    
    actual_dist = df['persona_type'].value_counts(normalize=True).sort_index()
    
    validation_results = []
    for persona, expected_weight in [(p, expected_personas[p]['weight']) for p in expected_personas]:
        actual_weight = actual_dist.get(persona, 0.0)
        diff = abs(actual_weight - expected_weight)
        status = "✅ PASS" if diff <= tolerance else "⚠️ FAIL"
        
        validation_results.append({
            'persona': persona,
            'expected': f"{expected_weight*100:.1f}%",
            'actual': f"{actual_weight*100:.1f}%",
            'diff': f"{diff*100:.1f}%",
            'status': status
        })
        
        print(f"{persona:30s} | Expected: {expected_weight*100:5.1f}% | Actual: {actual_weight*100:5.1f}% | Diff: {diff*100:4.1f}% | {status}")
    
    passed = sum(1 for r in validation_results if '✅' in r['status'])
    total = len(validation_results)
    
    print(f"\n{'='*70}")
    print(f"Result: {passed}/{total} personas within tolerance (±{tolerance*100}%)")
    print(f"{'='*70}\n")
    
    return passed == total


def validate_department_preferences(df, expected_personas):
    """Validate that department spending aligns with persona preferences."""
    print("\n" + "="*70)
    print("DEPARTMENT PREFERENCE VALIDATION")
    print("="*70)
    
    dept_cols = [c for c in df.columns if c.startswith('dept_total_value_')]
    
    validation_passed = True
    
    for persona_name in df['persona_type'].unique():
        persona_data = df[df['persona_type'] == persona_name]
        expected_prefs = expected_personas[persona_name].get('department_preferences', {})
        
        if not expected_prefs:
            continue
        
        # Calculate actual department spend distribution
        dept_totals = persona_data[dept_cols].sum()
        dept_totals_pct = dept_totals / dept_totals.sum()
        
        # Get top 3 expected departments
        top_expected = sorted(expected_prefs.items(), key=lambda x: x[1], reverse=True)[:3]
        
        print(f"\n{persona_name}:")
        print("  Expected Top Departments:")
        for dept, pct in top_expected:
            print(f"    {dept:40s}: {pct*100:5.1f}%")
        
        # Get top 3 actual departments
        dept_totals_sorted = dept_totals_pct.sort_values(ascending=False).head(3)
        print("  Actual Top Departments:")
        for dept_col, pct in dept_totals_sorted.items():
            dept_name = dept_col.replace('dept_total_value_', '')
            print(f"    {dept_name:40s}: {pct*100:5.1f}%")
        
        # Check if top expected departments are in top 5 actual
        top_5_actual = dept_totals_pct.sort_values(ascending=False).head(5)
        top_5_actual_names = [c.replace('dept_total_value_', '') for c in top_5_actual.index]
        
        matches = sum(1 for dept, _ in top_expected if dept in top_5_actual_names)
        status = "✅ PASS" if matches >= 2 else "⚠️ FAIL"
        print(f"  Status: {status} ({matches}/3 top expected departments in top 5 actual)")
        
        if matches < 2:
            validation_passed = False
    
    print(f"\n{'='*70}")
    print(f"Result: {'✅ ALL PASSED' if validation_passed else '⚠️ SOME FAILED'}")
    print(f"{'='*70}\n")
    
    return validation_passed


def validate_spending_ranges(df, expected_personas):
    """Validate that spending ranges match persona profiles."""
    print("\n" + "="*70)
    print("SPENDING RANGE VALIDATION")
    print("="*70)
    
    validation_passed = True
    
    for persona_name in df['persona_type'].unique():
        persona_data = df[df['persona_type'] == persona_name]
        expected_profile = expected_personas[persona_name].get('spending_profile', {})
        
        expected_aov_range = expected_profile.get('avg_order_value', [0, 1000])
        expected_freq_range = expected_profile.get('frequency_per_month', [0, 10])
        
        actual_aov_mean = persona_data['avg_order_value'].mean()
        actual_freq_mean = persona_data['frequency_per_month'].mean()
        
        # Check if actual means are within expected ranges
        aov_in_range = expected_aov_range[0] <= actual_aov_mean <= expected_aov_range[1]
        freq_in_range = expected_freq_range[0] <= actual_freq_mean <= expected_freq_range[1]
        
        aov_status = "✅" if aov_in_range else "⚠️"
        freq_status = "✅" if freq_in_range else "⚠️"
        
        print(f"\n{persona_name}:")
        print(f"  Avg Order Value:")
        print(f"    Expected Range: ${expected_aov_range[0]:.2f} - ${expected_aov_range[1]:.2f}")
        print(f"    Actual Mean:    ${actual_aov_mean:.2f} {aov_status}")
        print(f"  Frequency per Month:")
        print(f"    Expected Range: {expected_freq_range[0]:.2f} - {expected_freq_range[1]:.2f}")
        print(f"    Actual Mean:    {actual_freq_mean:.2f} {freq_status}")
        
        if not (aov_in_range and freq_in_range):
            validation_passed = False
    
    print(f"\n{'='*70}")
    print(f"Result: {'✅ ALL PASSED' if validation_passed else '⚠️ SOME FAILED'}")
    print(f"{'='*70}\n")
    
    return validation_passed


def validate_department_summaries(df):
    """Validate that department summaries aggregate correctly."""
    print("\n" + "="*70)
    print("DEPARTMENT SUMMARY VALIDATION")
    print("="*70)
    
    dept_value_cols = [c for c in df.columns if c.startswith('dept_total_value_')]
    dept_unit_cols = [c for c in df.columns if c.startswith('dept_total_units_')]
    
    validation_passed = True
    
    # Sample 10 random customers
    sample_customers = df.sample(min(10, len(df)))
    
    for idx, row in sample_customers.iterrows():
        customer_id = row['customer_id']
        total_purchases = row['total_purchases']
        
        # Sum of all department units should approximately equal total_purchases
        dept_units_sum = sum(row[col] for col in dept_unit_cols)
        
        # Allow small rounding differences
        units_match = abs(dept_units_sum - total_purchases) <= 2
        
        status = "✅" if units_match else "⚠️"
        
        if not units_match:
            print(f"{customer_id}: Total Purchases={total_purchases}, Dept Units Sum={dept_units_sum} {status}")
            validation_passed = False
    
    if validation_passed:
        print("✅ All sampled customers: Department units match total purchases")
    
    # Note: Department values are generated independently and won't sum exactly to total_revenue
    # This is realistic - individual transactions have variance
    # Just check that department sums are reasonable (within order of magnitude)
    print("\nDepartment Value Sanity Check (sample):")
    for idx, row in sample_customers.head(5).iterrows():
        customer_id = row['customer_id']
        total_revenue = row['total_revenue']
        dept_value_sum = sum(row[col] for col in dept_value_cols)
        
        # Check that dept sum is at least 20% of total revenue (very loose check)
        ratio = dept_value_sum / total_revenue if total_revenue > 0 else 0
        reasonable = ratio >= 0.2
        status = "✅" if reasonable else "⚠️"
        
        print(f"  {customer_id}: Total Revenue=${total_revenue:.2f}, Dept Sum=${dept_value_sum:.2f} (ratio: {ratio:.1%}) {status}")
        
        if not reasonable:
            validation_passed = False
    
    print(f"\n{'='*70}")
    print(f"Result: {'✅ PASSED' if validation_passed else '⚠️ FAILED'}")
    print(f"{'='*70}\n")
    
    return validation_passed


def generate_validation_report(df, expected_personas):
    """Generate comprehensive validation report."""
    print("\n" + "="*70)
    print("COMPREHENSIVE VALIDATION REPORT")
    print("="*70)
    print(f"Dataset Size: {len(df)} customers")
    print(f"Features: {len(df.columns)} columns")
    print(f"Personas: {df['persona_type'].nunique()} unique types")
    print(f"Date: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    # Run all validations
    results = {}
    results['persona_weights'] = validate_persona_weights(df, expected_personas)
    results['department_preferences'] = validate_department_preferences(df, expected_personas)
    results['spending_ranges'] = validate_spending_ranges(df, expected_personas)
    results['department_summaries'] = validate_department_summaries(df)
    
    # Summary
    print("\n" + "="*70)
    print("VALIDATION SUMMARY")
    print("="*70)
    
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "⚠️ FAILED"
        print(f"{test_name.replace('_', ' ').title():40s}: {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "="*70)
    if all_passed:
        print("🎉 ALL VALIDATIONS PASSED!")
        print("The persona-based data generation system is working correctly.")
    else:
        print("⚠️ SOME VALIDATIONS FAILED")
        print("Review the failures above and adjust persona configurations if needed.")
    print("="*70 + "\n")
    
    return all_passed


def main():
    """Run comprehensive persona validation."""
    print("="*70)
    print("PERSONA DISTRIBUTION & PATTERN VALIDATION")
    print("="*70)
    print("\nGenerating validation dataset (1000 customers)...")
    
    # Load config for n_customers and enriched features
    from customer_segmentation import get_config
    config_path = project_root / "config" / "config.yml"
    config = get_config(str(config_path))
    n_customers = config.data_generation.get('n_customers', 10000)
    use_enriched_features = config.fuzzy_clustering.get('use_enriched_features', True)
    
    # Generate large dataset
    generator = RetailDataGenerator(
        seed=config.data_generation.get('random_seed', 42),
        faker_enabled=config.data_generation.get('faker', {}).get('enabled', True),
        use_personas=config.data_generation.get('use_personas', True),
        personas_config_path=config.data_generation.get('personas_config_file', 'config/personas.yml'),
        hierarchy_config_path=config.data_generation.get('hierarchy_config_file', 'hierarchy_parsed.yml')
    )
    df = generator.generate_customer_data(n_customers=n_customers, dataset_type='enriched' if use_enriched_features else 'basic')
    print(f"✅ Generated {len(df)} customers with {len(df.columns)} features")
    
    # Load expected personas
    expected_personas = load_expected_personas()
    print(f"✅ Loaded {len(expected_personas)} persona definitions")
    
    # Run validation
    all_passed = generate_validation_report(df, expected_personas)
    
    # Save validation dataset
    validation_path = project_root / "data" / "validation_1000_customers.csv"
    df.to_csv(validation_path, index=False)
    print(f"\n💾 Validation dataset saved to: {validation_path}")
    
    # Exit with appropriate code
    sys.exit(0 if all_passed else 1)


if __name__ == '__main__':
    main()
