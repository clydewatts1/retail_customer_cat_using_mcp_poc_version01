# Visualizations Directory

This directory contains visualization plots generated from customer segmentation analysis.

## Generated Visualizations

When you run `examples/visualize_segments.py`, the following plots are created:

1. **cluster_distribution.png** - Distribution of customers across segments
2. **segment_characteristics.png** - Comparison of key metrics across segments
3. **rfm_scatter.png** - RFM (Recency, Frequency, Monetary) analysis scatter plots
4. **membership_heatmap.png** - Fuzzy membership degrees for sample customers

## Generating Visualizations

```bash
cd examples
python visualize_segments.py
```

The visualizations help you understand:
- How customers are distributed across different segments
- Key characteristics that differentiate segments
- Relationships between RFM metrics
- How "fuzzy" the segment boundaries are (membership degrees)
