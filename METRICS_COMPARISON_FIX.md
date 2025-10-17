# Fix: Clustering Metrics Comparison KeyError

## Issue
**Error:** `KeyError: 'davies_bouldin_index'` when running `run_segmentation_pipeline.py`

**Root Cause:** The comparison table was trying to access metrics that don't exist in all clustering methods. Each method returns different evaluation metrics:

### Metrics by Method

| Method | Silhouette | Davies-Bouldin | Calinski-Harabasz | Method-Specific |
|--------|------------|----------------|-------------------|-----------------|
| **Fuzzy C-Means** | ✅ | ❌ | ❌ | PC (Partition Coefficient), PE (Partition Entropy) |
| **Neural Clustering** | ✅ | ❌ | ❌ | Reconstruction Error |
| **GMM** | ✅ | ✅ | ✅ | BIC, AIC, Log Likelihood |

## Solution

Updated the comparison table to:
1. Show **only Silhouette Score** as the common metric across all methods
2. Display **method-specific metrics** separately for each method
3. Add **detailed explanations** of what each metric means

### New Comparison Output

```
Clustering Methods Comparison:
  Method                    Silhouette Score     Method-Specific Metrics
  ------------------------- -------------------- --------------------------------------------------
  Fuzzy C-Means                           0.XXXX  PC=0.XXXX, PE=0.XXXX
  Neural Clustering                       0.XXXX  Recon. Error=0.XXXXXX
  GMM                                     0.XXXX  DB=0.XXXX, CH=XXXX.XX

  Notes:
    - Silhouette Score: Higher is better (range: -1 to 1)
    - PC (Partition Coefficient): Higher is better (range: 1/n_clusters to 1)
    - PE (Partition Entropy): Lower is better
    - Recon. Error (Reconstruction Error): Lower is better
    - DB (Davies-Bouldin Index): Lower is better
    - CH (Calinski-Harabasz Score): Higher is better

  Additional GMM Metrics:
    BIC (Bayesian Information Criterion): XXX.XX (lower is better)
    AIC (Akaike Information Criterion): XXX.XX (lower is better)
    Log Likelihood: XXX.XX (higher is better)
```

## Changes Made

**File:** `examples/run_segmentation_pipeline.py`

### Before (Lines 370-382)
```python
print("Clustering Methods Comparison:")
print(f"  {'Method':<25} {'Silhouette':<12} {'Davies-Bouldin':<18} {'Calinski-Harabasz'}")
print(f"  {'-'*25} {'-'*12} {'-'*18} {'-'*18}")
print(f"  {'Fuzzy C-Means':<25} {fuzzy_metrics['silhouette_score']:>11.4f} {fuzzy_metrics['davies_bouldin_index']:>17.4f} {fuzzy_metrics['calinski_harabasz_score']:>18.2f}")  # ❌ KeyError
print(f"  {'Neural Clustering':<25} {neural_metrics['silhouette_score']:>11.4f} {neural_metrics['davies_bouldin_index']:>17.4f} {neural_metrics['calinski_harabasz_score']:>18.2f}")  # ❌ KeyError
print(f"  {'GMM':<25} {gmm_metrics['silhouette_score']:>11.4f} {gmm_metrics['davies_bouldin_index']:>17.4f} {gmm_metrics['calinski_harabasz_score']:>18.2f}")  # ✅ OK
```

### After (Lines 370-387)
```python
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
```

## Metric Definitions

### Common Metric (All Methods)

**Silhouette Score**
- **Range:** -1 to 1
- **Best:** Higher (closer to 1)
- **Meaning:** Measures how similar a point is to its own cluster compared to other clusters
- **Interpretation:** 
  - 1.0 = Perfect clustering
  - 0.0 = Overlapping clusters
  - -1.0 = Wrong cluster assignment

### Fuzzy C-Means Specific

**Partition Coefficient (PC)**
- **Range:** 1/n_clusters to 1
- **Best:** Higher (closer to 1)
- **Meaning:** Measures the fuzziness of the clustering
- **Interpretation:** Higher values indicate crisper cluster assignments

**Partition Entropy (PE)**
- **Range:** 0 to log(n_clusters)
- **Best:** Lower (closer to 0)
- **Meaning:** Measures the uncertainty in cluster assignments
- **Interpretation:** Lower values indicate more definite cluster membership

### Neural Clustering Specific

**Reconstruction Error**
- **Range:** 0 to ∞
- **Best:** Lower (closer to 0)
- **Meaning:** How well the autoencoder reconstructs the input data
- **Interpretation:** Lower values indicate better feature learning

### GMM Specific

**Davies-Bouldin Index (DB)**
- **Range:** 0 to ∞
- **Best:** Lower (closer to 0)
- **Meaning:** Ratio of within-cluster scatter to between-cluster separation
- **Interpretation:** Lower values indicate better-separated clusters

**Calinski-Harabasz Score (CH)**
- **Range:** 0 to ∞
- **Best:** Higher
- **Meaning:** Ratio of between-cluster variance to within-cluster variance
- **Interpretation:** Higher values indicate better-defined clusters

**Bayesian Information Criterion (BIC)**
- **Range:** -∞ to 0 (typically negative)
- **Best:** Lower (less negative)
- **Meaning:** Model selection criterion balancing fit and complexity
- **Interpretation:** Lower values indicate better model fit

**Akaike Information Criterion (AIC)**
- **Range:** -∞ to 0 (typically negative)
- **Best:** Lower (less negative)
- **Meaning:** Model selection criterion emphasizing fit
- **Interpretation:** Lower values indicate better model fit

**Log Likelihood**
- **Range:** -∞ to 0 (typically negative)
- **Best:** Higher (closer to 0)
- **Meaning:** Probability of data given the model
- **Interpretation:** Higher values indicate better fit

## Benefits of Updated Display

1. **Accurate Comparison** - Only compares metrics that exist for all methods
2. **Method Insights** - Shows unique strengths of each method
3. **User Education** - Explains what each metric means
4. **No Errors** - No more KeyError exceptions
5. **Better Interpretation** - Clear guidance on what "better" means

## Testing

Run the pipeline to verify the fix:
```bash
python examples/run_segmentation_pipeline.py
```

Expected: No KeyError, clean comparison table with all metrics displayed correctly.

## Related Files

- `src/customer_segmentation/fuzzy_clustering.py` - Returns: silhouette_score, partition_coefficient, partition_entropy
- `src/customer_segmentation/neural_clustering.py` - Returns: silhouette_score, reconstruction_error
- `src/customer_segmentation/gmm_clustering.py` - Returns: silhouette_score, davies_bouldin_index, calinski_harabasz_score, bic, aic, log_likelihood

---

**Fixed by:** AI Assistant  
**Date:** October 17, 2025  
**Status:** ✅ Resolved
