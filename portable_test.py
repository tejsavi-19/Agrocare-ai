import tensorflow as tf
import numpy as np
import os
import sys

# Suppress TensorFlow logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications import MobileNetV3Large
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.applications.mobilenet_v3 import preprocess_input

def get_base_dir():
    # Robust way to get the directory where this script is running
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

# Config
BASE_DIR = get_base_dir()
IMG_SIZE = 224

# Define paths relative to this script
MODEL_REL_PATH = os.path.join("models", "leaf_stem_healthy_diseased.h5")
MODEL_PATH = os.path.join(BASE_DIR, MODEL_REL_PATH)

TEST_IMAGES = ["p3.jpg", "p22.jpg", "p1.jpg"] # Added variations just in case

print(f"Script Location: {BASE_DIR}")
print(f"Looking for model at: {MODEL_PATH}")

def build_model_architecture():
    print("Building model architecture...", flush=True)
    try:
        base_model = MobileNetV3Large(
            include_top=False,
            input_shape=(IMG_SIZE, IMG_SIZE, 3),
            weights=None 
        )
        
        x = base_model.output
        x = GlobalAveragePooling2D()(x)
        x = Dropout(0.4)(x)
        output = Dense(1, activation="sigmoid")(x)
        
        model = Model(inputs=base_model.input, outputs=output)
        return model
    except Exception as e:
        print(f"Error building model architecture: {e}")
        return None

def load_robust_model():
    if not os.path.exists(MODEL_PATH):
        print(f"CRITICAL ERROR: Model file not found at {MODEL_PATH}")
        print("Please ensure the 'models' folder is in the same directory as this script.")
        return None

    model = build_model_architecture()
    if model is None: return None

    print(f"Loading weights...", flush=True)
    try:
        model.load_weights(MODEL_PATH)
        print("Weights loaded successfully.")
    except Exception as e:
        print(f"Error loading weights: {e}")
        print("Attempting to load as full model...")
        try:
             model = tf.keras.models.load_model(MODEL_PATH, compile=False)
             print("Successfully loaded as full model instead.")
        except Exception as e2:
             print(f"Failed to load model: {e2}")
             return None
    return model

def test_images():
    print("\n" + "="*50)
    print("PORTABLE DIAGNOSTIC TEST")
    print("="*50)

    model = load_robust_model()
    if model is None:
        print("Exiting due to model loading failure.")
        input("Press Enter to exit...")
        return

    print("\nStarting Predictions...")
    
    found_any = False
    for img_name in TEST_IMAGES:
        img_path = os.path.join(BASE_DIR, img_name)
        
        if not os.path.exists(img_path):
            continue
            
        found_any = True
        print(f"\nProcessing: {img_name}")
        try:
            img = image.load_img(img_path, target_size=(IMG_SIZE, IMG_SIZE))
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array = preprocess_input(img_array)

            prediction = model.predict(img_array, verbose=0)[0][0]
            
            if prediction < 0.5:
                label = "DISEASED"
                confidence = (1.0 - prediction) * 100
            else:
                label = "HEALTHY"
                confidence = prediction * 100

            print(f"Raw Value: {prediction:.4f}")
            print(f"Result: {label}")
            print(f"Confidence: {confidence:.2f}%")
            
        except Exception as e:
            print(f"Error processing {img_name}: {e}")

    if not found_any:
        print("\nNo test images found!")
        print(f"Looked for: {', '.join(TEST_IMAGES)}")
        print(f"In directory: {BASE_DIR}")
    
    print("\n" + "="*50)
    print("Test Complete.")
    print("="*50)
    # input("Press Enter to close...") # Uncomment if sending to friend to keep window open

if __name__ == "__main__":
    test_images()
