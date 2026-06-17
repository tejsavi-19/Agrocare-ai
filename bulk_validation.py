import tensorflow as tf
import numpy as np
import os
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v3 import preprocess_input
from tensorflow.keras.models import Model
from tensorflow.keras.applications import MobileNetV3Large
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout

# Config
IMG_SIZE = 224
MODEL_PATH = r"models\leaf_stem_healthy_diseased.h5"
HEALTHY_DIR = r"healthy\healthy"

def load_robust_model():
    base_model = MobileNetV3Large(include_top=False, input_shape=(IMG_SIZE, IMG_SIZE, 3), weights=None)
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dropout(0.4)(x)
    output = Dense(1, activation="sigmoid")(x)
    model = Model(inputs=base_model.input, outputs=output)
    model.load_weights(MODEL_PATH)
    return model

def run_bulk_healthy_test():
    print("\n" + "="*80)
    print("BULK HEALTHY DATASET VALIDATION")
    print("="*80)
    
    if not os.path.exists(HEALTHY_DIR):
        print(f"Error: Healthy directory not found at {HEALTHY_DIR}")
        return

    model = load_robust_model()
    
    files = [f for f in os.listdir(HEALTHY_DIR) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    total = len(files)
    print(f"Found {total} images in the healthy folder.")
    
    passed = 0
    failed = []
    confidences = []

    print("Running predictions...")
    
    for i, img_name in enumerate(files):
        path = os.path.join(HEALTHY_DIR, img_name)
        
        img = image.load_img(path, target_size=(IMG_SIZE, IMG_SIZE))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)
        
        pred = model.predict(img_array, verbose=0)[0][0]
        
        # Result: > 0.5 is Healthy
        is_healthy = pred > 0.5
        conf = pred if is_healthy else (1 - pred)
        confidences.append(conf)
        
        if is_healthy:
            passed += 1
        else:
            failed.append((img_name, pred))
        
        if (i+1) % 50 == 0:
            print(f"Progress: {i+1}/{total}...")

    print("\n" + "="*80)
    print("FINAL RESULTS")
    print("="*80)
    print(f"Total Images: {total}")
    print(f"Correct (Healthy): {passed}")
    print(f"Incorrect (Diseased): {len(failed)}")
    print(f"Accuracy: {(passed/total)*100:.2f}%")
    print(f"Mean Confidence: {np.mean(confidences)*100:.2f}%")
    
    if failed:
        print("\nFailed Images (False Positives for Disease):")
        for f in failed[:20]: # Show first 20 errors
            print(f" - {f[0]} (Predicted Value: {f[1]:.4f})")
        if len(failed) > 20:
            print(f" ... and {len(failed)-20} more.")
    
    print("="*80 + "\n")

if __name__ == "__main__":
    run_bulk_healthy_test()
