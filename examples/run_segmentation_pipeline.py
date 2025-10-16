"""
Example demonstrating the complete customer segmentation pipeline.
This script shows how to:
1. Generate synthetic retail customer data
2. Perform fuzzy clustering
3. Perform neural network clustering
4. Enrich clusters with meaningful descriptions
5. Export data for AI agent interaction
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from customer_segmentation import (
    RetailDataGenerator,
    FuzzyCustomerSegmentation,
    NeuralCustomerSegmentation,
    ClusterEnrichment
)
import pandas as pd
import numpy as np


def main():
    """Run the complete customer segmentation pipeline."""
    
    print("=" * 80)
    print("Customer Segmentation POC - Complete Pipeline")
    print("=" * 80)
    print()
    
    # Step 1: Generate synthetic data
    print("Step 1: Generating synthetic retail customer data...")
    data_generator = RetailDataGenerator(seed=42)
    customer_data = data_generator.generate_customer_data(n_customers=500)
    
    # Save data
    os.makedirs('../data', exist_ok=True)
    data_generator.save_data(customer_data, '../data/customer_sales_data.csv')
    
    print(f"Generated {len(customer_data)} customer records")
    print(f"Features: {list(customer_data.columns)}")
    print()
    
    # Display sample data
    print("Sample data (first 5 customers):")
    print(customer_data.head())
    print()
    
    # Step 2: Fuzzy Clustering
    print("=" * 80)
    print("Step 2: Performing Fuzzy C-Means Clustering...")
    print("=" * 80)
    
    fuzzy_model = FuzzyCustomerSegmentation(n_clusters=4, m=2.0, seed=42)
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
    
    neural_model = NeuralCustomerSegmentation(n_clusters=4, encoding_dim=10, 
                                              epochs=50, batch_size=32, seed=42)
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
        print(f"\nRecommended Interaction Strategies:")
        for strategy in profile['interaction_strategies'][:3]:  # Show top 3
            print(f"  • {strategy}")
        print()
    
    # Step 5: Export for AI Agent
    print("=" * 80)
    print("Step 5: Exporting Data for AI Agent Interaction...")
    print("=" * 80)
    
    enrichment.export_for_ai_agent('../data/customer_segments_for_ai.json')
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
    
    customer_export.to_csv('../data/customers_with_segments.csv', index=False)
    print("Customer data with segment assignments saved to '../data/customers_with_segments.csv'")
    print()
    
    # Summary
    print("=" * 80)
    print("Pipeline Completed Successfully!")
    print("=" * 80)
    print("\nGenerated Files:")
    print("  1. data/customer_sales_data.csv - Original customer data")
    print("  2. data/customers_with_segments.csv - Customers with cluster assignments")
    print("  3. data/customer_segments_for_ai.json - Enriched segments for AI agents")
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
