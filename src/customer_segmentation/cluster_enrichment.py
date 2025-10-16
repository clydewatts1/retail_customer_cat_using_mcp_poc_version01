"""
Cluster enrichment module for adding meaningful descriptions and metadata.
Enriches cluster data with human-readable descriptions for AI agent consumption.
"""
import numpy as np
import pandas as pd
from typing import Dict, List, Any


class ClusterEnrichment:
    """Enrich customer clusters with meaningful descriptions and metadata."""
    
    def __init__(self):
        """Initialize cluster enrichment."""
        self.cluster_profiles = {}
    
    def analyze_cluster_characteristics(self, data: pd.DataFrame, 
                                       cluster_labels: np.ndarray,
                                       cluster_centers: pd.DataFrame) -> Dict[int, Dict[str, Any]]:
        """
        Analyze characteristics of each cluster.
        
        Args:
            data: Original customer data
            cluster_labels: Cluster assignments for each customer
            cluster_centers: Cluster centers in original feature space
            
        Returns:
            Dictionary mapping cluster ID to characteristics
        """
        data_with_clusters = data.copy()
        data_with_clusters['cluster'] = cluster_labels
        
        characteristics = {}
        
        for cluster_id in range(len(cluster_centers)):
            cluster_data = data_with_clusters[data_with_clusters['cluster'] == cluster_id]
            
            if len(cluster_data) == 0:
                continue
            
            # Calculate statistics
            stats = {
                'size': len(cluster_data),
                'percentage': round(len(cluster_data) / len(data) * 100, 2),
                'avg_total_revenue': round(cluster_data['total_revenue'].mean(), 2),
                'avg_total_purchases': round(cluster_data['total_purchases'].mean(), 2),
                'avg_order_value': round(cluster_data['avg_order_value'].mean(), 2),
                'avg_recency_days': round(cluster_data['recency_days'].mean(), 2),
                'avg_frequency': round(cluster_data['frequency_per_month'].mean(), 2),
                'avg_lifetime_months': round(cluster_data['customer_lifetime_months'].mean(), 2),
                'avg_return_rate': round(cluster_data['return_rate'].mean(), 3)
            }
            
            characteristics[cluster_id] = stats
        
        return characteristics
    
    def generate_cluster_descriptions(self, characteristics: Dict[int, Dict[str, Any]]) -> Dict[int, str]:
        """
        Generate human-readable descriptions for each cluster.
        
        Args:
            characteristics: Cluster characteristics dictionary
            
        Returns:
            Dictionary mapping cluster ID to description
        """
        descriptions = {}
        
        for cluster_id, stats in characteristics.items():
            # Determine value tier
            if stats['avg_total_revenue'] > 15000:
                value_tier = "High-Value"
            elif stats['avg_total_revenue'] > 5000:
                value_tier = "Medium-Value"
            else:
                value_tier = "Low-Value"
            
            # Determine engagement level
            if stats['avg_frequency'] > 3:
                engagement = "Highly Engaged"
            elif stats['avg_frequency'] > 1:
                engagement = "Regularly Engaged"
            else:
                engagement = "Occasionally Engaged"
            
            # Determine recency status
            if stats['avg_recency_days'] < 30:
                recency_status = "Recent"
            elif stats['avg_recency_days'] < 90:
                recency_status = "Moderately Recent"
            else:
                recency_status = "At-Risk"
            
            # Generate description
            description = (
                f"{value_tier} {engagement} Customers ({recency_status}): "
                f"This segment represents {stats['percentage']}% of the customer base with "
                f"average revenue of ${stats['avg_total_revenue']:,.2f}. "
                f"They purchase approximately {stats['avg_frequency']:.1f} times per month "
                f"with an average order value of ${stats['avg_order_value']:.2f}. "
                f"Last purchase was {stats['avg_recency_days']:.0f} days ago on average."
            )
            
            descriptions[cluster_id] = description
        
        return descriptions
    
    def generate_segment_names(self, characteristics: Dict[int, Dict[str, Any]]) -> Dict[int, str]:
        """
        Generate short, memorable names for each segment.
        
        Args:
            characteristics: Cluster characteristics dictionary
            
        Returns:
            Dictionary mapping cluster ID to segment name
        """
        # Sort clusters by total revenue to assign names
        sorted_clusters = sorted(
            characteristics.items(),
            key=lambda x: x[1]['avg_total_revenue'],
            reverse=True
        )
        
        segment_names = {}
        
        for idx, (cluster_id, stats) in enumerate(sorted_clusters):
            if idx == 0:
                # Highest revenue cluster
                if stats['avg_recency_days'] < 30:
                    name = "VIP Champions"
                else:
                    name = "High-Value At-Risk"
            elif idx == 1:
                # Second highest
                if stats['avg_frequency'] > 2:
                    name = "Loyal Regulars"
                else:
                    name = "Potential Loyalists"
            elif idx == 2:
                # Third
                if stats['avg_recency_days'] < 60:
                    name = "Promising Customers"
                else:
                    name = "Need Attention"
            else:
                # Lowest revenue clusters
                if stats['avg_recency_days'] > 120:
                    name = "Hibernating"
                else:
                    name = "Price Sensitive"
            
            segment_names[cluster_id] = name
        
        return segment_names
    
    def generate_interaction_strategies(self, characteristics: Dict[int, Dict[str, Any]]) -> Dict[int, List[str]]:
        """
        Generate recommended interaction strategies for each segment.
        
        Args:
            characteristics: Cluster characteristics dictionary
            
        Returns:
            Dictionary mapping cluster ID to list of strategies
        """
        strategies = {}
        
        for cluster_id, stats in characteristics.items():
            cluster_strategies = []
            
            # Revenue-based strategies
            if stats['avg_total_revenue'] > 15000:
                cluster_strategies.extend([
                    "Provide premium customer service and dedicated account manager",
                    "Offer exclusive early access to new products",
                    "Create personalized shopping experiences"
                ])
            elif stats['avg_total_revenue'] > 5000:
                cluster_strategies.extend([
                    "Implement loyalty program with tiered rewards",
                    "Send personalized product recommendations",
                    "Offer bundle deals to increase order value"
                ])
            else:
                cluster_strategies.extend([
                    "Provide special discounts and promotions",
                    "Send educational content about product value",
                    "Create entry-level product bundles"
                ])
            
            # Frequency-based strategies
            if stats['avg_frequency'] < 1:
                cluster_strategies.append("Increase engagement through regular newsletters and updates")
            
            # Recency-based strategies
            if stats['avg_recency_days'] > 90:
                cluster_strategies.extend([
                    "Launch win-back campaign with special offers",
                    "Send re-engagement email sequence",
                    "Conduct customer feedback survey to understand concerns"
                ])
            
            # Return rate strategies
            if stats['avg_return_rate'] > 0.15:
                cluster_strategies.extend([
                    "Improve product descriptions and sizing guides",
                    "Offer virtual try-on or consultation services",
                    "Review product quality and customer expectations"
                ])
            
            strategies[cluster_id] = cluster_strategies
        
        return strategies
    
    def enrich_clusters(self, data: pd.DataFrame, cluster_labels: np.ndarray,
                       cluster_centers: pd.DataFrame) -> Dict[int, Dict[str, Any]]:
        """
        Perform complete cluster enrichment with descriptions and metadata.
        
        Args:
            data: Original customer data
            cluster_labels: Cluster assignments for each customer
            cluster_centers: Cluster centers in original feature space
            
        Returns:
            Enriched cluster profiles
        """
        # Analyze characteristics
        characteristics = self.analyze_cluster_characteristics(data, cluster_labels, cluster_centers)
        
        # Generate descriptions and metadata
        descriptions = self.generate_cluster_descriptions(characteristics)
        segment_names = self.generate_segment_names(characteristics)
        strategies = self.generate_interaction_strategies(characteristics)
        
        # Combine into enriched profiles
        for cluster_id in characteristics.keys():
            self.cluster_profiles[cluster_id] = {
                'segment_name': segment_names[cluster_id],
                'description': descriptions[cluster_id],
                'characteristics': characteristics[cluster_id],
                'interaction_strategies': strategies[cluster_id],
                'cluster_id': cluster_id
            }
        
        return self.cluster_profiles
    
    def export_for_ai_agent(self, output_path: str):
        """
        Export enriched cluster data in format suitable for AI agent consumption.
        
        Args:
            output_path: Path to save the export file
        """
        if not self.cluster_profiles:
            raise ValueError("No cluster profiles to export. Run enrich_clusters first.")
        
        # Create structured export
        export_data = {
            'cluster_profiles': self.cluster_profiles,
            'metadata': {
                'n_clusters': len(self.cluster_profiles),
                'total_customers': sum(p['characteristics']['size'] for p in self.cluster_profiles.values())
            }
        }
        
        # Save as JSON for easy AI agent consumption
        import json
        with open(output_path, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        print(f"Enriched cluster data exported to {output_path}")
