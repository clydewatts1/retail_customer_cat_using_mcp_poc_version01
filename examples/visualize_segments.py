"""
Visualization example for customer segmentation results.
Creates plots to visualize clusters and their characteristics.
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from customer_segmentation import (
    RetailDataGenerator,
    FuzzyCustomerSegmentation
)
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def plot_cluster_distribution(data, cluster_labels, enriched_profiles):
    """Plot distribution of customers across clusters."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Count plot
    cluster_counts = pd.Series(cluster_labels).value_counts().sort_index()
    segment_names = [enriched_profiles[i]['segment_name'] for i in cluster_counts.index]
    
    ax1.bar(range(len(cluster_counts)), cluster_counts.values, color='steelblue', alpha=0.7)
    ax1.set_xticks(range(len(cluster_counts)))
    ax1.set_xticklabels(segment_names, rotation=45, ha='right')
    ax1.set_ylabel('Number of Customers')
    ax1.set_title('Customer Distribution Across Segments')
    ax1.grid(axis='y', alpha=0.3)
    
    # Pie chart
    ax2.pie(cluster_counts.values, labels=segment_names, autopct='%1.1f%%',
            startangle=90, colors=sns.color_palette('Set2', len(cluster_counts)))
    ax2.set_title('Segment Percentage Distribution')
    
    plt.tight_layout()
    return fig


def plot_segment_characteristics(data, cluster_labels, enriched_profiles):
    """Plot key characteristics by segment."""
    data_with_clusters = data.copy()
    data_with_clusters['cluster'] = cluster_labels
    data_with_clusters['segment_name'] = data_with_clusters['cluster'].map(
        {i: enriched_profiles[i]['segment_name'] for i in enriched_profiles.keys()}
    )
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # Total Revenue
    ax = axes[0, 0]
    segment_revenue = data_with_clusters.groupby('segment_name')['total_revenue'].mean().sort_values()
    segment_revenue.plot(kind='barh', ax=ax, color='green', alpha=0.7)
    ax.set_xlabel('Average Total Revenue ($)')
    ax.set_title('Average Revenue by Segment')
    ax.grid(axis='x', alpha=0.3)
    
    # Purchase Frequency
    ax = axes[0, 1]
    segment_freq = data_with_clusters.groupby('segment_name')['frequency_per_month'].mean().sort_values()
    segment_freq.plot(kind='barh', ax=ax, color='blue', alpha=0.7)
    ax.set_xlabel('Purchases per Month')
    ax.set_title('Average Purchase Frequency by Segment')
    ax.grid(axis='x', alpha=0.3)
    
    # Recency
    ax = axes[1, 0]
    segment_recency = data_with_clusters.groupby('segment_name')['recency_days'].mean().sort_values()
    segment_recency.plot(kind='barh', ax=ax, color='orange', alpha=0.7)
    ax.set_xlabel('Days Since Last Purchase')
    ax.set_title('Average Recency by Segment')
    ax.grid(axis='x', alpha=0.3)
    
    # Average Order Value
    ax = axes[1, 1]
    segment_aov = data_with_clusters.groupby('segment_name')['avg_order_value'].mean().sort_values()
    segment_aov.plot(kind='barh', ax=ax, color='purple', alpha=0.7)
    ax.set_xlabel('Average Order Value ($)')
    ax.set_title('Average Order Value by Segment')
    ax.grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    return fig


def plot_rfm_scatter(data, cluster_labels, enriched_profiles):
    """Create RFM scatter plots."""
    data_with_clusters = data.copy()
    data_with_clusters['cluster'] = cluster_labels
    data_with_clusters['segment_name'] = data_with_clusters['cluster'].map(
        {i: enriched_profiles[i]['segment_name'] for i in enriched_profiles.keys()}
    )
    
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    
    # Recency vs Frequency
    ax = axes[0]
    for segment in data_with_clusters['segment_name'].unique():
        segment_data = data_with_clusters[data_with_clusters['segment_name'] == segment]
        ax.scatter(segment_data['recency_days'], segment_data['frequency_per_month'],
                  label=segment, alpha=0.6, s=50)
    ax.set_xlabel('Recency (Days Since Last Purchase)')
    ax.set_ylabel('Frequency (Purchases per Month)')
    ax.set_title('Recency vs Frequency by Segment')
    ax.legend()
    ax.grid(alpha=0.3)
    
    # Frequency vs Monetary
    ax = axes[1]
    for segment in data_with_clusters['segment_name'].unique():
        segment_data = data_with_clusters[data_with_clusters['segment_name'] == segment]
        ax.scatter(segment_data['frequency_per_month'], segment_data['total_revenue'],
                  label=segment, alpha=0.6, s=50)
    ax.set_xlabel('Frequency (Purchases per Month)')
    ax.set_ylabel('Monetary (Total Revenue $)')
    ax.set_title('Frequency vs Monetary by Segment')
    ax.legend()
    ax.grid(alpha=0.3)
    
    plt.tight_layout()
    return fig


def plot_membership_heatmap(membership_matrix, enriched_profiles, sample_size=50):
    """Plot fuzzy membership heatmap for sample customers."""
    # Sample customers for visualization
    sample_indices = np.random.choice(membership_matrix.shape[1], 
                                     min(sample_size, membership_matrix.shape[1]), 
                                     replace=False)
    sample_membership = membership_matrix[:, sample_indices]
    
    segment_names = [enriched_profiles[i]['segment_name'] 
                    for i in range(len(enriched_profiles))]
    
    fig, ax = plt.subplots(figsize=(12, 6))
    im = ax.imshow(sample_membership, cmap='YlOrRd', aspect='auto')
    
    ax.set_yticks(range(len(segment_names)))
    ax.set_yticklabels(segment_names)
    ax.set_xlabel('Customer Sample')
    ax.set_ylabel('Segment')
    ax.set_title(f'Fuzzy Membership Matrix (Sample of {len(sample_indices)} Customers)')
    
    plt.colorbar(im, ax=ax, label='Membership Degree')
    plt.tight_layout()
    return fig


def main():
    """Generate and visualize customer segmentation."""
    print("Generating customer data and performing segmentation...")
    
    # Generate data
    generator = RetailDataGenerator(seed=42)
    customer_data = generator.generate_customer_data(n_customers=500)
    
    # Perform fuzzy clustering
    from customer_segmentation import ClusterEnrichment
    
    fuzzy_model = FuzzyCustomerSegmentation(n_clusters=4, m=2.0, seed=42)
    cluster_labels, membership_matrix = fuzzy_model.fit_predict(customer_data)
    
    # Enrich clusters
    enrichment = ClusterEnrichment()
    cluster_centers = fuzzy_model.get_cluster_centers()
    enriched_profiles = enrichment.enrich_clusters(customer_data, cluster_labels, cluster_centers)
    
    print("Creating visualizations...")
    
    # Create output directory
    os.makedirs('../visualizations', exist_ok=True)
    
    # Generate plots
    fig1 = plot_cluster_distribution(customer_data, cluster_labels, enriched_profiles)
    fig1.savefig('../visualizations/cluster_distribution.png', dpi=150, bbox_inches='tight')
    print("✓ Saved: cluster_distribution.png")
    
    fig2 = plot_segment_characteristics(customer_data, cluster_labels, enriched_profiles)
    fig2.savefig('../visualizations/segment_characteristics.png', dpi=150, bbox_inches='tight')
    print("✓ Saved: segment_characteristics.png")
    
    fig3 = plot_rfm_scatter(customer_data, cluster_labels, enriched_profiles)
    fig3.savefig('../visualizations/rfm_scatter.png', dpi=150, bbox_inches='tight')
    print("✓ Saved: rfm_scatter.png")
    
    fig4 = plot_membership_heatmap(membership_matrix, enriched_profiles, sample_size=50)
    fig4.savefig('../visualizations/membership_heatmap.png', dpi=150, bbox_inches='tight')
    print("✓ Saved: membership_heatmap.png")
    
    print("\nAll visualizations saved to ../visualizations/")
    print("\nVisualization Summary:")
    print("  1. cluster_distribution.png - Shows how customers are distributed across segments")
    print("  2. segment_characteristics.png - Compares key metrics across segments")
    print("  3. rfm_scatter.png - RFM analysis scatter plots")
    print("  4. membership_heatmap.png - Fuzzy membership degrees for sample customers")


if __name__ == '__main__':
    main()
