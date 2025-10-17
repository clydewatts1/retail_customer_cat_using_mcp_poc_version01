# GMM Clustering Quick Reference

## Import
```python
from customer_segmentation import GMMCustomerSegmentation
```

## Basic Usage
```python
# Initialize
gmm = GMMCustomerSegmentation(
    n_clusters=4,           # Number of Gaussian components
    covariance_type='full', # 'full', 'tied', 'diag', 'spherical'
    max_iter=200,           # Max EM iterations
    n_init=10,              # Number of initializations
    seed=42                 # Random seed
)

# Fit and predict
labels, probabilities = gmm.fit_predict(data)

# Evaluate
metrics = gmm.evaluate(data)
```

## Key Methods

### Prediction
```python
# Hard clustering (cluster IDs)
labels = gmm.predict(data)  # → array([0, 2, 1, 0, ...])

# Soft clustering (probabilities)
probs = gmm.predict_proba(data)  # → array([[0.8, 0.1, 0.05, 0.05], ...])
```

### Model Information
```python
# Cluster centers (means)
centers = gmm.get_cluster_centers()  # → DataFrame

# Covariance matrices
covariances = gmm.get_covariances()  # → ndarray

# Mixture weights (priors)
weights = gmm.get_weights()  # → array([0.25, 0.25, 0.25, 0.25])
```

### Evaluation
```python
metrics = gmm.evaluate(data)
# Returns:
# {
#     'silhouette_score': 0.3676,
#     'bic': 12345.67,
#     'aic': 12234.56,
#     'davies_bouldin_index': 0.8234,
#     'calinski_harabasz_score': 1234.56,
#     'log_likelihood': -6117.28,
#     'n_clusters': 4,
#     'converged': True,
#     'n_iterations': 23
# }
```

### Uncertainty Analysis
```python
uncertainty = gmm.get_uncertainty_metrics(data)
# Returns:
# {
#     'avg_max_probability': 0.8542,
#     'std_max_probability': 0.1234,
#     'high_confidence_count': 234,
#     'high_confidence_pct': 46.8,
#     'low_confidence_count': 87,
#     'low_confidence_pct': 17.4,
#     'avg_entropy': 0.4567,
#     'max_entropy': 1.2345
# }
```

## Configuration-Based Features
```python
from customer_segmentation import get_config

config = get_config()
gmm.config = config.to_dict()  # Enable config-based feature selection

# Now GMM will use enriched features if configured:
# - dept_total_value_* columns
# - class_total_value_* columns
# - count_size_* columns
# etc.
```

## Common Patterns

### Find Borderline Customers
```python
labels, probs = gmm.fit_predict(data)
max_probs = probs.max(axis=1)

borderline = data[max_probs < 0.7]
print(f"Found {len(borderline)} borderline customers")
```

### Compare Covariance Types
```python
for cov_type in ['full', 'tied', 'diag', 'spherical']:
    gmm = GMMCustomerSegmentation(n_clusters=4, covariance_type=cov_type)
    gmm.fit(data)
    metrics = gmm.evaluate(data)
    print(f"{cov_type}: BIC={metrics['bic']:.2f}")
```

### Optimal Cluster Selection
```python
bic_scores = []
for k in range(2, 10):
    gmm = GMMCustomerSegmentation(n_clusters=k)
    gmm.fit(data)
    metrics = gmm.evaluate(data)
    bic_scores.append(metrics['bic'])

optimal_k = range(2, 10)[np.argmin(bic_scores)]
```

### Target High-Probability Customers
```python
# Get probabilities for a specific cluster (e.g., VIP cluster = 0)
vip_probs = probs[:, 0]

# Find potential VIPs (>70% probability)
potential_vips = data[vip_probs > 0.7]

# Find uncertain VIPs (50-70% probability)
uncertain_vips = data[(vip_probs > 0.5) & (vip_probs <= 0.7)]
```

## Metrics Guide

### Lower is Better
- **BIC** (Bayesian Information Criterion): Model selection
- **AIC** (Akaike Information Criterion): Model selection
- **Davies-Bouldin Index**: Cluster separation quality

### Higher is Better
- **Silhouette Score**: Cluster quality (-1 to 1)
- **Calinski-Harabasz Score**: Cluster dispersion ratio
- **Log Likelihood**: Model fit

### Uncertainty Metrics
- **High Confidence (>90%)**: Clearly belong to one cluster
- **Low Confidence (<70%)**: Borderline/transitional customers
- **Entropy**: Higher = more uncertain assignment

## Run Example Script
```powershell
cd examples
python run_gmm_clustering.py
```

## Jupyter Notebook
See **Section 5.5** in `examples/customer_segmentation_analysis.ipynb`

## Full Documentation
See `GMM_CLUSTERING_MODULE.md` for complete reference
