import tensorflow as tf
import numpy as np
import os
import sys
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications import MobileNetV3Large
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.applications.mobilenet_v3 import preprocess_input

# Config
IMG_SIZE = 224
MODEL_PATH = r"models\leaf_stem_healthy_diseased.h5"
TEST_IMAGE = r"C:\Users\rehan\Downloads\model-main\anthracnose-1-460x263.webp"

def test_single_image(img_path):
    print(f"Starting prediction for: {img_path}", flush=True)
    try:
        # 1. Rebuild Architecture exactly as in training
        print("Building model architecture...", flush=True)
        base_model = MobileNetV3Large(weights=None, include_top=False, input_shape=(IMG_SIZE, IMG_SIZE, 3))
        x = base_model.output
        x = GlobalAveragePooling2D()(x)
        x = Dropout(0.4)(x)
        predictions = Dense(1, activation='sigmoid')(x)
        model = Model(inputs=base_model.input, outputs=predictions)

        print(f"Loading weights from {MODEL_PATH}...", flush=True)
        model.load_weights(MODEL_PATH)

        # 2. Prepare Image
        if not os.path.exists(img_path):
            print(f"Error: {img_path} not found!", flush=True)
            return

        print("Loading and preprocessing image...", flush=True)
        img = image.load_img(img_path, target_size=(IMG_SIZE, IMG_SIZE))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)

        # 3. Predict
        print("Running prediction...", flush=True)
        preds = model.predict(img_array, verbose=0)
        prob = float(preds[0][0])
        
        # Mapping: 0=diseased, 1=healthy
        # (Based on folder names 'diseased' and 'healthy' being sorted alphabetically)
        result = "healthy" if prob > 0.5 else "diseased"
        confidence = prob if prob > 0.5 else (1 - prob)

        print("\n" + "="*40, flush=True)
        print(f"IMAGE: {os.path.basename(img_path)}", flush=True)
        print(f"Raw Prediction Value: {prob:.4f}", flush=True)
        print(f"PREDICTED CLASS: {result}", flush=True)
        print(f"CONFIDENCE: {confidence*100:.2f}%", flush=True)
        print("="*40 + "\n", flush=True)

    except Exception as e:
        print(f"CRITICAL ERROR: {e}", flush=True)

if __name__ == "__main__":
    test_single_image(TEST_IMAGE)
