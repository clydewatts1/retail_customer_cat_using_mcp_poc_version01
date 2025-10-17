"""
Example script demonstrating cluster profile export for all three clustering methods.
Generates JSON and YAML files for AI LLM analysis.
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

import pandas as pd
import numpy as np

from customer_segmentation import (
    RetailDataGenerator, 
    get_config,
    FuzzyCustomerSegmentation,
    NeuralCustomerSegmentation,
    GMMCustomerSegmentation
)


def main():
    """Run all clustering methods and export profiles for LLM analysis."""
    print("=" * 80)
    print("CLUSTER PROFILE EXPORT FOR AI LLM ANALYSIS")
    print("=" * 80)
    
    # Load configuration
    config = get_config()
    print(f"\n✓ Configuration loaded from: {config.config_path}")
    
    # Generate customer data
    print(f"\n📊 Generating customer data...")
    data_gen_config = config.data_generation
    use_enriched_features = config.fuzzy_clustering.get('use_enriched_features', True)
    
    # Setup persona configuration if enabled
    use_personas = data_gen_config.get('use_personas', True)
    faker_cfg = data_gen_config.get('faker', {})
    personas_path = data_gen_config.get('personas_config_file', 'config/personas.yml')
    hierarchy_path = data_gen_config.get('hierarchy_config_file', 'hierarchy_parsed.yml')
    
    generator = RetailDataGenerator(
        seed=data_gen_config['random_seed'],
        faker_enabled=faker_cfg.get('enabled', True),
        faker_locale=faker_cfg.get('locale', 'en_US'),
        use_personas=use_personas,
        personas_config_path=personas_path,
        hierarchy_config_path=hierarchy_path
    )
    
    # Generate dataset based on config (use enriched if configured)
    dataset_type = 'enriched' if use_enriched_features else 'basic'
    data = generator.generate_customer_data(
        n_customers=data_gen_config.get('n_customers', 10000),
        dataset_type=dataset_type
    )
    print(f"✓ Generated {len(data)} customer records with {len(data.columns)} features")
    print(f"   Using {dataset_type} dataset for clustering")
    
    # ==============================================================================
    # 1. FUZZY C-MEANS CLUSTERING
    # ==============================================================================
    print(f"\n{'='*80}")
    print("1. FUZZY C-MEANS CLUSTERING")
    print(f"{'='*80}")
    
    fuzzy_config = config.fuzzy_clustering
    fuzzy_model = FuzzyCustomerSegmentation(
        n_clusters=fuzzy_config.get('n_clusters', 13),
        m=float(fuzzy_config['fuzziness_parameter']),
        max_iter=fuzzy_config['max_iterations'],
        error=float(fuzzy_config['tolerance']),
        seed=fuzzy_config['random_seed']
    )
    fuzzy_model.config = config._config
    
    print(f"\n🔄 Fitting Fuzzy C-Means clustering...")
    fuzzy_labels, fuzzy_membership = fuzzy_model.fit_predict(data)
    data['fuzzy_cluster'] = fuzzy_labels
    
    fuzzy_metrics = fuzzy_model.evaluate(data)
    print(f"✓ Clustering completed - Silhouette Score: {fuzzy_metrics['silhouette_score']:.4f}")
    
    print(f"\n💾 Exporting Fuzzy cluster profile...")
    fuzzy_export = fuzzy_model.export_cluster_profile(data, output_dir='data/output')
    print(f"✓ JSON: {fuzzy_export['json']}")
    print(f"✓ YAML: {fuzzy_export['yaml']}")
    
    # ==============================================================================
    # 2. NEURAL NETWORK CLUSTERING
    # ==============================================================================
    print(f"\n{'='*80}")
    print("2. NEURAL NETWORK CLUSTERING")
    print(f"{'='*80}")
    
    neural_config = config.neural_clustering
    neural_model = NeuralCustomerSegmentation(
        n_clusters=neural_config.get('n_clusters', 13),
        encoding_dim=neural_config['encoding_dim'],
        epochs=neural_config['epochs'],
        batch_size=neural_config['batch_size'],
        seed=neural_config['random_seed']
    )
    neural_model.config = config._config
    
    print(f"\n🔄 Training Neural Network clustering...")
    neural_labels = neural_model.fit_predict(data, verbose=0)
    data['neural_cluster'] = neural_labels
    
    neural_metrics = neural_model.evaluate(data)
    print(f"✓ Clustering completed - Silhouette Score: {neural_metrics['silhouette_score']:.4f}")
    
    print(f"\n💾 Exporting Neural cluster profile...")
    neural_export = neural_model.export_cluster_profile(data, output_dir='data/output')
    print(f"✓ JSON: {neural_export['json']}")
    print(f"✓ YAML: {neural_export['yaml']}")
    
    # ==============================================================================
    # 3. GAUSSIAN MIXTURE MODEL (GMM) CLUSTERING
    # ==============================================================================
    print(f"\n{'='*80}")
    print("3. GAUSSIAN MIXTURE MODEL (GMM) CLUSTERING")
    print(f"{'='*80}")
    
    gmm_config = config.fuzzy_clustering  # Use same n_clusters
    gmm_model = GMMCustomerSegmentation(
        n_clusters=gmm_config.get('n_clusters', 13),
        covariance_type='full',
        max_iter=200,
        n_init=10,
        seed=gmm_config['random_seed']
    )
    gmm_model.config = config._config
    
    print(f"\n🔄 Fitting Gaussian Mixture Model...")
    gmm_labels, gmm_proba = gmm_model.fit_predict(data)
    data['gmm_cluster'] = gmm_labels
    
    gmm_metrics = gmm_model.evaluate(data)
    print(f"✓ Clustering completed - Silhouette Score: {gmm_metrics['silhouette_score']:.4f}")
    
    print(f"\n💾 Exporting GMM cluster profile...")
    gmm_export = gmm_model.export_cluster_profile(data, output_dir='data/output')
    print(f"✓ JSON: {gmm_export['json']}")
    print(f"✓ YAML: {gmm_export['yaml']}")
    
    # ==============================================================================
    # SUMMARY
    # ==============================================================================
    print(f"\n{'='*80}")
    print("EXPORT SUMMARY")
    print(f"{'='*80}")
    
    print(f"\n📁 All cluster profiles exported to: data/output/")
    print(f"\n🎯 Files Generated:")
    print(f"\nFuzzy C-Means:")
    print(f"  - {Path(fuzzy_export['json']).name}")
    print(f"  - {Path(fuzzy_export['yaml']).name}")
    
    print(f"\nNeural Network:")
    print(f"  - {Path(neural_export['json']).name}")
    print(f"  - {Path(neural_export['yaml']).name}")
    
    print(f"\nGaussian Mixture Model:")
    print(f"  - {Path(gmm_export['json']).name}")
    print(f"  - {Path(gmm_export['yaml']).name}")
    
    print(f"\n📊 Comparison:")
    print(f"  - Fuzzy C-Means Silhouette: {fuzzy_metrics['silhouette_score']:.4f}")
    print(f"  - Neural Network Silhouette: {neural_metrics['silhouette_score']:.4f}")
    print(f"  - GMM Silhouette: {gmm_metrics['silhouette_score']:.4f}")
    
    print(f"\n💡 Next Steps:")
    print(f"  - Use the JSON/YAML files as input to an AI LLM")
    print(f"  - LLM can analyze cluster characteristics and generate:")
    print(f"    • Customer segment profiles")
    print(f"    • Marketing recommendations")
    print(f"    • Personalization strategies")
    print(f"    • Business insights")
    
    print(f"\n{'='*80}")
    print("✓ PROFILE EXPORT COMPLETE")
    print(f"{'='*80}\n")


if __name__ == '__main__':
    main()
