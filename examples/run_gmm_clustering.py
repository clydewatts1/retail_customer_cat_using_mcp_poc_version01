"""
Example script demonstrating GMM (Gaussian Mixture Model) clustering for customer segmentation.
This script shows how to use the GMMCustomerSegmentation class.
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from customer_segmentation import RetailDataGenerator, get_config, GMMCustomerSegmentation


def main():
    """Run GMM clustering example."""
    print("=" * 70)
    print("GMM CLUSTERING FOR CUSTOMER SEGMENTATION")
    print("=" * 70)
    
    # Load configuration
    config = get_config()
    print(f"\n✓ Configuration loaded from: {config.config_path}")
    
    # Generate customer data
    print(f"\n📊 Generating customer data...")
    data_gen_config = config.data_generation
    use_personas = data_gen_config.get('use_personas', True)
    use_enriched_features = config.fuzzy_clustering.get('use_enriched_features', True)
    
    # Setup persona configuration if enabled
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
    
    if use_personas:
        print(f"   Using persona-based generation")
    
    # Initialize GMM clustering
    print(f"\n🔄 Initializing GMM clustering...")
    gmm_config = config.fuzzy_clustering  # Use same config for n_clusters
    
    gmm_model = GMMCustomerSegmentation(
        n_clusters=gmm_config.get('n_clusters', 13),
        covariance_type='full',
        max_iter=200,
        n_init=10,
        seed=gmm_config['random_seed']
    )
    
    # Store config for feature selection
    gmm_model.config = config._config  # Access internal config dict
    
    # Fit and predict
    print(f"🎯 Fitting GMM with {gmm_config.get('n_clusters', 13)} components...")
    cluster_labels, probabilities = gmm_model.fit_predict(data)
    
    # Add results to dataframe
    data['gmm_cluster'] = cluster_labels
    
    # Display results
    print(f"\n✓ GMM clustering completed!")
    print(f"  - Converged: {gmm_model.gmm.converged_}")
    print(f"  - Iterations: {gmm_model.gmm.n_iter_}")
    
    print(f"\n📈 Cluster Distribution:")
    cluster_counts = data['gmm_cluster'].value_counts().sort_index()
    for cluster_id, count in cluster_counts.items():
        pct = (count / len(data)) * 100
        print(f"  - Cluster {cluster_id}: {count} customers ({pct:.1f}%)")
    
    # Evaluate clustering
    print(f"\n📊 Clustering Metrics:")
    metrics = gmm_model.evaluate(data)
    print(f"  - Silhouette Score: {metrics['silhouette_score']:.4f}")
    print(f"  - BIC: {metrics['bic']:.2f}")
    print(f"  - AIC: {metrics['aic']:.2f}")
    print(f"  - Davies-Bouldin Index: {metrics['davies_bouldin_index']:.4f} (lower is better)")
    print(f"  - Calinski-Harabasz Score: {metrics['calinski_harabasz_score']:.2f} (higher is better)")
    print(f"  - Log Likelihood: {metrics['log_likelihood']:.2f}")
    
    # Uncertainty metrics
    print(f"\n🎲 Assignment Uncertainty:")
    uncertainty = gmm_model.get_uncertainty_metrics(data)
    print(f"  - Average Max Probability: {uncertainty['avg_max_probability']:.4f}")
    print(f"  - High Confidence (>90%): {uncertainty['high_confidence_count']} customers ({uncertainty['high_confidence_pct']:.1f}%)")
    print(f"  - Low Confidence (<70%): {uncertainty['low_confidence_count']} customers ({uncertainty['low_confidence_pct']:.1f}%)")
    print(f"  - Average Entropy: {uncertainty['avg_entropy']:.4f}")
    
    # Display cluster centers
    print(f"\n🎯 Cluster Centers:")
    centers = gmm_model.get_cluster_centers()
    print(centers.to_string())
    
    # Display mixture weights
    print(f"\n⚖️  Mixture Weights (Prior Probabilities):")
    weights = gmm_model.get_weights()
    for i, weight in enumerate(weights):
        print(f"  - Cluster {i}: {weight:.4f}")
    
    # Export cluster profiles for LLM analysis
    print(f"\n💾 Exporting cluster profiles for AI LLM analysis...")
    export_result = gmm_model.export_cluster_profile(data, output_dir='data/output')
    print(f"✓ JSON profile saved to: {export_result['json']}")
    print(f"✓ YAML profile saved to: {export_result['yaml']}")
    
    # Visualize results
    print(f"\n📊 Creating visualizations...")
    
    # Create figure with multiple subplots
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # 1. Hard clustering scatter plot
    scatter1 = axes[0, 0].scatter(
        data['recency_days'], 
        data['total_revenue'],
        c=data['gmm_cluster'], 
        cmap='viridis',
        alpha=0.6, 
        s=50, 
        edgecolors='black', 
        linewidth=0.5
    )
    axes[0, 0].set_xlabel('Recency (days)', fontsize=12)
    axes[0, 0].set_ylabel('Total Revenue ($)', fontsize=12)
    axes[0, 0].set_title('GMM Clustering (Hard Assignment)', fontsize=14, fontweight='bold')
    axes[0, 0].grid(alpha=0.3)
    plt.colorbar(scatter1, ax=axes[0, 0], label='Cluster')
    
    # 2. Soft clustering - assignment confidence
    max_proba = probabilities.max(axis=1)
    scatter2 = axes[0, 1].scatter(
        data['recency_days'], 
        data['total_revenue'],
        c=max_proba, 
        cmap='plasma',
        alpha=0.6, 
        s=50, 
        edgecolors='black', 
        linewidth=0.5
    )
    axes[0, 1].set_xlabel('Recency (days)', fontsize=12)
    axes[0, 1].set_ylabel('Total Revenue ($)', fontsize=12)
    axes[0, 1].set_title('GMM Assignment Confidence', fontsize=14, fontweight='bold')
    axes[0, 1].grid(alpha=0.3)
    plt.colorbar(scatter2, ax=axes[0, 1], label='Max Probability')
    
    # 3. Cluster sizes bar chart
    axes[1, 0].bar(
        cluster_counts.index, 
        cluster_counts.values, 
        color='mediumseagreen', 
        edgecolor='black',
        linewidth=1.5
    )
    axes[1, 0].set_xlabel('Cluster', fontsize=12)
    axes[1, 0].set_ylabel('Number of Customers', fontsize=12)
    axes[1, 0].set_title('Cluster Size Distribution', fontsize=14, fontweight='bold')
    axes[1, 0].grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for i, v in enumerate(cluster_counts.values):
        axes[1, 0].text(i, v + 5, str(v), ha='center', fontweight='bold')
    
    # 4. Probability distribution histogram
    axes[1, 1].hist(max_proba, bins=30, color='steelblue', edgecolor='black', alpha=0.7)
    axes[1, 1].axvline(0.9, color='green', linestyle='--', linewidth=2, label='High Confidence (>90%)')
    axes[1, 1].axvline(0.7, color='orange', linestyle='--', linewidth=2, label='Low Confidence (<70%)')
    axes[1, 1].set_xlabel('Maximum Probability', fontsize=12)
    axes[1, 1].set_ylabel('Frequency', fontsize=12)
    axes[1, 1].set_title('Assignment Confidence Distribution', fontsize=14, fontweight='bold')
    axes[1, 1].legend()
    axes[1, 1].grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    
    # Save visualization
    output_path = Path(__file__).parent.parent / 'visualizations' / 'gmm_clustering_results.png'
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Visualization saved to: {output_path}")
    
    plt.show()
    
    # Summary
    print(f"\n{'=' * 70}")
    print("SUMMARY")
    print(f"{'=' * 70}")
    print(f"✓ Successfully clustered {len(data)} customers into {gmm_config.get('n_clusters', 13)} segments")
    print(f"✓ Silhouette Score: {metrics['silhouette_score']:.4f}")
    print(f"✓ Average Assignment Confidence: {uncertainty['avg_max_probability']:.4f}")
    print(f"✓ GMM provides probabilistic cluster assignments for uncertainty quantification")
    print(f"{'=' * 70}\n")


if __name__ == '__main__':
    main()
