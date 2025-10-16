"""
Quick validation script to test config module attributes.
Run this to verify the config module is working correctly.
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from customer_segmentation import get_config

def test_config():
    """Test config module attributes."""
    try:
        config_path = Path(__file__).parent.parent / "config" / "config.yml"
        print(f"Loading config from: {config_path}")
        print(f"Config exists: {config_path.exists()}")
        print()
        
        config = get_config(str(config_path))
        print("✓ Config loaded successfully")
        print()
        
        # Test required attributes
        tests = [
            ('paths', lambda: config.paths),
            ('data_generation', lambda: config.data_generation),
            ('columns', lambda: config.columns),
            ('fuzzy_clustering', lambda: config.fuzzy_clustering),
            ('neural_clustering', lambda: config.neural_clustering),
            ('visualization', lambda: config.visualization),
        ]
        
        print("Testing config attributes:")
        print("-" * 50)
        
        for name, getter in tests:
            try:
                value = getter()
                print(f"✓ config.{name} -> {type(value).__name__} with {len(value)} keys")
            except Exception as e:
                print(f"✗ config.{name} -> ERROR: {e}")
                return False
        
        print()
        print("Testing nested access:")
        print("-" * 50)
        
        # Test specific nested values
        nested_tests = [
            ("config.data_generation['n_customers']", lambda: config.data_generation['n_customers']),
            ("config.data_generation['random_seed']", lambda: config.data_generation['random_seed']),
            ("config.paths['data_dir']", lambda: config.paths['data_dir']),
            ("config.paths['visualizations_dir']", lambda: config.paths['visualizations_dir']),
            ("config.fuzzy_clustering['n_clusters']", lambda: config.fuzzy_clustering['n_clusters']),
            ("config.neural_clustering['n_clusters']", lambda: config.neural_clustering['n_clusters']),
            ("config.visualization['dpi']", lambda: config.visualization['dpi']),
            ("config.visualization['figure_format']", lambda: config.visualization['figure_format']),
        ]
        
        for desc, getter in nested_tests:
            try:
                value = getter()
                print(f"✓ {desc} -> {value}")
            except Exception as e:
                print(f"✗ {desc} -> ERROR: {e}")
                return False
        
        print()
        print("=" * 50)
        print("✓ All config tests passed!")
        print("=" * 50)
        return True
        
    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_config()
    sys.exit(0 if success else 1)
