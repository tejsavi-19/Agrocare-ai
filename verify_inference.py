"""
Quick verification that inference code works correctly
Tests with a minimal trained model
"""

import numpy as np
import tensorflow as tf
from tensorflow import keras
from PIL import Image
import os

# Create a minimal test model to verify inference works
def create_minimal_test_model():
    """Create and save a small test model for verification"""
    print("Creating minimal test model...")
    
    inputs = keras.Input(shape=(224, 224, 3))
    x = keras.layers.Conv2D(4, 3, activation='relu')(inputs)
    x = keras.layers.MaxPooling2D()(x)
    x = keras.layers.GlobalAveragePooling2D()(x)
    x = keras.layers.Dense(8, activation='relu')(x)
    outputs = keras.layers.Dense(1, activation='sigmoid')(x)
    
    model = keras.Model(inputs=inputs, outputs=outputs)
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    
    # Save it
    os.makedirs('models', exist_ok=True)
    model.save('models/leaf_stem_healthy_diseased.keras')
    print("✓ Test model saved to: models/leaf_stem_healthy_diseased.keras")
    return model

def create_test_image():
    """Create a test image"""
    print("\nCreating test image...")
    # Create a simple RGB image
    img_array = np.random.randint(0, 256, (224, 224, 3), dtype=np.uint8)
    img = Image.fromarray(img_array)
    test_path = 'test_sample.jpg'
    img.save(test_path)
    print(f"✓ Test image saved to: {test_path}")
    return test_path

if __name__ == '__main__':
    print("="*60)
    print("Inference Code Verification")
    print("="*60)
    
    # Create test model
    create_minimal_test_model()
    
    # Create test image
    test_img_path = create_test_image()
    
    # Now test the inference functions
    print("\nTesting inference functions...")
    try:
        from inference_binary_leaf_stem import predict_health
        
        result = predict_health(test_img_path)
        print(f"\n✓ Inference successful!")
        print(f"  Status: {result['status']}")
        print(f"  Confidence: {result['confidence']:.4f}")
        
        print("\n" + "="*60)
        print("✓ All tests passed!")
        print("="*60)
        print("\nNOTE: This used a minimal test model for verification.")
        print("When you have your full dataset ready, run:")
        print("  python train_binary_leaf_stem.py")
        
    except Exception as e:
        print(f"\n✗ Error during inference test: {str(e)}")
        import traceback
        traceback.print_exc()
