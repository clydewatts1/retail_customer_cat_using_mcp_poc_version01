# GMM Clustering Module

## Overview

The GMM (Gaussian Mixture Model) clustering module provides probabilistic customer segmentation using Gaussian distributions. This is the third clustering method in the customer segmentation POC, alongside Fuzzy C-Means and Neural Network clustering.

## File Location

`src/customer_segmentation/gmm_clustering.py`

## Key Features

### 1. **Probabilistic Clustering**
- Each customer has a probability distribution over all clusters
- Provides soft assignments (probabilities) in addition to hard assignments (labels)
- Enables uncertainty quantification for cluster memberships

### 2. **Flexible Covariance Structures**
- **Full**: Each component has its own general covariance matrix
- **Tied**: All components share the same covariance matrix
- **Diag**: Each component has its own diagonal covariance matrix
- **Spherical**: Each component has its own single variance

### 3. **Comprehensive Metrics**
- Silhouette Score (clustering quality)
- BIC (Bayesian Information Criterion)
- AIC (Akaike Information Criterion)
- Davies-Bouldin Index
- Calinski-Harabasz Score
- Log Likelihood

### 4. **Uncertainty Analysis**
- Assignment confidence metrics
- Entropy calculations
- High/low confidence customer identification

## Class: GMMCustomerSegmentation

### Constructor Parameters

```python
GMMCustomerSegmentation(
    n_clusters: int = 4,
    covariance_type: str = 'full',
    max_iter: int = 200,
    n_init: int = 10,
    seed: Optional[int] = 42
)
```

**Parameters:**
- `n_clusters`: Number of Gaussian components (clusters)
- `covariance_type`: Type of covariance parameters ('full', 'tied', 'diag', 'spherical')
- `max_iter`: Maximum number of EM iterations
- `n_init`: Number of initializations to perform
- `seed`: Random seed for reproducibility

### Main Methods

#### 1. `fit(data: pd.DataFrame)`
Fit the GMM model to customer data.

```python
gmm_model = GMMCustomerSegmentation(n_clusters=4)
gmm_model.fit(data)
```

#### 2. `predict(data: pd.DataFrame) -> np.ndarray`
Predict hard cluster assignments.

```python
cluster_labels = gmm_model.predict(data)
```

#### 3. `predict_proba(data: pd.DataFrame) -> np.ndarray`
Predict cluster membership probabilities (soft clustering).

```python
probabilities = gmm_model.predict_proba(data)
# probabilities.shape = (n_customers, n_clusters)
```

#### 4. `fit_predict(data: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]`
Fit model and return both hard labels and probabilities.

```python
cluster_labels, probabilities = gmm_model.fit_predict(data)
```

#### 5. `get_cluster_centers() -> pd.DataFrame`
Get cluster centers (means) in original feature space.

```python
centers = gmm_model.get_cluster_centers()
```

#### 6. `get_covariances() -> np.ndarray`
Get covariance matrices for each cluster.

```python
covariances = gmm_model.get_covariances()
```

#### 7. `get_weights() -> np.ndarray`
Get mixture weights (prior probabilities) for each cluster.

```python
weights = gmm_model.get_weights()
```

#### 8. `evaluate(data: pd.DataFrame) -> dict`
Comprehensive clustering quality evaluation.

```python
metrics = gmm_model.evaluate(data)
# Returns: {
#     'silhouette_score': float,
#     'bic': float,
#     'aic': float,
#     'davies_bouldin_index': float,
#     'calinski_harabasz_score': float,
#     'log_likelihood': float,
#     'n_clusters': int,
#     'converged': bool,
#     'n_iterations': int
# }
```

#### 9. `get_uncertainty_metrics(data: pd.DataFrame) -> dict`
Calculate assignment uncertainty metrics.

```python
uncertainty = gmm_model.get_uncertainty_metrics(data)
# Returns: {
#     'avg_max_probability': float,
#     'std_max_probability': float,
#     'high_confidence_count': int,
#     'high_confidence_pct': float,
#     'low_confidence_count': int,
#     'low_confidence_pct': float,
#     'avg_entropy': float,
#     'max_entropy': float
# }
```

## Usage Example

### Basic Usage

```python
from customer_segmentation import RetailDataGenerator, GMMCustomerSegmentation, get_config

# Load configuration
config = get_config()

# Generate customer data
generator = RetailDataGenerator(seed=42)
data = generator.generate_customers(n_customers=500)

# Initialize GMM clustering
gmm_model = GMMCustomerSegmentation(
    n_clusters=4,
    covariance_type='full',
    max_iter=200,
    n_init=10,
    seed=42
)

# Store config for feature selection
gmm_model.config = config.to_dict()

# Fit and predict
cluster_labels, probabilities = gmm_model.fit_predict(data)

# Add results to dataframe
data['gmm_cluster'] = cluster_labels

# Evaluate clustering
metrics = gmm_model.evaluate(data)
print(f"Silhouette Score: {metrics['silhouette_score']:.4f}")
print(f"BIC: {metrics['bic']:.2f}")
print(f"AIC: {metrics['aic']:.2f}")

# Analyze uncertainty
uncertainty = gmm_model.get_uncertainty_metrics(data)
print(f"High Confidence Customers: {uncertainty['high_confidence_pct']:.1f}%")
print(f"Low Confidence Customers: {uncertainty['low_confidence_pct']:.1f}%")
```

### Configuration-Based Feature Selection

The GMM clustering module supports configuration-based feature selection, just like the fuzzy and neural clustering modules:

```yaml
# config/config.yml
gmm_clustering:
  use_enriched_features: true
  features_to_use:
    - total_purchases
    - total_revenue
    - avg_order_value
    - recency_days
    - frequency_per_month
    - customer_lifetime_months
    - return_rate
  enriched_features_to_use:
    - dept_total_value_Mens
    - dept_total_value_Womens
    - class_total_value_Shirts
    - class_total_value_Pants
    # ... etc
```

If `gmm_clustering` config is not available, it falls back to `fuzzy_clustering` config.

## Running the Example Script

```powershell
# Navigate to examples directory
cd examples

# Run GMM clustering example
python run_gmm_clustering.py
```

This will:
1. Generate synthetic customer data
2. Fit GMM clustering model
3. Display cluster distribution and metrics
4. Show uncertainty analysis
5. Create visualizations (saved to `visualizations/gmm_clustering_results.png`)

## Comparison with Other Methods

### GMM vs Fuzzy C-Means
- **GMM**: Probabilistic model with Gaussian assumptions, provides likelihood-based metrics (BIC/AIC)
- **Fuzzy**: Membership-based soft clustering, uses partition coefficient/entropy

### GMM vs Neural Network
- **GMM**: Explicit probabilistic model, interpretable covariance structure
- **Neural**: Deep feature learning, captures non-linear patterns

### When to Use GMM
1. Need probabilistic cluster assignments
2. Want to quantify assignment uncertainty
3. Data approximately follows Gaussian distributions
4. Need model selection via BIC/AIC
5. Require interpretable covariance structure

## Metrics Interpretation

### Model Selection Metrics
- **BIC (lower is better)**: Bayesian Information Criterion - penalizes model complexity
- **AIC (lower is better)**: Akaike Information Criterion - measures model fit

### Clustering Quality Metrics
- **Silhouette Score (higher is better)**: Ranges from -1 to 1, measures cluster separation
- **Davies-Bouldin Index (lower is better)**: Ratio of within-cluster to between-cluster distances
- **Calinski-Harabasz Score (higher is better)**: Ratio of between-cluster to within-cluster dispersion

### Uncertainty Metrics
- **Average Max Probability**: Mean of highest probability for each customer (closer to 1 = more confident)
- **High Confidence**: Customers with >90% probability in one cluster
- **Low Confidence**: Customers with <70% probability in assigned cluster
- **Entropy**: Measure of assignment uncertainty (lower = more certain)

## Integration with Notebook

The GMM clustering is fully integrated into the Jupyter notebook at:
`examples/customer_segmentation_analysis.ipynb`

See **Section 5.5** for GMM implementation and visualizations.

## Advanced Features

### Covariance Type Selection

```python
# Experiment with different covariance types
for cov_type in ['full', 'tied', 'diag', 'spherical']:
    gmm_model = GMMCustomerSegmentation(
        n_clusters=4,
        covariance_type=cov_type
    )
    gmm_model.fit(data)
    metrics = gmm_model.evaluate(data)
    print(f"{cov_type}: BIC={metrics['bic']:.2f}")
```

### Optimal Cluster Selection

```python
# Use BIC to select optimal number of clusters
bic_scores = []
n_clusters_range = range(2, 10)

for n in n_clusters_range:
    gmm = GMMCustomerSegmentation(n_clusters=n)
    gmm.fit(data)
    metrics = gmm.evaluate(data)
    bic_scores.append(metrics['bic'])

optimal_k = n_clusters_range[np.argmin(bic_scores)]
print(f"Optimal clusters: {optimal_k}")
```

### Identifying Borderline Customers

```python
# Find customers with uncertain cluster assignments
probabilities = gmm_model.predict_proba(data)
max_proba = probabilities.max(axis=1)

borderline_customers = data[max_proba < 0.7]
print(f"Found {len(borderline_customers)} borderline customers")

# These customers might benefit from special attention or
# could be transitioning between segments
```

## Dependencies

- `numpy`: Array operations
- `pandas`: Data manipulation
- `scikit-learn`: GaussianMixture, StandardScaler, metrics
- `matplotlib`: Visualization (in example script)
- `seaborn`: Statistical visualization (in example script)

## Best Practices

1. **Standardize Features**: GMM is sensitive to feature scales (handled automatically)
2. **Try Multiple Initializations**: Use `n_init >= 10` to avoid local optima
3. **Check Convergence**: Verify `gmm.converged_` is True
4. **Use BIC/AIC**: For model selection and comparison
5. **Analyze Uncertainty**: Identify low-confidence assignments for review
6. **Covariance Selection**: Start with 'full', try 'tied' if overfitting

## Future Enhancements

- Time-series tracking of probability changes
- Ensemble clustering with fuzzy and neural methods
- Hierarchical GMM for nested segmentation
- Online/incremental GMM updates
- Custom initialization strategies
