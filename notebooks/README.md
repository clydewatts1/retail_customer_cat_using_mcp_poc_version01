# Notebooks Directory

This directory contains Jupyter notebooks for the Retail Customer Categorization project.

## Notebook Structure

The notebooks are organized to follow a typical data science workflow:

### 1. Data Exploration (`01_data_exploration.ipynb`)
- Load and inspect raw customer data
- Perform exploratory data analysis (EDA)
- Identify features for categorization
- Create visualizations

### 2. Fuzzy Clustering - Traditional ML (`02_fuzzy_clustering_traditional_ml.ipynb`)
- Implement fuzzy c-means clustering
- Use scikit-fuzzy library
- Evaluate clustering quality
- Profile customer segments

### 3. Fuzzy Clustering - Neural Networks (`03_fuzzy_clustering_neural_network.ipynb`)
- Build neural network-based fuzzy clustering
- Use TensorFlow/Keras
- Compare with traditional ML approach
- Save trained models

## Getting Started

1. **Activate the conda environment:**
   ```bash
   conda activate retail_customer_cat
   ```

2. **Launch Jupyter Lab:**
   ```bash
   jupyter lab
   ```

3. **Start with notebook 01** and work through the sequence.

## Best Practices

- **Keep notebooks clean**: Remove debugging code and temporary outputs before committing
- **Document your work**: Use markdown cells to explain your thought process
- **Version control**: Commit working versions of notebooks regularly
- **Save outputs**: Save processed data and models to appropriate directories
- **Use relative paths**: Reference data and models using relative paths (e.g., `../data/raw/`)

## Tips for Jupyter Notebooks

- Use **Restart & Run All** regularly to ensure reproducibility
- Clear outputs before committing large notebooks with image outputs
- Consider using **nbconvert** to export notebooks to HTML or PDF for sharing
- Use **%matplotlib inline** for inline plotting
- Use **%%time** magic command to profile cell execution time

## Additional Notebooks

Feel free to add more notebooks for:
- Model evaluation and comparison
- Hyperparameter tuning
- Customer segment analysis
- Deployment and inference
- Custom experiments
