import tensorflow as tf
import numpy as np
import os
import sys
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications import MobileNetV3Large
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model

# Config
IMG_SIZE = 224
MODEL_PATH = r"models\leaf_stem_healthy_diseased.h5"
TEST_IMAGE = "download (1).jpg"

def rebuild_and_test():
    print("Starting script...", flush=True)
    try:
        # 1. Rebuild Architecture
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
        if not os.path.exists(TEST_IMAGE):
            print(f"Error: {TEST_IMAGE} not found!", flush=True)
            return

        print(f"Testing on {TEST_IMAGE}...", flush=True)
        img = image.load_img(TEST_IMAGE, target_size=(IMG_SIZE, IMG_SIZE))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array /= 255.0

        # 3. Predict
        print("Running prediction...", flush=True)
        preds = model.predict(img_array, verbose=0)
        prob = float(preds[0][0])
        
        # Mapping: 0=diseased, 1=healthy
        result = "healthy" if prob > 0.5 else "diseased"
        confidence = prob if prob > 0.5 else (1 - prob)

        print("\n" + "="*30, flush=True)
        print(f"FINAL RESULT FOR: {TEST_IMAGE}", flush=True)
        print(f"Raw Prediction Value: {prob:.4f}", flush=True)
        print(f"PREDICTED CLASS: {result}", flush=True)
        print(f"CONFIDENCE: {confidence*100:.2f}%", flush=True)
        print("="*30 + "\n", flush=True)

    except Exception as e:
        print(f"CRITICAL ERROR: {e}", flush=True)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    rebuild_and_test()
