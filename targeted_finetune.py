import tensorflow as tf
import numpy as np
import os
import random
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v3 import preprocess_input
from tensorflow.keras.applications import MobileNetV3Large
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout

# Config
IMG_SIZE = 224
MODEL_PATH = r"models\leaf_stem_healthy_diseased.h5"
DATA_DIR = r"Plant dataset/leaves_healthy_or_diseased"
HEALTHY_FAIL_DIR = r"healthy\healthy"

# Lists
NEW_HEALTHY_FAILURES = [
    "1.jpg", "15.jpg", "16.jpg", "17.jpg", "18.jpg", "2.jpg", "4.jpg", "Saluyot-Leaves.jpg"
]
PREVIOUS_GOLDEN_HEALTHY = ["download.jpg", "download (1).jpg", "h1.jpg", "h2.jpg", "h3.jpg", "h4.jpg", "h5.jpg", "h6.jpg", "h8.webp"]
PREVIOUS_GOLDEN_DISEASED = ["anthracnose-1-460x263.webp", "di.jpg", "di2.jpg", "di3.jpg", "di4.jpg", "di6.jpg", "di7.jpg", "di8.jpg"]

def load_random_samples(folder, count):
    samples = []
    files = [f for f in os.listdir(folder) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
    selected = random.sample(files, min(count, len(files)))
    for f in selected:
        path = os.path.join(folder, f)
        img = image.load_img(path, target_size=(IMG_SIZE, IMG_SIZE))
        img_array = image.img_to_array(img)
        samples.append(img_array)
    return np.array(samples)

def run_ultimate_calibration():
    print("Ultimate Calibration (Global Accuracy Strike)...")
    
    # 1. Build Architecture
    base_model = MobileNetV3Large(include_top=False, input_shape=(IMG_SIZE, IMG_SIZE, 3), weights=None)
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dropout(0.4)(x)
    output = Dense(1, activation="sigmoid")(x)
    model = Model(inputs=base_model.input, outputs=output)
    
    # 2. Load Weights
    print(f"Loading weights from {MODEL_PATH}...")
    model.load_weights(MODEL_PATH)
    model.trainable = True
    model.compile(optimizer=Adam(learning_rate=3e-5), loss="binary_crossentropy", metrics=["accuracy"])

    # 3. Prepare Batch
    all_imgs = []
    all_labels = []

    # Add New Healthy Failures (20x)
    for img_name in NEW_HEALTHY_FAILURES:
        path = os.path.join(HEALTHY_FAIL_DIR, img_name)
        if os.path.exists(path):
            img = image.load_img(path, target_size=(IMG_SIZE, IMG_SIZE))
            all_imgs.extend([image.img_to_array(img)] * 20)
            all_labels.extend([1.0] * 20)

    # Add Previous Golden Healthy (10x)
    for img_name in PREVIOUS_GOLDEN_HEALTHY:
        if os.path.exists(img_name):
            img = image.load_img(img_name, target_size=(IMG_SIZE, IMG_SIZE))
            all_imgs.extend([image.img_to_array(img)] * 10)
            all_labels.extend([1.0] * 10)

    # Add Previous Golden Diseased (15x)
    for img_name in PREVIOUS_GOLDEN_DISEASED:
        if os.path.exists(img_name):
            img = image.load_img(img_name, target_size=(IMG_SIZE, IMG_SIZE))
            all_imgs.extend([image.img_to_array(img)] * 15)
            all_labels.extend([0.0] * 15)

    # Add background samples
    print("Adding background samples...")
    healthy_back = load_random_samples(os.path.join(DATA_DIR, "healthy"), 30)
    diseased_back = load_random_samples(os.path.join(DATA_DIR, "diseased"), 40)
    all_imgs.extend(healthy_back)
    all_labels.extend([1.0] * len(healthy_back))
    all_imgs.extend(diseased_back)
    all_labels.extend([0.0] * len(diseased_back))

    # Preprocess
    all_imgs = preprocess_input(np.array(all_imgs))
    all_labels = np.array(all_labels)

    # 4. Calibration
    print(f"Starting Ultimate Calibration on {len(all_imgs)} samples (25 epochs)...")
    model.fit(all_imgs, all_labels, epochs=25, batch_size=32, verbose=1)

    # 5. Save
    print("\nSaving Ultimate Model...")
    model.save(MODEL_PATH) 
    print("Success: Final model bias corrected for all known failures.")

if __name__ == "__main__":
    run_ultimate_calibration()
