"""
Visualization example for customer segmentation results.
Creates plots to visualize clusters and their characteristics.
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
    ClusterEnrichment,
    get_config
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


def plot_department_preferences(data, cluster_labels, enriched_profiles):
    """Plot department preferences by segment."""
    data_with_clusters = data.copy()
    data_with_clusters['cluster'] = cluster_labels
    data_with_clusters['segment_name'] = data_with_clusters['cluster'].map(
        {i: enriched_profiles[i]['segment_name'] for i in enriched_profiles.keys()}
    )
    
    # Get department value columns
    dept_cols = [col for col in data.columns if 'dept_total_value_' in col]
    
    if not dept_cols:
        print("No department columns found")
        return None
    
    # Calculate average department spending by segment
    dept_data = []
    for segment in data_with_clusters['segment_name'].unique():
        segment_data = data_with_clusters[data_with_clusters['segment_name'] == segment]
        for col in dept_cols:
            dept_name = col.replace('dept_total_value_', '')
            avg_value = segment_data[col].mean()
            dept_data.append({
                'Segment': segment,
                'Department': dept_name,
                'Average Value': avg_value
            })
    
    dept_df = pd.DataFrame(dept_data)
    
    # Create grouped bar chart
    fig, ax = plt.subplots(figsize=(14, 6))
    segments = dept_df['Segment'].unique()
    departments = dept_df['Department'].unique()
    x = np.arange(len(departments))
    width = 0.8 / len(segments)
    
    for i, segment in enumerate(segments):
        segment_values = dept_df[dept_df['Segment'] == segment]['Average Value'].values
        ax.bar(x + i * width, segment_values, width, label=segment, alpha=0.8)
    
    ax.set_xlabel('Department')
    ax.set_ylabel('Average Spending ($)')
    ax.set_title('Department Spending by Customer Segment')
    ax.set_xticks(x + width * (len(segments) - 1) / 2)
    ax.set_xticklabels(departments, rotation=45, ha='right')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    return fig


def plot_size_distribution(data, cluster_labels, enriched_profiles):
    """Plot size/age distribution by segment."""
    data_with_clusters = data.copy()
    data_with_clusters['cluster'] = cluster_labels
    data_with_clusters['segment_name'] = data_with_clusters['cluster'].map(
        {i: enriched_profiles[i]['segment_name'] for i in enriched_profiles.keys()}
    )
    
    # Get size/age columns
    size_cols = [col for col in data.columns if 'count_' in col]
    
    if not size_cols:
        print("No size/age columns found")
        return None
    
    # Calculate average counts by segment
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    
    # Child ages
    child_cols = [col for col in size_cols if 'count_Baby' in col or 'count_Child' in col]
    if child_cols:
        ax = axes[0]
        segment_child_data = data_with_clusters.groupby('segment_name')[child_cols].mean()
        segment_child_data.columns = [col.replace('count_', '') for col in segment_child_data.columns]
        segment_child_data.plot(kind='bar', ax=ax, alpha=0.7, rot=45)
        ax.set_xlabel('Segment')
        ax.set_ylabel('Average Count')
        ax.set_title('Child Age Distribution by Segment')
        ax.legend(title='Age Group')
        ax.grid(axis='y', alpha=0.3)
    
    # Adult sizes
    adult_cols = [col for col in size_cols if 'count_size_' in col]
    if adult_cols:
        ax = axes[1]
        segment_adult_data = data_with_clusters.groupby('segment_name')[adult_cols].mean()
        segment_adult_data.columns = [col.replace('count_size_', '') for col in segment_adult_data.columns]
        segment_adult_data.plot(kind='bar', ax=ax, alpha=0.7, rot=45)
        ax.set_xlabel('Segment')
        ax.set_ylabel('Average Count')
        ax.set_title('Adult Size Distribution by Segment')
        ax.legend(title='Size')
        ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    return fig


def main():
    """Generate and visualize customer segmentation."""
    
    # Load configuration
    config_path = Path(__file__).parent.parent / "config" / "config.yml"
    config = get_config(str(config_path))
    
    print("Generating enriched customer data and performing segmentation...")
    print(f"Configuration loaded from: {config_path}")
    print(f"Current working directory: {os.getcwd()}")
    
    # Get parameters from config
    num_customers = config.data_generation['n_customers']
    seed = config.data_generation['random_seed']
    fuzzy_params = config.fuzzy_clustering
    
    # Generate enriched data
    faker_cfg = config.data_generation.get('faker', {}) if isinstance(config.data_generation, dict) else {}
    generator = RetailDataGenerator(
        seed=seed,
        faker_enabled=faker_cfg.get('enabled', True),
        faker_locale=faker_cfg.get('locale', 'en_US')
    )
    customer_data = generator.generate_customer_data(n_customers=num_customers)
    
    # Save enriched data using config paths
    data_dir = Path(__file__).parent.parent / config.paths['data_dir']
    data_dir.mkdir(parents=True, exist_ok=True)
    enriched_data_path = data_dir / "customer_sales_data_enriched.csv"
    generator.save_data(customer_data, str(enriched_data_path))
    print(f"Generated {len(customer_data)} customer records with enriched features")
    
    # Perform fuzzy clustering with config parameters
    fuzzy_model = FuzzyCustomerSegmentation(
        n_clusters=fuzzy_params.get('n_clusters', 4),
        m=fuzzy_params.get('fuzziness_parameter', 2.0),
        seed=seed
    )
    cluster_labels, membership_matrix = fuzzy_model.fit_predict(customer_data)
    
    # Enrich clusters
    enrichment = ClusterEnrichment()
    cluster_centers = fuzzy_model.get_cluster_centers()
    enriched_profiles = enrichment.enrich_clusters(customer_data, cluster_labels, cluster_centers)
    
    print("Creating visualizations...")
    
    # Create output directory using config path
    viz_dir = Path(__file__).parent.parent / config.paths['visualizations_dir']
    viz_dir.mkdir(parents=True, exist_ok=True)
    
    # Get visualization settings from config
    viz_config = config.visualization
    dpi = viz_config.get('dpi', 150)
    format = viz_config.get('figure_format', 'png')
    
    # Generate plots
    fig1 = plot_cluster_distribution(customer_data, cluster_labels, enriched_profiles)
    output_path = viz_dir / f"cluster_distribution.{format}"
    fig1.savefig(output_path, dpi=dpi, bbox_inches='tight')
    print(f"✓ Saved: {output_path}")
    
    fig2 = plot_segment_characteristics(customer_data, cluster_labels, enriched_profiles)
    output_path = viz_dir / f"segment_characteristics.{format}"
    fig2.savefig(output_path, dpi=dpi, bbox_inches='tight')
    print(f"✓ Saved: {output_path}")
    
    fig3 = plot_rfm_scatter(customer_data, cluster_labels, enriched_profiles)
    output_path = viz_dir / f"rfm_scatter.{format}"
    fig3.savefig(output_path, dpi=dpi, bbox_inches='tight')
    print(f"✓ Saved: {output_path}")
    
    fig4 = plot_membership_heatmap(membership_matrix, enriched_profiles, sample_size=50)
    output_path = viz_dir / f"membership_heatmap.{format}"
    fig4.savefig(output_path, dpi=dpi, bbox_inches='tight')
    print(f"✓ Saved: {output_path}")
    
    fig5 = plot_department_preferences(customer_data, cluster_labels, enriched_profiles)
    if fig5:
        output_path = viz_dir / f"department_preferences.{format}"
        fig5.savefig(output_path, dpi=dpi, bbox_inches='tight')
        print(f"✓ Saved: {output_path}")
    
    fig6 = plot_size_distribution(customer_data, cluster_labels, enriched_profiles)
    if fig6:
        output_path = viz_dir / f"size_distribution.{format}"
        fig6.savefig(output_path, dpi=dpi, bbox_inches='tight')
        print(f"✓ Saved: {output_path}")
    
    print(f"\nAll visualizations saved to {viz_dir}")
    print("\nVisualization Summary:")
    print("  1. cluster_distribution - Shows how customers are distributed across segments")
    print("  2. segment_characteristics - Compares key metrics across segments")
    print("  3. rfm_scatter - RFM analysis scatter plots")
    print("  4. membership_heatmap - Fuzzy membership degrees for sample customers")
    print("  5. department_preferences - Department spending patterns by segment")
    print("  6. size_distribution - Size/age breakdown by segment")
    print(f"\nEnriched data includes department/class totals and size breakdowns")
    print(f"Configuration: {num_customers} customers, {fuzzy_params.get('n_clusters', 4)} clusters, seed={seed}")


if __name__ == '__main__':
    main()
