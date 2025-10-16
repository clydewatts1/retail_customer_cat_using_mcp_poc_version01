# Configuration Directory

This directory contains configuration files for the Retail Customer Categorization project.

## Purpose

Store project-wide configuration files such as:
- Model hyperparameters
- Data processing parameters
- Logging configuration
- API keys (never commit actual keys!)
- Environment-specific settings

## Example Configuration Files

### config.yaml (example)
```yaml
# Model Configuration
model:
  fuzzy_cmeans:
    n_clusters: 5
    fuzziness: 2
    max_iterations: 1000
    error_threshold: 0.005
  
  neural_network:
    encoding_dim: 10
    hidden_layers: [64, 32]
    learning_rate: 0.001
    batch_size: 32
    epochs: 100

# Data Configuration
data:
  raw_data_path: "data/raw"
  processed_data_path: "data/processed"
  test_size: 0.2
  random_state: 42

# Feature Configuration
features:
  numerical: ["age", "income", "purchase_frequency"]
  categorical: ["gender", "location", "membership_tier"]
```

## Best Practices

1. **Never commit secrets**: Use environment variables or secret management tools
2. **Use templates**: Create `.template` versions of config files with dummy values
3. **Document parameters**: Add comments explaining each configuration option
4. **Version control**: Track configuration changes to understand model evolution
5. **Environment-specific configs**: Use different configs for dev, staging, production
