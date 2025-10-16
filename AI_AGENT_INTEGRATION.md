# AI Agent Integration Guide

This guide explains how to use the customer segmentation results with AI agents for enhanced customer interactions.

## Overview

The customer segmentation POC generates enriched cluster profiles that can be consumed by AI agents to provide personalized customer interactions. The system outputs data in JSON format that includes:

- Segment names and descriptions
- Customer characteristics
- Recommended interaction strategies
- Individual customer segment assignments

## Output Files for AI Agents

### 1. customer_segments_for_ai.json

This file contains enriched segment profiles:

```json
{
  "cluster_profiles": {
    "0": {
      "segment_name": "Hibernating",
      "description": "Low-Value Occasionally Engaged Customers (At-Risk)...",
      "characteristics": {
        "size": 79,
        "percentage": 15.8,
        "avg_total_revenue": 114.10,
        ...
      },
      "interaction_strategies": [
        "Launch win-back campaign with special offers",
        "Send re-engagement email sequence",
        ...
      ]
    }
  }
}
```

### 2. customers_with_segments.csv

Individual customer data with segment assignments:

- Customer ID
- All original features (purchases, revenue, etc.)
- Fuzzy cluster assignment
- Neural cluster assignment
- Fuzzy membership degrees for each cluster
- Segment name

## Integration Examples

### Example 1: Customer Service AI Agent

```python
import json
import pandas as pd

# Load segment profiles
with open('data/customer_segments_for_ai.json', 'r') as f:
    segments = json.load(f)

# Load customer data with segments
customers = pd.read_csv('data/customers_with_segments.csv')

def get_customer_context(customer_id):
    """Get relevant context for AI agent interaction."""
    customer = customers[customers['customer_id'] == customer_id].iloc[0]
    segment_id = int(customer['fuzzy_cluster'])
    segment_profile = segments['cluster_profiles'][str(segment_id)]
    
    context = {
        'customer_id': customer_id,
        'segment': segment_profile['segment_name'],
        'description': segment_profile['description'],
        'strategies': segment_profile['interaction_strategies'],
        'recent_activity': {
            'days_since_purchase': customer['recency_days'],
            'total_revenue': customer['total_revenue'],
            'avg_order_value': customer['avg_order_value']
        }
    }
    
    return context

# Use in AI agent prompt
customer_context = get_customer_context('CUST_00123')
prompt = f"""
You are a customer service AI agent. Here's information about the customer:

Segment: {customer_context['segment']}
{customer_context['description']}

Last purchase: {customer_context['recent_activity']['days_since_purchase']} days ago
Total lifetime value: ${customer_context['recent_activity']['total_revenue']:,.2f}

Recommended strategies:
{chr(10).join(f'- {s}' for s in customer_context['strategies'][:3])}

Based on this information, help the customer with their inquiry.
"""
```

### Example 2: Marketing Campaign AI Agent

```python
def generate_campaign_recommendations():
    """Generate targeted campaigns for each segment."""
    with open('data/customer_segments_for_ai.json', 'r') as f:
        segments = json.load(f)
    
    campaigns = {}
    for cluster_id, profile in segments['cluster_profiles'].items():
        segment_name = profile['segment_name']
        
        campaign = {
            'segment': segment_name,
            'target_size': profile['characteristics']['size'],
            'message_tone': 'urgent' if 'At-Risk' in profile['description'] else 'appreciation',
            'offer_type': profile['interaction_strategies'][0],
            'expected_revenue_per_customer': profile['characteristics']['avg_total_revenue'],
            'priority': 'high' if profile['characteristics']['avg_recency_days'] > 90 else 'medium'
        }
        
        campaigns[segment_name] = campaign
    
    return campaigns
```

### Example 3: Personalized Product Recommendation

```python
def get_personalized_recommendations(customer_id):
    """Get product recommendations based on segment."""
    customer = customers[customers['customer_id'] == customer_id].iloc[0]
    segment_id = int(customer['fuzzy_cluster'])
    segment_profile = segments['cluster_profiles'][str(segment_id)]
    
    # High-value customers
    if 'VIP' in segment_profile['segment_name']:
        return {
            'products': 'premium_collection',
            'price_range': 'high',
            'message': 'Exclusive new arrivals just for you',
            'discount': 0  # No discount needed
        }
    
    # At-risk customers
    elif 'Hibernating' in segment_profile['segment_name']:
        return {
            'products': 'best_sellers',
            'price_range': 'medium',
            'message': 'We miss you! Here\'s a special offer',
            'discount': 20  # Aggressive discount
        }
    
    # Regular customers
    else:
        return {
            'products': 'new_arrivals',
            'price_range': 'medium',
            'message': 'Check out what\'s new',
            'discount': 10  # Moderate discount
        }
```

### Example 4: Chatbot Context Enhancement

```python
class CustomerServiceChatbot:
    """Enhanced chatbot with customer segmentation."""
    
    def __init__(self):
        with open('data/customer_segments_for_ai.json', 'r') as f:
            self.segments = json.load(f)
        self.customers = pd.read_csv('data/customers_with_segments.csv')
    
    def get_response(self, customer_id, message):
        """Generate contextual response based on segment."""
        # Get customer segment
        customer = self.customers[self.customers['customer_id'] == customer_id].iloc[0]
        segment_id = int(customer['fuzzy_cluster'])
        segment = self.segments['cluster_profiles'][str(segment_id)]
        
        # Build context
        context = f"""
        Customer Segment: {segment['segment_name']}
        Purchase Frequency: {customer['frequency_per_month']:.1f} per month
        Last Purchase: {customer['recency_days']} days ago
        Avg Order Value: ${customer['avg_order_value']:.2f}
        
        Recommended Approach: {segment['interaction_strategies'][0]}
        """
        
        # Use context in AI model (pseudo-code)
        # response = ai_model.generate(message, context)
        
        return context  # In real implementation, return AI response
```

## Best Practices

### 1. Regular Updates
- Re-run clustering periodically (weekly/monthly)
- Update segment profiles as customer behavior changes
- Track segment migration patterns

### 2. Segment-Specific Strategies
- Tailor communication tone to segment characteristics
- Adjust offer aggressiveness based on recency and value
- Prioritize high-value at-risk customers

### 3. Privacy and Ethics
- Ensure customer data is handled securely
- Use segments for helpful personalization, not manipulation
- Provide opt-out options for personalized communications

### 4. Performance Tracking
- Monitor conversion rates by segment
- Track segment-specific metrics (retention, lifetime value)
- A/B test segment-based strategies

## Integration Checklist

- [ ] Load segment profiles from JSON
- [ ] Map customer IDs to segments
- [ ] Implement segment-specific logic in AI agent
- [ ] Test with sample customers from each segment
- [ ] Monitor AI agent performance by segment
- [ ] Set up automated re-clustering pipeline
- [ ] Implement feedback loop for strategy refinement

## Support

For integration assistance or questions, please open an issue on GitHub.
