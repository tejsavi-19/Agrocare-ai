import os
import numpy as np
import tensorflow as tf
from PIL import Image

# Config
IMG_SIZE = (224, 224)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "leaf_stem_healthy_diseased.h5")
# Points to local image for reproduction
TEST_IMAGE_PATH = os.path.join(BASE_DIR, "test.webp")

def run_test():
    print(f"Loading model from {MODEL_PATH}...", flush=True)
    if not os.path.exists(MODEL_PATH):
        print(f"Error: Model file not found at {MODEL_PATH}", flush=True)
        return

    try:
        model = tf.keras.models.load_model(MODEL_PATH, compile=False)
        print("Model loaded successfully.", flush=True)
    except Exception as e:
        print(f"First attempt failed: {e}", flush=True)
        try:
            from tensorflow.keras.applications import MobileNetV3Large
            from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
            from tensorflow.keras.models import Model
            
            base_model = MobileNetV3Large(include_top=False, input_shape=(IMG_SIZE[0], IMG_SIZE[1], 3), weights=None)
            x = base_model.output
            x = GlobalAveragePooling2D()(x)
            x = Dropout(0.4)(x)
            output = Dense(1, activation="sigmoid")(x)
            model = Model(inputs=base_model.input, outputs=output)
            model.load_weights(MODEL_PATH)
            print("Model weights loaded into reconstructed architecture successfully.", flush=True)
        except Exception as e3:
            print(f"Final reconstruction attempt failed: {e3}", flush=True)
            return

    print(f"Testing on {TEST_IMAGE_PATH}...", flush=True)
    if not os.path.exists(TEST_IMAGE_PATH):
        print(f"Error: Image file not found at {TEST_IMAGE_PATH}", flush=True)
        return

    try:
        # FIXED PREPROCESSING: Use standard MobileNetV3 preprocessing
        from tensorflow.keras.applications.mobilenet_v3 import preprocess_input
        img = Image.open(TEST_IMAGE_PATH).convert('RGB')
        img = img.resize(IMG_SIZE)
        img_array = np.array(img, dtype=np.float32)
        # img_array = img_array / 255.0  <-- INCORRECT for this model
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)

        # Make prediction
        pred_output = model.predict(img_array)
        prediction = float(pred_output.flatten()[0])
        
        # FIXED LOGIC: > 0.5 is Healthy
        status = "Healthy" if prediction > 0.5 else "Diseased"
        confidence = float(prediction) if prediction > 0.5 else float(1.0 - prediction)

        print("\n" + "="*30, flush=True)
        print("RESULT", flush=True)
        print("="*30, flush=True)
        print(f"File: {TEST_IMAGE_PATH}", flush=True)
        print(f"Raw Prediction: {prediction:.4f}", flush=True)
        print(f"PREDICTED CLASS: {status}", flush=True)
        print(f"CONFIDENCE: {confidence*100:.2f}%", flush=True)
        print("="*30, flush=True)

    except Exception as e:
        print(f"Error during inference: {e}", flush=True)

if __name__ == "__main__":
    run_test()
