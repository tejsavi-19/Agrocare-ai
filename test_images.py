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
TEST_IMAGES = ["test.webp", "t2.jpg.jpeg"]

def build_model_architecture():
    print("Building model architecture...")
    base_model = MobileNetV3Large(
        include_top=False,
        input_shape=(IMG, IMG, 3),
        weights=None 
    )
    
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dropout(0.4)(x)
    output = Dense(1, activation="sigmoid")(x)
    
    model = Model(inputs=base_model.input, outputs=output)
    return model

def load_robust_model():
    print(f"Loading weights from {MODEL_WEIGHTS_PATH}...")
    model = build_model_architecture()
    try:
        model.load_weights(MODEL_WEIGHTS_PATH)
        print("Weights loaded successfully.")
    except Exception as e:
        print(f"Error loading weights: {e}")
        try:
             model = tf.keras.models.load_model(MODEL_WEIGHTS_PATH, compile=False)
             print("Successfully loaded as full model instead.")
        except Exception as e2:
             print(f"Failed to load as full model too: {e2}")
             return None
    return model

def test_images():
    model = load_robust_model()
    if model is None:
        print("Failed to load model. Exiting.")
        return

    for img_name in TEST_IMAGES:
        img_path = os.path.join(BASE_DIR, img_name)
        print(f"\nTesting on {img_path}...")
        
        if os.path.exists(img_path):
            try:
                img = image.load_img(img_path, target_size=(IMG, IMG))
                img_array = image.img_to_array(img)
                img_array = np.expand_dims(img_array, axis=0)
                img_array = preprocess_input(img_array)

                prediction = model.predict(img_array, verbose=0)[0][0]
                
                if prediction < 0.5:
                    label = "diseased"
                    confidence = (1.0 - prediction) * 100
                else:
                    label = "healthy"
                    confidence = prediction * 100

                print(f"Raw Prediction Value: {prediction:.4f}")
                print(f"PREDICTED CLASS: {label}")
                print(f"CONFIDENCE: {confidence:.2f}%")
            except Exception as e:
                print(f"Error processing {img_name}: {e}")
        else:
            print(f"Error: {img_path} not found.")

if __name__ == "__main__":
    test_images()
