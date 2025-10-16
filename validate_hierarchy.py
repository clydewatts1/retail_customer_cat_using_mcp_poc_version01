"""
Validate hierarchical department-class relationships in generated data.
"""
import pandas as pd
import numpy as np

# Load data
df = pd.read_csv('data/customer_sales_data_enriched.csv')

print("=" * 80)
print("HIERARCHICAL DEPARTMENT-CLASS VALIDATION")
print("=" * 80)
print()

# Test 5 random customers
np.random.seed(42)
sample_indices = np.random.choice(len(df), min(5, len(df)), replace=False)

all_valid = True

for idx in sample_indices:
    c = df.iloc[idx]
    print(f"Customer {c['customer_id']}:")
    
    # Accessories & Footwear
    acc_dept = c['dept_total_value_Accessories & Footwear']
    acc_classes = (c['class_total_value_Bags & Wallets'] + 
                   c['class_total_value_Soft & Hard Accessories'])
    acc_valid = abs(acc_dept - acc_classes) < 0.01
    all_valid = all_valid and acc_valid
    
    print(f"  Accessories & Footwear: ${acc_dept:.2f}")
    print(f"    = Bags & Wallets (${c['class_total_value_Bags & Wallets']:.2f})")
    print(f"    + Soft & Hard Accessories (${c['class_total_value_Soft & Hard Accessories']:.2f})")
    print(f"    = ${acc_classes:.2f} {'✓' if acc_valid else '✗ ERROR'}")
    
    # Health & Wellness
    hw_dept = c['dept_total_value_Health & Wellness']
    hw_classes = (c['class_total_value_Consumables'] + 
                  c['class_total_value_Personal Care'])
    hw_valid = abs(hw_dept - hw_classes) < 0.01
    all_valid = all_valid and hw_valid
    
    print(f"  Health & Wellness: ${hw_dept:.2f}")
    print(f"    = Consumables (${c['class_total_value_Consumables']:.2f})")
    print(f"    + Personal Care (${c['class_total_value_Personal Care']:.2f})")
    print(f"    = ${hw_classes:.2f} {'✓' if hw_valid else '✗ ERROR'}")
    
    # Home & Lifestyle
    hl_dept = c['dept_total_value_Home & Lifestyle']
    hl_classes = c['class_total_value_Bedding']
    hl_valid = abs(hl_dept - hl_classes) < 0.01
    all_valid = all_valid and hl_valid
    
    print(f"  Home & Lifestyle: ${hl_dept:.2f}")
    print(f"    = Bedding (${c['class_total_value_Bedding']:.2f})")
    print(f"    = ${hl_classes:.2f} {'✓' if hl_valid else '✗ ERROR'}")
    print()

print("=" * 80)
print(f"OVERALL VALIDATION: {'✓ PASS - All hierarchies are correct!' if all_valid else '✗ FAIL - Errors detected'}")
print("=" * 80)
print()

# Summary statistics
print("Summary Statistics:")
print(f"Total customers: {len(df)}")
print(f"Features per customer: {len(df.columns)}")
print()

print("Department Distribution (Average per customer):")
for dept in ['Accessories & Footwear', 'Health & Wellness', 'Home & Lifestyle']:
    avg_value = df[f'dept_total_value_{dept}'].mean()
    avg_units = df[f'dept_total_units_{dept}'].mean()
    print(f"  {dept}: ${avg_value:.2f} ({avg_units:.1f} units)")
print()

print("Class Distribution (Average per customer):")
classes = ['Bags & Wallets', 'Soft & Hard Accessories', 'Consumables', 'Personal Care', 'Bedding']
for cls in classes:
    avg_value = df[f'class_total_value_{cls}'].mean()
    avg_units = df[f'class_total_units_{cls}'].mean()
    print(f"  {cls}: ${avg_value:.2f} ({avg_units:.1f} units)")
