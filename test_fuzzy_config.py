"""Test script to validate fuzzy clustering features configuration."""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from customer_segmentation import get_config

# Load configuration
config_path = Path(__file__).parent / 'config' / 'config.yml'
config = get_config(str(config_path))

print("=" * 80)
print("FUZZY CLUSTERING FEATURES CONFIGURATION TEST")
print("=" * 80)
print()

# Test fuzzy clustering config
print("=== FUZZY CLUSTERING CONFIG ===")
fc = config.fuzzy_clustering
print(f"Clusters: {fc.get('n_clusters')}")
print(f"Fuzziness Parameter: {fc.get('fuzziness_parameter')}")
print(f"Max Iterations: {fc.get('max_iterations')}")
print(f"Random Seed: {fc.get('random_seed')}")
print()

print(f"Core Features ({len(fc.get('features_to_use', []))}):")
for feat in fc.get('features_to_use', []):
    print(f"  - {feat}")
print()

print(f"Use Enriched Features: {fc.get('use_enriched_features')}")
print(f"Enriched Features Available ({len(fc.get('enriched_features_to_use', []))}):")
for feat in fc.get('enriched_features_to_use', [])[:5]:  # Show first 5
    print(f"  - {feat}")
if len(fc.get('enriched_features_to_use', [])) > 5:
    print(f"  ... and {len(fc.get('enriched_features_to_use', [])) - 5} more")
print()

print("Output Columns:")
output_cols = fc.get('output_columns', {})
for key, value in output_cols.items():
    print(f"  {key}: {value}")
print()

# Test neural clustering config
print("=== NEURAL CLUSTERING CONFIG ===")
nc = config.neural_clustering
print(f"Clusters: {nc.get('n_clusters')}")
print(f"Encoding Dim: {nc.get('encoding_dim')}")
print(f"Epochs: {nc.get('epochs')}")
print()

print(f"Use Enriched Features: {nc.get('use_enriched_features')}")
print(f"Enriched Features Available ({len(nc.get('enriched_features_to_use', []))}):")
for feat in nc.get('enriched_features_to_use', [])[:5]:
    print(f"  - {feat}")
if len(nc.get('enriched_features_to_use', [])) > 5:
    print(f"  ... and {len(nc.get('enriched_features_to_use', [])) - 5} more")
print()

print("Output Columns:")
output_cols = nc.get('output_columns', {})
for key, value in output_cols.items():
    print(f"  {key}: {value}")
print()

print("=" * 80)
print("✓ CONFIGURATION LOADED SUCCESSFULLY!")
print("=" * 80)
