"""
Binary Leaf/Stem Health Detection - Inference Script
Provides simple prediction function to classify leaves/stems as healthy or diseased.
"""

import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from PIL import Image
import traceback

# Global model variable (loaded once)
_model = None

def load_model(model_path='models/leaf_stem_healthy_diseased.keras'):
    """
    Load the pre-trained binary classification model.
    
    Args:
        model_path: Path to the saved model file (.keras format)
    
    Returns:
        keras.Model: Loaded model
    """
    global _model
    if _model is None:
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found at {model_path}. Train the model first using train_binary_leaf_stem.py")
        _model = keras.models.load_model(model_path)
        print(f"Model loaded from: {model_path}")
    return _model

def preprocess_image(image_path, target_size=(224, 224)):
    """
    Load and preprocess an image for model inference.
    
    Args:
        image_path: Path to the image file
        target_size: Target size for the image
    
    Returns:
        np.ndarray: Preprocessed image array (normalized to 0-1)
    """
    # Load image
    img = Image.open(image_path).convert('RGB')
    
    # Resize to target size
    img = img.resize(target_size)
    
    # Convert to numpy array and normalize
    img_array = np.array(img, dtype=np.float32)
    img_array = img_array / 255.0
    
    # Add batch dimension
    img_array = np.expand_dims(img_array, axis=0)
    
    return img_array

def predict_health(image_path, model_path='models/leaf_stem_healthy_diseased.keras'):
    """
    Predict whether a plant leaf or stem is healthy or diseased.
    
    Args:
        image_path: Path to the leaf/stem image
        model_path: Path to the trained model file (.keras format)
    
    Returns:
        dict: Prediction result with keys:
            - "status": "Healthy" or "Diseased"
            - "confidence": float between 0 and 1
    
    Example:
        >>> result = predict_health('path/to/leaf_image.jpg')
        >>> print(result)
        {'status': 'Diseased', 'confidence': 0.85}
    """
    # Load model
    model = load_model(model_path)
    
    # Preprocess image
    img_array = preprocess_image(image_path)
    
    # Make prediction
    pred_output = model.predict(img_array)
    prediction = float(pred_output.flatten()[0])
    
    # Convert to health status
    # 0.0 = Healthy, 1.0 = Diseased
    status = "Diseased" if prediction > 0.5 else "Healthy"
    
    # Confidence is the probability of the predicted class
    confidence = float(prediction) if prediction > 0.5 else float(1.0 - prediction)
    
    return {
        "status": status,
        "confidence": confidence
    }

def batch_predict(image_dir, model_path='models/leaf_stem_healthy_diseased.keras'):
    """
    Predict health status for all images in a directory.
    
    Args:
        image_dir: Path to directory containing images
        model_path: Path to the trained model file (.keras format)
    
    Returns:
        list: List of dicts with keys: "image", "status", "confidence"
    """
    results = []
    
    # Get list of image files
    supported_formats = {'.jpg', '.jpeg', '.png', '.bmp', '.gif'}
    image_files = [
        f for f in os.listdir(image_dir)
        if os.path.splitext(f)[1].lower() in supported_formats
    ]
    
    if not image_files:
        print(f"No images found in {image_dir}")
        return results
    
    print(f"Predicting health status for {len(image_files)} images...")
    
    for filename in image_files:
        image_path = os.path.join(image_dir, filename)
        try:
            prediction = predict_health(image_path, model_path)
            results.append({
                "image": filename,
                "status": prediction["status"],
                "confidence": prediction["confidence"]
            })
            print(f"  {filename}: {prediction['status']} (confidence: {prediction['confidence']:.4f})")
        except Exception as e:
            print(f"  Error processing {filename}: {str(e)}")
    
    return results

if __name__ == '__main__':
    """
    Example usage of the prediction functions.
    """
    # Example 1: Single image prediction
    print("=" * 60)
    print("Binary Leaf/Stem Health Detection - Inference Example")
    print("=" * 60)
    
    # Create a dummy test image for demonstration
    test_image_path = 'test_leaf.jpg'
    
    # Check if we have a test image
    if os.path.exists(test_image_path):
        print(f"\nPredicting health status for: {test_image_path}")
        result = predict_health(test_image_path)
        print(f"Result: {result}")
    else:
        print(f"\nNo test image found at {test_image_path}")
        print("To use predict_health(), provide a path to a leaf/stem image:")
        print("  >>> result = predict_health('path/to/leaf_image.jpg')")
        print("  >>> print(result)")
        print("  {'status': 'Healthy', 'confidence': 0.92}")
    
    # Example 2: Batch prediction on directory
    test_dir = 'test_images'
    if os.path.exists(test_dir):
        print(f"\nBatch predicting images in: {test_dir}")
        results = batch_predict(test_dir)
        for r in results:
            print(f"  {r}")
    else:
        print(f"\nNo test directory found at {test_dir}")
        print("To batch predict, create a directory with images and use:")
        print("  >>> results = batch_predict('path/to/image/directory')")
