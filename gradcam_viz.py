import tensorflow as tf
import numpy as np
import cv2
import os
from tensorflow.keras.models import Model
from tensorflow.keras.applications.mobilenet_v3 import preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications import MobileNetV3Large
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout

# Config
IMG_SIZE = 224
MODEL_PATH = r"models\leaf_stem_healthy_diseased.h5"
IMG_PATH = "download.jpg"
OUTPUT_PATH = "gradcam_output.jpg"

def get_gradcam_heatmap(model, img_array, last_conv_layer_name, pred_index=None):
    grad_model = Model(
        [model.inputs], [model.get_layer(last_conv_layer_name).output, model.output]
    )

    with tf.GradientTape() as tape:
        last_conv_layer_output, preds = grad_model(img_array)
        if pred_index is None:
            pred_index = tf.argmax(preds[0])
        class_channel = preds[:, pred_index]

    grads = tape.gradient(class_channel, last_conv_layer_output)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

    last_conv_layer_output = last_conv_layer_output[0]
    heatmap = last_conv_layer_output @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)

    heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
    return heatmap.numpy()

def save_and_display_gradcam(img_path, heatmap, cam_path=OUTPUT_PATH):
    # Load original image
    img = cv2.imread(img_path)
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    
    # 1. Threshold the heatmap to create a binary mask
    # Normalize heatmap to 0-255 first for robust thresholding
    heatmap_norm = np.uint8(255 * heatmap)
    _, binary_mask = cv2.threshold(heatmap_norm, 127, 255, cv2.THRESH_BINARY)
    
    # 2. Find ALL contours of the activated regions
    contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # 3. Draw red outlines for EACH region found
    detected_count = 0
    for cnt in contours:
        # Ignore small contours (noise filtering > 200)
        if cv2.contourArea(cnt) > 200:
            # Get bounding rectangle
            x, y, w, h = cv2.boundingRect(cnt)
            
            # Draw a clear red rectangle (BGR: 0, 0, 255)
            # Thickness: 2 pixels
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            detected_count += 1
            print(f"Detected infected spot {detected_count} at [{x}, {y}, {w}, {h}]")

    if detected_count == 0:
        print("No significant activation regions detected (area > 200).")

    # Save the result (original image + red rectangles)
    cv2.imwrite(cam_path, img)
    print(f"Highlighted result saved to {cam_path}")

def run_gradcam():
    # 1. Rebuild Architecture
    print("Building model architecture...")
    base_model = MobileNetV3Large(weights=None, include_top=False, input_shape=(IMG_SIZE, IMG_SIZE, 3))
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dropout(0.4)(x)
    predictions = Dense(1, activation='sigmoid')(x)
    model = Model(inputs=base_model.input, outputs=predictions)

    print(f"Loading weights from {MODEL_PATH}...")
    model.load_weights(MODEL_PATH)

    # 2. Prepare Image
    if not os.path.exists(IMG_PATH):
        print(f"Error: {IMG_PATH} not found!")
        return

    img = image.load_img(IMG_PATH, target_size=(IMG_SIZE, IMG_SIZE))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    # 3. Find Last Conv Layer Name
    # For MobileNetV3Large, usually 'Conv_1' or similar before pooling
    last_conv_layer_name = None
    for layer in reversed(model.layers):
        if isinstance(layer, tf.keras.layers.Conv2D):
            last_conv_layer_name = layer.name
            break
    
    if not last_conv_layer_name:
        # Fallback search in base_model
        for layer in reversed(base_model.layers):
            if isinstance(layer, tf.keras.layers.Conv2D):
                last_conv_layer_name = layer.name
                break

    print(f"Using layer: {last_conv_layer_name}")

    # 4. Generate Heatmap
    # For binary classification with sigmoid, pred_index is None as we use the single output
    heatmap = get_gradcam_heatmap(model, img_array, last_conv_layer_name)
    save_and_display_gradcam(IMG_PATH, heatmap)

if __name__ == "__main__":
    run_gradcam()
