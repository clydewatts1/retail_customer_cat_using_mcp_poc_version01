# Cluster Profile Export for AI LLM Analysis

## Overview

All three clustering methods (Fuzzy C-Means, Neural Network, and GMM) now export comprehensive cluster profiles in JSON and YAML formats. These structured files are designed to be consumed by AI Large Language Models (LLMs) for generating business insights, customer segment descriptions, and marketing recommendations.

---

## What's Exported

Each clustering method generates two files:
1. **JSON file**: Machine-readable format for programmatic access
2. **YAML file**: Human-readable format for review and editing

### File Naming Convention
```
{method}_cluster_profile_{timestamp}.{format}

Examples:
- fuzzy_cluster_profile_20251017_054128.json
- neural_cluster_profile_20251017_054133.yaml
- gmm_cluster_profile_20251017_054133.json
```

---

## Profile Structure

### Common Metadata (All Methods)
```json
{
  "metadata": {
    "method": "Method name",
    "timestamp": "ISO 8601 timestamp",
    "n_clusters": 4,
    "n_samples": 500,
    ...method-specific parameters...
  },
  "metrics": {
    ...clustering quality metrics...
  },
  "features_used": ["feature1", "feature2", ...],
  "clusters": {
    "cluster_0": {...},
    "cluster_1": {...},
    ...
  }
}
```

### Per-Cluster Information
Each cluster contains:
```json
{
  "cluster_id": 0,
  "size": 150,
  "percentage": 30.0,
  "cluster_center": {
    "total_revenue": 3500.50,
    "recency_days": 15.3,
    ...all features...
  },
  "feature_statistics": {
    "total_revenue": {
      "mean": 3500.50,
      "median": 3200.00,
      "std": 450.25,
      "min": 2000.00,
      "max": 5000.00,
      "q25": 3000.00,
      "q75": 4000.00
    },
    ...for each feature...
  }
}
```

---

## Method-Specific Details

### 1. Fuzzy C-Means Profile

**Additional Metadata:**
- `fuzziness_parameter` (m value)
- `max_iterations`
- `convergence_threshold`

**Additional Metrics:**
- `partition_coefficient`: Fuzzy clustering quality (higher = better)
- `partition_entropy`: Cluster overlap (lower = better)

**Per-Cluster Additions:**
```json
{
  "membership_stats": {
    "mean": 0.85,
    "std": 0.12,
    "min": 0.45,
    "max": 1.0
  }
}
```

**File Example:**
```json
{
  "metadata": {
    "method": "Fuzzy C-Means (FCM)",
    "fuzziness_parameter": 2.0,
    "max_iterations": 150
  },
  "metrics": {
    "silhouette_score": 0.3476,
    "partition_coefficient": 0.7856,
    "partition_entropy": 0.4123
  }
}
```

---

### 2. Neural Network Profile

**Additional Metadata:**
- `encoding_dim`: Dimension of latent space
- `epochs`: Training epochs
- `batch_size`: Training batch size

**Additional Metrics:**
- `reconstruction_error`: Autoencoder quality (lower = better)

**Per-Cluster Additions:**
```json
{
  "encoded_space_stats": {
    "mean_distance_to_center": 2.45,
    "std_distance_to_center": 0.85
  }
}
```

**File Example:**
```json
{
  "metadata": {
    "method": "Neural Network (Autoencoder + K-Means)",
    "encoding_dim": 10,
    "epochs": 100,
    "batch_size": 32
  },
  "metrics": {
    "silhouette_score": 0.3228,
    "reconstruction_error": 0.0523
  }
}
```

---

### 3. GMM Profile

**Additional Metadata:**
- `covariance_type`: 'full', 'tied', 'diag', or 'spherical'
- `converged`: Whether EM algorithm converged
- `n_iterations`: Actual iterations taken

**Additional Metrics:**
- `bic`: Bayesian Information Criterion (lower = better)
- `aic`: Akaike Information Criterion (lower = better)
- `davies_bouldin_index`: Cluster separation (lower = better)
- `calinski_harabasz_score`: Cluster dispersion (higher = better)
- `log_likelihood`: Model fit quality

**Additional Root-Level:**
```json
{
  "mixture_weights": [0.25, 0.28, 0.22, 0.25],
  "uncertainty_metrics": {
    "avg_max_probability": 0.9998,
    "high_confidence_count": 500,
    "high_confidence_pct": 100.0,
    "low_confidence_count": 0,
    "avg_entropy": 0.0006
  }
}
```

**Per-Cluster Additions:**
```json
{
  "mixture_weight": 0.25,
  "probability_stats": {
    "mean": 0.9985,
    "std": 0.0045,
    "min": 0.9123,
    "max": 0.9999,
    "median": 0.9987
  },
  "covariance_info": {
    "type": "full",
    "feature_variances": {
      "total_revenue": 150000.5,
      "recency_days": 25.3,
      ...
    }
  }
}
```

---

## Usage

### Method 1: Individual Clustering Method

```python
from customer_segmentation import GMMCustomerSegmentation

# Fit your model
gmm = GMMCustomerSegmentation(n_clusters=4)
gmm.fit_predict(data)

# Export profile
export_result = gmm.export_cluster_profile(data, output_dir='data/output')

print(f"JSON: {export_result['json']}")
print(f"YAML: {export_result['yaml']}")

# Access profile in memory
profile = export_result['profile']
print(f"Silhouette Score: {profile['metrics']['silhouette_score']}")
```

### Method 2: Export All Three Methods

```bash
python examples/export_cluster_profiles.py
```

This will generate 6 files (2 per method) in `data/output/`.

---

## AI LLM Integration

### Prompt Template for LLM Analysis

```
You are a data analyst specializing in customer segmentation. 
Analyze the following cluster profile and provide:

1. **Segment Names**: Descriptive names for each cluster
2. **Customer Personas**: Detailed descriptions of typical customers
3. **Marketing Strategies**: Tailored recommendations for each segment
4. **Business Insights**: Key patterns and opportunities

Cluster Profile:
{json_content}

Format your response as:
- Segment Overview
- Detailed Analysis per Cluster
- Cross-Cluster Comparisons
- Actionable Recommendations
```

### Example LLM Workflow

```python
import json
from openai import OpenAI  # or your preferred LLM client

# Load the exported profile
with open('data/output/gmm_cluster_profile_20251017_054133.json', 'r') as f:
    profile = json.load(f)

# Create prompt
prompt = f"""
Analyze this customer segmentation profile and generate:
1. Descriptive names for each cluster
2. Customer personas
3. Marketing recommendations

Profile:
{json.dumps(profile, indent=2)}
"""

# Send to LLM
client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a customer segmentation expert."},
        {"role": "user", "content": prompt}
    ]
)

print(response.choices[0].message.content)
```

---

## Profile Contents - Detailed Breakdown

### What the LLM Receives

#### 1. Cluster Sizes
```json
{
  "cluster_0": {
    "size": 150,
    "percentage": 30.0
  }
}
```
**LLM Can Determine**: Relative importance of each segment

#### 2. Feature Centroids
```json
{
  "cluster_center": {
    "total_revenue": 15000.50,
    "recency_days": 15,
    "frequency_per_month": 3.5,
    "return_rate": 0.05
  }
}
```
**LLM Can Determine**: Typical customer profile for the segment

#### 3. Feature Distributions
```json
{
  "feature_statistics": {
    "total_revenue": {
      "mean": 15000.50,
      "median": 14500.00,
      "std": 2500.00,
      "min": 8000.00,
      "max": 25000.00
    }
  }
}
```
**LLM Can Determine**: 
- Segment homogeneity (low std = tight cluster)
- Outlier presence (large min/max ranges)
- Distribution skewness (mean vs median)

#### 4. Hierarchical Product Preferences
```json
{
  "feature_statistics": {
    "dept_total_value_Accessories & Footwear": {
      "mean": 3500.00,
      ...
    },
    "class_total_value_Bags & Wallets": {
      "mean": 2000.00,
      ...
    }
  }
}
```
**LLM Can Determine**: 
- Department and class affinity
- Product category preferences
- Cross-selling opportunities

#### 5. Size/Age Preferences
```json
{
  "feature_statistics": {
    "count_Baby": {"mean": 5.2},
    "count_size_XL": {"mean": 8.5}
  }
}
```
**LLM Can Determine**: 
- Customer demographic indicators
- Life stage inference
- Product sizing patterns

---

## Business Applications

### 1. Segment Naming
**Input**: Cluster center values for all features  
**Output**: "VIP Champions", "Loyal Regulars", "At-Risk Customers", etc.

### 2. Persona Generation
**Input**: Feature statistics + distributions  
**Output**: Detailed customer personas with demographics, behaviors, preferences

### 3. Marketing Strategy
**Input**: Cluster characteristics + business metrics  
**Output**: 
- Recommended channels (email, SMS, direct mail)
- Offer types (discounts, loyalty rewards, new products)
- Message tone and content
- Campaign timing

### 4. Product Recommendations
**Input**: Department/class preferences  
**Output**: 
- Top products to promote per segment
- Cross-sell opportunities
- New product launch targeting

### 5. Risk Assessment
**Input**: Recency, frequency, return rate  
**Output**: 
- Churn risk identification
- Re-engagement strategies
- Retention priorities

### 6. Revenue Optimization
**Input**: Total revenue, avg order value, frequency  
**Output**: 
- Upsell opportunities
- Value growth strategies
- Lifetime value projections

---

## File Locations

After running `export_cluster_profiles.py`:

```
data/output/
├── fuzzy_cluster_profile_20251017_054128.json    (34.9 KB)
├── fuzzy_cluster_profile_20251017_054128.yaml    (68.2 KB)
├── neural_cluster_profile_20251017_054133.json   (10.2 KB)
├── neural_cluster_profile_20251017_054133.yaml   (20.1 KB)
├── gmm_cluster_profile_20251017_054133.json      (41.8 KB)
└── gmm_cluster_profile_20251017_054133.yaml      (82.5 KB)
```

**Note**: GMM files are larger due to additional probability and covariance information.

---

## API Reference

### Fuzzy C-Means
```python
fuzzy_model.generate_cluster_profile(data: pd.DataFrame) -> Dict[str, Any]
fuzzy_model.export_cluster_profile(data: pd.DataFrame, output_dir: str = 'data/output') -> Dict[str, str]
```

### Neural Network
```python
neural_model.generate_cluster_profile(data: pd.DataFrame) -> Dict[str, Any]
neural_model.export_cluster_profile(data: pd.DataFrame, output_dir: str = 'data/output') -> Dict[str, str]
```

### GMM
```python
gmm_model.generate_cluster_profile(data: pd.DataFrame) -> Dict[str, Any]
gmm_model.export_cluster_profile(data: pd.DataFrame, output_dir: str = 'data/output') -> Dict[str, str]
```

**Returns**:
```python
{
    'json': '/path/to/file.json',
    'yaml': '/path/to/file.yaml',
    'profile': {...}  # The profile dictionary
}
```

---

## Next Steps

1. **Load profiles into your LLM tool**
2. **Generate segment descriptions**
3. **Create marketing campaigns**
4. **Build customer personas**
5. **Develop targeting strategies**

---

## Example LLM Output

Given a cluster profile, an LLM might generate:

```
CLUSTER 0: High-Value Frequent Shoppers (31% of customers)

Profile:
- Average Revenue: $16,515
- Purchase Frequency: 6x per month
- Last Purchase: 14.6 days ago
- Return Rate: 3.1% (very low)
- Strong preference for Accessories & Footwear ($2,936)

Persona: "Premium Fashion Enthusiasts"
These are your most valuable customers who shop frequently and across 
multiple categories. They show strong brand loyalty (low returns) and 
consistent engagement.

Marketing Strategy:
✓ VIP treatment and early access to new products
✓ Loyalty rewards and exclusive events
✓ Personalized product recommendations
✓ Premium customer service tier

Recommended Actions:
1. Launch VIP loyalty program tier
2. Exclusive previews of new collections
3. Personal shopper services
4. Invitation-only sales events
```

---

**Status: ✅ FULLY IMPLEMENTED AND TESTED**
