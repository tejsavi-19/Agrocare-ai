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

# List of images to test based on file system check
# format: (filename, expected_class)
TEST_IMAGES = [
    ("download.jpg", "Healthy"),
    ("download (1).jpg", "Healthy"),
    ("anthracnose-1-460x263.webp", "Diseased"),
    ("di.jpg", "Diseased"),
    ("di2.jpg", "Diseased"),
    ("di3.jpg", "Diseased"),
    ("di4.jpg", "Diseased"),
    ("di6.jpg", "Diseased"),
    ("h1.jpg", "Healthy"),
    ("h2.jpg", "Healthy"),
    ("h3.jpg", "Healthy"),
    ("h4.jpg", "Healthy"),
    ("h5.jpg", "Healthy"),
    ("h6.jpg", "Healthy"),
    ("h8.webp", "Healthy"),
    ("di7.jpg", "Diseased"),
    ("di8.jpg", "Diseased")
]

def load_robust_model():
    base_model = MobileNetV3Large(include_top=False, input_shape=(IMG_SIZE, IMG_SIZE, 3), weights=None)
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dropout(0.4)(x)
    output = Dense(1, activation="sigmoid")(x)
    model = Model(inputs=base_model.input, outputs=output)
    model.load_weights(MODEL_PATH)
    return model

def run_batch_test():
    print("\n" + "="*80)
    print("CONSOLIDATED BATCH VERIFICATION REPORT (17 IMAGES)")
    print("="*80)
    
    model = load_robust_model()
    
    results = []
    
    for img_name, expected in TEST_IMAGES:
        if not os.path.exists(img_name):
            results.append((img_name, "NOT FOUND", expected, "-", "⚠️ SKIP"))
            continue
            
        img = image.load_img(img_name, target_size=(IMG_SIZE, IMG_SIZE))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)
        
        pred = model.predict(img_array, verbose=0)[0][0]
        label = "Healthy" if pred > 0.5 else "Diseased"
        confidence = pred if pred > 0.5 else (1 - pred)
        
        status = "✅ PASS" if label.lower() == expected.lower() else "❌ FAIL"
        results.append((img_name, label, expected, f"{confidence*100:.2f}%", status))

    print(f"{'Image Name':<30} | {'Predicted':<10} | {'Expected':<10} | {'Confidence':<10} | {'Status'}")
    print("-" * 90)
    for res in results:
        print(f"{res[0]:<30} | {res[1]:<10} | {res[2]:<10} | {res[3]:<10} | {res[4]}")
    print("="*90 + "\n")

if __name__ == "__main__":
    run_batch_test()
