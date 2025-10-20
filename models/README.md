# Models Directory

This directory stores trained machine learning and neural network models.

## Directory Purpose

- Store serialized models (`.pkl`, `.h5`, `.pt`, etc.)
- Save model checkpoints during training
- Keep track of model versions

## Model Naming Convention

Use descriptive names that include:
- Model type (e.g., `fcm`, `nn`, `autoencoder`)
- Date/version
- Key parameters

Examples:
- `fuzzy_cmeans_5clusters_v1.pkl`
- `fuzzy_clustering_nn_20240101.h5`
- `autoencoder_encoder_dim10_v2.h5`

## Best Practices

1. **Version Control**: Do not commit large model files to git
   - Add `*.h5`, `*.pkl`, `*.pt` to `.gitignore` (already configured)
   - Use Git LFS or model registry services for model versioning

2. **Model Documentation**: Create a `MODELS.md` file documenting:
   - Model architecture
   - Training parameters
   - Performance metrics
   - Training date and data used

3. **Model Checkpoints**: Use subdirectories for different model versions
   ```
   models/
   ├── fuzzy_cmeans/
   │   ├── v1/
   │   └── v2/
   └── neural_network/
       ├── checkpoints/
       └── final/
   ```

4. **Serialization**: Use appropriate formats:
   - Pickle (`.pkl`) for scikit-learn models
   - HDF5 (`.h5`) for Keras/TensorFlow models
   - PyTorch (`.pt`, `.pth`) for PyTorch models
   - ONNX (`.onnx`) for cross-framework compatibility

## Loading Models

Example code for loading models:

```python
# Load scikit-learn model
import pickle
with open('models/fuzzy_cmeans_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Load Keras model
from tensorflow import keras
model = keras.models.load_model('models/fuzzy_clustering_nn.h5')
```

## Model Registry

Consider using tools like:
- MLflow for experiment tracking and model registry
- DVC for data and model versioning
- W&B (Weights & Biases) for experiment management
