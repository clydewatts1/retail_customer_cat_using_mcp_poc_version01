"""
Example demonstrating the complete customer segmentation pipeline.
This script shows how to:
1. Generate synthetic retail customer data
2. Perform fuzzy clustering
3. Perform neural network clustering
4. Enrich clusters with meaningful descriptions
5. Export data for AI agent interaction

All parameters are loaded from config.yml.
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
    print("Customer Segmentation POC - Complete Pipeline")
    print("=" * 80)
    print(f"Configuration loaded from: {config_path}")
    print()
    
    # Step 1: Generate synthetic data with enriched features
    print("Step 1: Generating synthetic retail customer data with enriched features...")
    
    # Get data generation parameters from config
    num_customers = config.data_generation['n_customers']
    seed = config.data_generation['random_seed']
    
    data_generator = RetailDataGenerator(seed=seed)
    customer_data = data_generator.generate_customer_data(n_customers=num_customers)
    
    # Save enriched data using config paths
    data_dir = Path(__file__).parent.parent / config.paths['data_dir']
    data_dir.mkdir(parents=True, exist_ok=True)
    enriched_data_path = data_dir / "customer_sales_data_enriched.csv"
    data_generator.save_data(customer_data, str(enriched_data_path))
    
    print(f"Generated {len(customer_data)} customer records")
    print(f"Features: {list(customer_data.columns)}")
    print(f"Enriched features include department/class totals and size breakdowns")
    print()
    
    # Display sample data
    print("Sample data (first 5 customers):")
    print(customer_data.head())
    print()

    # Show sample of enriched columns
    enriched_cols = [col for col in customer_data.columns if 'dept_total_value' in col or 'class_total_value' in col or 'count_' in col]
    print("Sample of enriched columns (first 5 customers):")
    print(customer_data[enriched_cols].head())
    print()
    
    # Step 2: Fuzzy Clustering
    print("=" * 80)
    print("Step 2: Performing Fuzzy C-Means Clustering...")
    print("=" * 80)
    
    # Get fuzzy clustering parameters from config
    fuzzy_params = config.fuzzy_clustering
    fuzzy_model = FuzzyCustomerSegmentation(
        n_clusters=fuzzy_params.get('n_clusters', 4),
        m=fuzzy_params.get('fuzziness_parameter', 2.0),
        seed=seed
    )
    fuzzy_labels, fuzzy_membership = fuzzy_model.fit_predict(customer_data)
    
    print(f"Fuzzy clustering completed with {fuzzy_model.n_clusters} clusters")
    print()
    
    # Evaluate fuzzy clustering
    fuzzy_metrics = fuzzy_model.evaluate(customer_data)
    print("Fuzzy Clustering Metrics:")
    for metric, value in fuzzy_metrics.items():
        print(f"  {metric}: {value:.4f}")
    print()
    
    # Get cluster centers
    fuzzy_centers = fuzzy_model.get_cluster_centers()
    print("Fuzzy Cluster Centers:")
    print(fuzzy_centers)
    print()
    
    # Step 3: Neural Network Clustering
    print("=" * 80)
    print("Step 3: Performing Neural Network Clustering...")
    print("=" * 80)
    
    # Get neural clustering parameters from config
    neural_params = config.neural_clustering
    neural_model = NeuralCustomerSegmentation(
        n_clusters=neural_params.get('n_clusters', 4),
        encoding_dim=neural_params.get('encoding_dim', 10),
        epochs=neural_params.get('epochs', 50),
        batch_size=neural_params.get('batch_size', 32),
        seed=seed
    )
    neural_labels = neural_model.fit_predict(customer_data, verbose=0)
    
    print(f"Neural clustering completed with {neural_model.n_clusters} clusters")
    print()
    
    # Evaluate neural clustering
    neural_metrics = neural_model.evaluate(customer_data)
    print("Neural Clustering Metrics:")
    for metric, value in neural_metrics.items():
        print(f"  {metric}: {value:.4f}")
    print()
    
    # Get cluster centers
    neural_centers = neural_model.get_cluster_centers(customer_data)
    print("Neural Cluster Centers:")
    print(neural_centers)
    print()
    
    # Step 4: Cluster Enrichment (using fuzzy clustering results)
    print("=" * 80)
    print("Step 4: Enriching Clusters with Meaningful Descriptions...")
    print("=" * 80)
    
    enrichment = ClusterEnrichment()
    enriched_profiles = enrichment.enrich_clusters(
        customer_data, fuzzy_labels, fuzzy_centers
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
        segment_data = customer_data[fuzzy_labels == cluster_id]
        
        # Department preferences
        dept_cols = [col for col in customer_data.columns if 'dept_total_value_' in col]
        dept_avg = segment_data[dept_cols].mean()
        top_dept = dept_avg.nlargest(3)
        print(f"\nTop Departments by Value:")
        for dept_col, value in top_dept.items():
            dept_name = dept_col.replace('dept_total_value_', '')
            print(f"  - {dept_name}: ${value:.2f}")
        
        # Class preferences
        class_cols = [col for col in customer_data.columns if 'class_total_value_' in col]
        class_avg = segment_data[class_cols].mean()
        top_class = class_avg.nlargest(3)
        print(f"\nTop Classes by Value:")
        for class_col, value in top_class.items():
            class_name = class_col.replace('class_total_value_', '')
            print(f"  - {class_name}: ${value:.2f}")
        
        # Size breakdown
        size_cols = [col for col in customer_data.columns if 'count_' in col]
        size_avg = segment_data[size_cols].mean()
        print(f"\nAverage Size/Age Breakdown:")
        for size_col, count in size_avg.items():
            size_name = size_col.replace('count_', '').replace('count_size_', 'Size ')
            print(f"  - {size_name}: {count:.1f} items")
        
        print(f"\nRecommended Interaction Strategies:")
        for strategy in profile['interaction_strategies'][:3]:  # Show top 3
            print(f"  • {strategy}")
        print()
    
    # Step 5: Export for AI Agent
    print("=" * 80)
    print("Step 5: Exporting Data for AI Agent Interaction...")
    print("=" * 80)
    
    # Export using config path
    ai_export_path = data_dir / "customer_segments_for_ai.json"
    enrichment.export_for_ai_agent(str(ai_export_path))
    print()
    
    # Create customer-level export with cluster assignments
    customer_export = customer_data.copy()
    customer_export['fuzzy_cluster'] = fuzzy_labels
    customer_export['neural_cluster'] = neural_labels
    
    # Add membership degrees for fuzzy clustering
    for i in range(fuzzy_model.n_clusters):
        customer_export[f'fuzzy_membership_cluster_{i}'] = fuzzy_membership[i, :]
    
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
    print(f"  1. {enriched_data_path} - Enriched customer data with dept/class/size features")
    print(f"  2. {customers_with_segments_path} - Customers with cluster assignments")
    print(f"  3. {ai_export_path} - Enriched segments for AI agents")
    print()
    print("Enriched Data Features:")
    dept_cols = [col for col in customer_data.columns if 'dept_total_value_' in col]
    class_cols = [col for col in customer_data.columns if 'class_total_value_' in col]
    size_cols = [col for col in customer_data.columns if 'count_' in col]
    print(f"  - Department metrics: {len(dept_cols)} value columns + {len([c for c in customer_data.columns if 'dept_total_units_' in c])} unit columns")
    print(f"  - Class metrics: {len(class_cols)} value columns + {len([c for c in customer_data.columns if 'class_total_units_' in c])} unit columns")
    print(f"  - Size/Age breakdowns: {len(size_cols)} columns")
    print()
    print("Clustering Comparison:")
    print(f"  Fuzzy C-Means Silhouette Score: {fuzzy_metrics['silhouette_score']:.4f}")
    print(f"  Neural Clustering Silhouette Score: {neural_metrics['silhouette_score']:.4f}")
    print()
    print("Next Steps:")
    print("  - Review the enriched segment profiles in the JSON file")
    print("  - Use the segment data to inform AI agent interactions")
    print("  - Customize interaction strategies based on business needs")
    print("  - Apply clustering to real customer data")
    print()


if __name__ == '__main__':
    main()
