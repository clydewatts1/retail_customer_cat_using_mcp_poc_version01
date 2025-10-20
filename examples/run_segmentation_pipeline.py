"""
Example demonstrating the complete customer segmentation pipeline.
This script shows how to:
1. Generate synthetic retail customer data (with persona support)
2. Perform fuzzy clustering on BASIC dataset
3. Perform neural network clustering on BASIC dataset
4. Perform GMM clustering on BASIC dataset
5. Enrich clusters with meaningful descriptions
6. Export data for AI agent interaction

All parameters are loaded from config.yml.

NEW: Uses BASIC dataset (clustering features only) for clustering,
     and ENRICHED dataset for analysis and enrichment.
"""
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from customer_segmentation import (
    RetailDataGenerator,
    FuzzyCustomerSegmentation,
    NeuralCustomerSegmentation,
    GMMCustomerSegmentation,
    ClusterEnrichment,
    get_config
)
import pandas as pd
import numpy as np


def main():
    """Run the complete customer segmentation pipeline."""
    
    # Load configuration
    config_path = Path(__file__).parent.parent / "config" / "config.yml"
    config = get_config(str(config_path))
    
    print("=" * 80)
    print("Customer Segmentation POC - Complete Pipeline (with Personas)")
    print("=" * 80)
    print(f"Configuration loaded from: {config_path}")
    print()
    
    # Step 1: Generate or load customer data
    print("Step 1: Loading customer data (BASIC for clustering, ENRICHED for analysis)...")
    
    # Get data generation parameters from config
    num_customers = config.data_generation.get('n_customers', 10000)
    seed = config.data_generation['random_seed']
    use_personas = config.data_generation.get('use_personas', True)
    generate_dual = config.data_generation.get('generate_dual_datasets', True)
    
    # Setup data paths
    data_dir = Path(__file__).parent.parent / config.paths['data_dir']
    data_dir.mkdir(parents=True, exist_ok=True)
    basic_data_path = data_dir / Path(config.data_generation.get('basic_dataset_path', 'customer_sales_data_basic.csv')).name
    enriched_data_path = data_dir / Path(config.data_generation.get('enriched_dataset_path', 'customer_sales_data_enriched.csv')).name
    # Always use enriched features for clustering if set in config
    use_enriched_features = config.fuzzy_clustering.get('use_enriched_features', True)
    
    # Check if data already exists
    if basic_data_path.exists() and enriched_data_path.exists():
        print(f"✅ Loading existing datasets:")
        print(f"   - Basic: {basic_data_path}")
        print(f"   - Enriched: {enriched_data_path}")
        customer_data_basic = pd.read_csv(basic_data_path)
        customer_data_enriched = pd.read_csv(enriched_data_path)
        
        # CRITICAL: Ensure both datasets have the same customers in the same order
        if len(customer_data_basic) != len(customer_data_enriched):
            print(f"\n⚠️  WARNING: Dataset size mismatch!")
            print(f"   Basic: {len(customer_data_basic)} customers")
            print(f"   Enriched: {len(customer_data_enriched)} customers")
            print(f"   Aligning datasets to match basic dataset...")
            
            # Align enriched to match basic dataset customer IDs
            if 'customer_id' in customer_data_basic.columns and 'customer_id' in customer_data_enriched.columns:
                basic_ids = customer_data_basic['customer_id'].tolist()
                customer_data_enriched = customer_data_enriched[customer_data_enriched['customer_id'].isin(basic_ids)]
                # Ensure same order
                customer_data_enriched = customer_data_enriched.set_index('customer_id').loc[basic_ids].reset_index()
                print(f"   ✅ Aligned enriched dataset: {len(customer_data_enriched)} customers")
            else:
                print(f"   ❌ Cannot align - missing customer_id column")
                print(f"   Regenerating datasets...")
                raise ValueError("Dataset mismatch - please delete both files and regenerate")
        else:
            # Ensure same order even if same length
            if 'customer_id' in customer_data_basic.columns and 'customer_id' in customer_data_enriched.columns:
                basic_ids = customer_data_basic['customer_id'].tolist()
                enriched_ids = customer_data_enriched['customer_id'].tolist()
                if basic_ids != enriched_ids:
                    print(f"   ⚠️  Customer order mismatch - reordering enriched dataset...")
                    customer_data_enriched = customer_data_enriched.set_index('customer_id').loc[basic_ids].reset_index()
                    print(f"   ✅ Reordered enriched dataset")
    else:
        print(f"📊 Generating NEW datasets with persona support...")
        faker_cfg = config.data_generation.get('faker', {})
        personas_path = config.data_generation.get('personas_config_file', 'config/personas.yml')
        hierarchy_path = config.data_generation.get('hierarchy_config_file', 'hierarchy_parsed.yml')
        
        data_generator = RetailDataGenerator(
            seed=seed,
            faker_enabled=faker_cfg.get('enabled', True),
            faker_locale=faker_cfg.get('locale', 'en_US'),
            use_personas=use_personas,
            personas_config_path=personas_path,
            hierarchy_config_path=hierarchy_path
        )
        
        # Generate datasets according to config
        dataset_type = 'both' if generate_dual else 'enriched'
        if use_enriched_features:
            dataset_type = 'both' if generate_dual else 'enriched'
        else:
            dataset_type = 'basic'
        customer_data_enriched = data_generator.generate_customer_data(
            n_customers=num_customers,
            dataset_type=dataset_type
        )
        # Save enriched (basic saved automatically if dual)
        data_generator.save_data(customer_data_enriched, str(enriched_data_path))
        # Load basic dataset if it exists
        if basic_data_path.exists():
            customer_data_basic = pd.read_csv(basic_data_path)
        else:
            customer_data_basic = None
    
    print(f"\n📊 Dataset Summary:")
    if customer_data_basic is not None:
        print(f"   BASIC (for clustering):  {len(customer_data_basic):4d} customers, {len(customer_data_basic.columns):3d} features")
    else:
        print(f"   BASIC (for clustering):  Not generated (enriched only mode)")
    print(f"   ENRICHED (for analysis): {len(customer_data_enriched):4d} customers, {len(customer_data_enriched.columns):3d} features")
    
    if 'persona_type' in customer_data_enriched.columns:
        print(f"\n📈 Persona Distribution (from enriched dataset):")
        persona_counts = customer_data_enriched['persona_type'].value_counts()
        for persona, count in persona_counts.sort_index().items():
            pct = (count / len(customer_data_enriched)) * 100
            print(f"   {persona:30s}: {count:3d} ({pct:5.1f}%)")
    
    print()
    
    # Display sample data (from basic dataset for clustering)
    if customer_data_basic is not None:
        print("Sample BASIC dataset (used for clustering - first 5 customers):")
        display_cols = ['customer_id', 'total_purchases', 'total_revenue', 
                    'avg_order_value', 'recency_days', 'frequency_per_month']
        print(customer_data_basic[display_cols].head())
        print()
    else:
        print("No BASIC dataset available. All clustering will use ENRICHED dataset.")
        customer_data_basic = customer_data_enriched
    
    # Step 2: Fuzzy Clustering (using BASIC dataset)
    print("=" * 80)
    print("Step 2: Performing Fuzzy C-Means Clustering (on BASIC dataset)...")
    print("=" * 80)
    
    # Get fuzzy clustering parameters from config
    fuzzy_params = config.fuzzy_clustering
    fuzzy_model = FuzzyCustomerSegmentation(
        n_clusters=fuzzy_params.get('n_clusters', config.fuzzy_clustering.get('n_clusters', 13)),
        m=fuzzy_params.get('fuzziness_parameter', 2.0),
        seed=seed
    )
    fuzzy_labels, fuzzy_membership = fuzzy_model.fit_predict(customer_data_basic)
    
    print(f"Fuzzy clustering completed with {fuzzy_model.n_clusters} clusters")
    print()
    
    # Evaluate fuzzy clustering
    fuzzy_metrics = fuzzy_model.evaluate(customer_data_basic)
    print("Fuzzy Clustering Metrics:")
    for metric, value in fuzzy_metrics.items():
        print(f"  {metric}: {value:.4f}")
    print()
    
    # Get cluster centers
    fuzzy_centers = fuzzy_model.get_cluster_centers()
    print("Fuzzy Cluster Centers:")
    print(fuzzy_centers)
    print()
    
    # Step 3: Neural Network Clustering (using BASIC dataset)
    print("=" * 80)
    print("Step 3: Performing Neural Network Clustering (on BASIC dataset)...")
    print("=" * 80)
    
    # Get neural clustering parameters from config
    neural_params = config.neural_clustering
    neural_model = NeuralCustomerSegmentation(
        n_clusters=neural_params.get('n_clusters', config.neural_clustering.get('n_clusters', 13)),
        encoding_dim=neural_params.get('encoding_dim', 10),
        epochs=neural_params.get('epochs', 50),
        batch_size=neural_params.get('batch_size', 32),
        seed=seed
    )
    neural_labels = neural_model.fit_predict(customer_data_basic, verbose=0)
    
    print(f"Neural clustering completed with {neural_model.n_clusters} clusters")
    print()
    
    # Evaluate neural clustering
    neural_metrics = neural_model.evaluate(customer_data_basic)
    print("Neural Clustering Metrics:")
    for metric, value in neural_metrics.items():
        print(f"  {metric}: {value:.4f}")
    print()
    
    # Get cluster centers
    neural_centers = neural_model.get_cluster_centers(customer_data_basic)
    print("Neural Cluster Centers:")
    print(neural_centers)
    print()
    
    # Step 4: GMM Clustering (using BASIC dataset)
    print("=" * 80)
    print("Step 4: Performing GMM (Gaussian Mixture Model) Clustering (on BASIC dataset)...")
    print("=" * 80)
    
    # Get GMM clustering parameters from config (use same n_clusters as fuzzy/neural)
    gmm_params = config.fuzzy_clustering  # Use same config section
    gmm_model = GMMCustomerSegmentation(
        n_clusters=gmm_params.get('n_clusters', config.fuzzy_clustering.get('n_clusters', 13)),
        covariance_type='full',
        max_iter=200,
        n_init=10,
        seed=seed
    )
    gmm_labels, gmm_probabilities = gmm_model.fit_predict(customer_data_basic)
    
    print(f"GMM clustering completed with {gmm_model.n_clusters} clusters")
    print(f"  - Converged: {gmm_model.gmm.converged_}")
    print(f"  - Iterations: {gmm_model.gmm.n_iter_}")
    print()
    
    # Evaluate GMM clustering
    gmm_metrics = gmm_model.evaluate(customer_data_basic)
    print("GMM Clustering Metrics:")
    for metric, value in gmm_metrics.items():
        if 'score' in metric.lower() or 'index' in metric.lower():
            print(f"  {metric}: {value:.4f}")
        else:
            print(f"  {metric}: {value:.2f}")
    print()
    
    # Get cluster centers
    gmm_centers = gmm_model.get_cluster_centers()
    print("GMM Cluster Centers:")
    print(gmm_centers)
    print()
    
    # Step 5: Cluster Enrichment (using ENRICHED dataset for detailed analysis)
    print("=" * 80)
    print("Step 5: Enriching Clusters with Descriptions (using ENRICHED dataset)...")
    print("=" * 80)
    
    enrichment = ClusterEnrichment()
    enriched_profiles = enrichment.enrich_clusters(
        customer_data_enriched, fuzzy_labels, fuzzy_centers
    )
    
    print(f"Enriched {len(enriched_profiles)} cluster profiles")
    print()
    
    # Display enriched profiles
    for cluster_id, profile in enriched_profiles.items():
        print(f"\n{'=' * 60}")
        print(f"Cluster {cluster_id}: {profile['segment_name']}")
        print(f"{'=' * 60}")
        print(f"\nDescription:")
        print(f"  {profile['description']}")
        print(f"\nKey Characteristics:")
        chars = profile['characteristics']
        print(f"  - Segment Size: {chars['size']} customers ({chars['percentage']}%)")
        print(f"  - Avg Revenue: ${chars['avg_total_revenue']:,.2f}")
        print(f"  - Avg Order Value: ${chars['avg_order_value']:.2f}")
        print(f"  - Avg Frequency: {chars['avg_frequency']:.2f} purchases/month")
        print(f"  - Avg Recency: {chars['avg_recency_days']:.0f} days")
        
        # Analyze enriched features for this segment
        segment_data = customer_data_enriched[fuzzy_labels == cluster_id]
        
        # Department preferences
        dept_cols = [col for col in customer_data_enriched.columns if 'dept_total_value_' in col]
        dept_avg = segment_data[dept_cols].mean()
        top_dept = dept_avg.nlargest(3)
        print(f"\nTop Departments by Value:")
        for dept_col, value in top_dept.items():
            dept_name = dept_col.replace('dept_total_value_', '')
            print(f"  - {dept_name}: ${value:.2f}")
        
        # Class preferences (only if present in enriched dataset)
        class_cols = [col for col in customer_data_enriched.columns if 'class_total_value_' in col]
        if class_cols:
            class_avg = segment_data[class_cols].mean()
            top_class = class_avg.nlargest(3)
            print(f"\nTop Classes by Value:")
            for class_col, value in top_class.items():
                class_name = class_col.replace('class_total_value_', '')
                print(f"  - {class_name}: ${value:.2f}")
        
        # Size breakdown (only if present in enriched dataset)
        size_cols = [col for col in customer_data_enriched.columns if 'count_' in col]
        if size_cols:
            size_avg = segment_data[size_cols].mean()
            print(f"\nAverage Size/Age Breakdown:")
            for size_col, count in size_avg.items():
                size_name = size_col.replace('count_', '').replace('count_size_', 'Size ')
                print(f"  - {size_name}: {count:.1f} items")
        
        print(f"\nRecommended Interaction Strategies:")
        for strategy in profile['interaction_strategies'][:3]:  # Show top 3
            print(f"  • {strategy}")
        print()
    
    # Step 6: Export Cluster Profiles for All Methods
    print("=" * 80)
    print("Step 6: Exporting Cluster Profiles for All Methods...")
    print("=" * 80)
    
    # Export Fuzzy cluster profiles
    from datetime import datetime
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_dir = data_dir / "output"
    output_dir.mkdir(exist_ok=True)
    
    # Fuzzy profiles (already enriched above)
    fuzzy_profile_path = output_dir / f"fuzzy_cluster_profile_{timestamp}.json"
    enrichment.export_for_ai_agent(str(fuzzy_profile_path))
    print(f"✓ Fuzzy cluster profiles saved to: {fuzzy_profile_path}")
    
    # Neural profiles
    neural_enrichment = ClusterEnrichment()
    neural_profiles = neural_enrichment.enrich_clusters(
        customer_data_enriched, neural_labels, neural_centers
    )
    neural_profile_path = output_dir / f"neural_cluster_profile_{timestamp}.json"
    neural_enrichment.export_for_ai_agent(str(neural_profile_path))
    print(f"✓ Neural cluster profiles saved to: {neural_profile_path}")
    
    # GMM profiles
    gmm_enrichment = ClusterEnrichment()
    gmm_profiles = gmm_enrichment.enrich_clusters(
        customer_data_enriched, gmm_labels, gmm_centers
    )
    gmm_profile_path = output_dir / f"gmm_cluster_profile_{timestamp}.json"
    gmm_enrichment.export_for_ai_agent(str(gmm_profile_path))
    print(f"✓ GMM cluster profiles saved to: {gmm_profile_path}")
    
    # Main AI export (using Fuzzy as default)
    ai_export_path = data_dir / "customer_segments_for_ai.json"
    enrichment.export_for_ai_agent(str(ai_export_path))
    print(f"✓ Default AI segments (Fuzzy) saved to: {ai_export_path}")
    print()
    
    # Create customer-level export with cluster assignments (using enriched dataset)
    customer_export = customer_data_enriched.copy()
    customer_export['fuzzy_cluster'] = fuzzy_labels
    customer_export['neural_cluster'] = neural_labels
    customer_export['gmm_cluster'] = gmm_labels
    
    # Add membership degrees for fuzzy clustering
    for i in range(fuzzy_model.n_clusters):
        customer_export[f'fuzzy_membership_cluster_{i}'] = fuzzy_membership[i, :]
    
    # Add probabilities for GMM clustering
    for i in range(gmm_model.n_clusters):
        customer_export[f'gmm_probability_cluster_{i}'] = gmm_probabilities[:, i]
    
    # Add segment names
    segment_names = {cid: profile['segment_name'] 
                    for cid, profile in enriched_profiles.items()}
    customer_export['segment_name'] = customer_export['fuzzy_cluster'].map(segment_names)
    
    customers_with_segments_path = data_dir / "customers_with_segments.csv"
    customer_export.to_csv(customers_with_segments_path, index=False)
    print(f"Customer data with segment assignments saved to '{customers_with_segments_path}'")
    print()
    
    # Summary
    print("=" * 80)
    print("Pipeline Completed Successfully!")
    print("=" * 80)
    print("\nGenerated Files:")
    print(f"  1. {basic_data_path}")
    print(f"     → Basic customer data (51 columns, optimized for clustering)")
    print(f"  2. {enriched_data_path}")
    print(f"     → Enriched customer data (757 columns with dept/class/size features)")
    print(f"  3. {customers_with_segments_path}")
    print(f"     → Customers with all cluster assignments (Fuzzy, Neural, GMM)")
    print(f"  4. {ai_export_path}")
    print(f"     → Default AI segments (Fuzzy method)")
    print(f"  5. {output_dir}/")
    print(f"     → fuzzy_cluster_profile_{timestamp}.json")
    print(f"     → neural_cluster_profile_{timestamp}.json")
    print(f"     → gmm_cluster_profile_{timestamp}.json")
    print()
    print("Enriched Data Features:")
    dept_cols = [col for col in customer_data_enriched.columns if 'dept_total_value_' in col]
    class_cols = [col for col in customer_data_enriched.columns if 'class_total_value_' in col]
    size_cols = [col for col in customer_data_enriched.columns if 'count_' in col]
    print(f"  - Department metrics: {len(dept_cols)} value columns + {len([c for c in customer_data_enriched.columns if 'dept_total_units_' in c])} unit columns")
    print(f"  - Class metrics: {len(class_cols)} value columns + {len([c for c in customer_data_enriched.columns if 'class_total_units_' in c])} unit columns")
    print(f"  - Size/Age breakdowns: {len(size_cols)} columns")
    print()
    print("Clustering Methods Comparison:")
    print(f"  {'Method':<25} {'Silhouette Score':<20} {'Method-Specific Metrics'}")
    print(f"  {'-'*25} {'-'*20} {'-'*50}")
    print(f"  {'Fuzzy C-Means':<25} {fuzzy_metrics['silhouette_score']:>19.4f}  PC={fuzzy_metrics['partition_coefficient']:.4f}, PE={fuzzy_metrics['partition_entropy']:.4f}")
    print(f"  {'Neural Clustering':<25} {neural_metrics['silhouette_score']:>19.4f}  Recon. Error={neural_metrics['reconstruction_error']:.6f}")
    print(f"  {'GMM':<25} {gmm_metrics['silhouette_score']:>19.4f}  DB={gmm_metrics['davies_bouldin_index']:.4f}, CH={gmm_metrics['calinski_harabasz_score']:.2f}")
    print()
    print("  Notes:")
    print("    - Silhouette Score: Higher is better (range: -1 to 1)")
    print("    - PC (Partition Coefficient): Higher is better (range: 1/n_clusters to 1)")
    print("    - PE (Partition Entropy): Lower is better")
    print("    - Recon. Error (Reconstruction Error): Lower is better")
    print("    - DB (Davies-Bouldin Index): Lower is better")
    print("    - CH (Calinski-Harabasz Score): Higher is better")
    print()
    print("  Additional GMM Metrics:")
    print(f"    BIC (Bayesian Information Criterion): {gmm_metrics['bic']:.2f} (lower is better)")
    print(f"    AIC (Akaike Information Criterion): {gmm_metrics['aic']:.2f} (lower is better)")
    print(f"    Log Likelihood: {gmm_metrics['log_likelihood']:.2f} (higher is better)")
    print()
    print("Next Steps:")
    print("  - Review the enriched segment profiles in the JSON file")
    print("  - Use the segment data to inform AI agent interactions")
    print("  - Compare cluster assignments across all three methods")
    print("  - Customize interaction strategies based on business needs")
    print("  - Apply clustering to real customer data")
    print("  - Analyze persona distribution in enriched dataset")
    print()


if __name__ == '__main__':
    main()
