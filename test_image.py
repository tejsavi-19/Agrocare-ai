import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image

MODEL_PATH = r"models\healthy_diseased.h5"
IMG_SIZE = (224,224)

model = tf.keras.models.load_model(MODEL_PATH)

img_path = input("Enter image path: ")

img = image.load_img(img_path, target_size=IMG_SIZE)
img = image.img_to_array(img)
img = img / 255.0
img = np.expand_dims(img, axis=0)

pred = model.predict(img)[0][0]

if pred < 0.5:
    print("\nPrediction: Healthy")
    print("Confidence:", round(float(1-pred),3))
else:
    print("\nPrediction: Diseased")
    print("Confidence:", round(float(pred),3))
