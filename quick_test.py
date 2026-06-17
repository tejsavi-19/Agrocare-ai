import tensorflow as tf
import numpy as np
import os
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v3 import preprocess_input

# Config
IMG = 224
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models/leaf_stem_healthy_diseased.h5")
TEST_IMAGE_PATH = os.path.join(BASE_DIR, "download.jpg")

print(f"Loading model from {MODEL_PATH}...")
model = tf.keras.models.load_model(MODEL_PATH, compile=False)

print(f"Testing on {TEST_IMAGE_PATH}...")
if os.path.exists(TEST_IMAGE_PATH):
    img = image.load_img(TEST_IMAGE_PATH, target_size=(IMG, IMG))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    prediction = model.predict(img_array)[0][0]
    
    # Mapping based on alphabetical order: diseased=0, healthy=1
    if prediction < 0.5:
        label = "diseased"
        confidence = (1.0 - prediction) * 100
    else:
        label = "healthy"
        confidence = prediction * 100

    print(f"Raw Prediction: {prediction:.4f}")
    print(f"PREDICTED CLASS: {label}")
    print(f"CONFIDENCE: {confidence:.2f}%")
else:
    print("Error: download.jpg not found.")
