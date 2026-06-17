---
title: Agrocare Ai
emoji: 🌱
colorFrom: green
colorTo: yellow
sdk: docker
app_port: 7860
pinned: false
---

# Binary Plant Leaf/Stem Health Detection Model

A TensorFlow-based deep learning model that classifies plant leaves or stems as **Healthy** or **Diseased** using binary classification.

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Prepare Dataset
Organize your images in the following structure:
```
dataset/
├── train/
│   ├── Healthy/
│   │   ├── image1.jpg
│   │   ├── image2.jpg
│   │   └── ...
│   └── Diseased/
│       ├── image1.jpg
│       ├── image2.jpg
│       └── ...
└── val/
    ├── Healthy/
    │   ├── image1.jpg
    │   └── ...
    └── Diseased/
        ├── image1.jpg
        └── ...
```

### 3. Train the Model
```bash
python train_binary_leaf_stem.py
```

This will:
- Create a MobileNetV3Large model with binary classification
- Load images from dataset/train/ and dataset/val/
- Apply data augmentation (rotation, zoom, horizontal flip)
- Train for 10 epochs
- Save the model to `models/leaf_stem_healthy_diseased.h5`

### 4. Use the Model for Inference
```python
from inference_binary_leaf_stem import predict_health

# Predict on a single image
result = predict_health('path/to/leaf_image.jpg')
print(result)
# Output: {'status': 'Healthy', 'confidence': 0.92}
```

Or batch predict on multiple images:
```python
from inference_binary_leaf_stem import batch_predict

results = batch_predict('path/to/image/directory')
for r in results:
    print(f"{r['image']}: {r['status']} ({r['confidence']:.4f})")
```

## Model Details

- **Architecture**: MobileNetV3Large with transfer learning
- **Input Size**: 224 × 224 pixels
- **Output**: Binary classification (Healthy=0, Diseased=1)
- **Loss Function**: Binary Cross-Entropy
- **Optimizer**: Adam (learning rate 1e-4)
- **Data Augmentation**: Rotation (20°), Zoom (0.2), Horizontal Flip
- **Training Epochs**: 10

## File Structure

```
.
├── train_binary_leaf_stem.py          # Training script
├── inference_binary_leaf_stem.py      # Inference functions
├── requirements.txt                    # Python dependencies
├── models/
│   └── leaf_stem_healthy_diseased.h5  # Trained model (after training)
└── dataset/
    ├── train/
    │   ├── Healthy/
    │   └── Diseased/
    └── val/
        ├── Healthy/
        └── Diseased/
```

## Requirements

- Python 3.8+
- TensorFlow 2.13+
- Pillow 10.0+
- NumPy 1.24+

## Notes

- The model works for both leaves and stems
- Binary classification only (Healthy vs Diseased)
- No disease type/severity classification
- Requires GPU for faster training (CPU works but slower)
- All image formats: JPG, PNG, BMP, GIF are supported
"# model" 
"# model" 
