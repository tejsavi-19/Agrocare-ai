import tensorflow as tf
import numpy as np
import os
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications import MobileNetV3Large
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.applications.mobilenet_v3 import preprocess_input

# Config
IMG = 224
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_WEIGHTS_PATH = os.path.join(BASE_DIR, "models", "leaf_stem_healthy_diseased.h5")
TEST_IMAGE_PATH = os.path.join(BASE_DIR, "download.jpg")

def build_model_architecture():
    # Reconstruct the exact same architecture as used in test_image.py
    base_model = MobileNetV3Large(
        include_top=False,
        input_shape=(IMG, IMG, 3),
        weights=None # We'll load our own weights
    )
    
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dropout(0.4)(x)
    output = Dense(1, activation="sigmoid")(x)
    
    model = Model(inputs=base_model.input, outputs=output)
    return model

def verify_fix():
    print("Reconstructing model architecture...")
    model = build_model_architecture()
    
    print(f"Loading weights from {MODEL_WEIGHTS_PATH}...")
    try:
        model.load_weights(MODEL_WEIGHTS_PATH)
    except Exception as e:
        print(f"Error loading weights: {e}")
        # If it fails, maybe it's because it's a full model file, not just weights
        try:
             model = tf.keras.models.load_model(MODEL_WEIGHTS_PATH, compile=False)
             print("Successfully loaded as full model instead.")
        except Exception as e2:
             print(f"Failed to load as full model too: {e2}")
             return

    print(f"Testing on {TEST_IMAGE_PATH}...")
    if os.path.exists(TEST_IMAGE_PATH):
        img = image.load_img(TEST_IMAGE_PATH, target_size=(IMG, IMG))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)

        prediction = model.predict(img_array)[0][0]
        
        # Alphabetic: diseased=0, healthy=1
        if prediction < 0.5:
            label = "diseased"
            confidence = (1.0 - prediction) * 100
        else:
            label = "healthy"
            confidence = prediction * 100

        print(f"Raw Prediction Value: {prediction:.4f}")
        print(f"PREDICTED CLASS: {label}")
        print(f"CONFIDENCE: {confidence:.2f}%")
        
        if label == "healthy":
            print("\nSUCCESS: The model NOW correctly identifies the healthy leaf!")
            print("The brightness bias fix is working.")
        else:
            print("\nSTILL MISCLASSIFIED: The model still thinks the bright leaf is diseased.")
            print(f"Current prediction: {label} ({confidence:.2f}%)")
    else:
        print(f"Error: {TEST_IMAGE_PATH} not found.")

if __name__ == "__main__":
    verify_fix()
