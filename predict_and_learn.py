import tensorflow as tf
import numpy as np
import os
import argparse
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v3 import preprocess_input
from tensorflow.keras.models import Model
from tensorflow.keras.applications import MobileNetV3Large
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.optimizers import Adam

# Config
IMG_SIZE = 224
MODEL_PATH = r"models\leaf_stem_healthy_diseased.h5"

def load_robust_model():
    base_model = MobileNetV3Large(include_top=False, input_shape=(IMG_SIZE, IMG_SIZE, 3), weights=None)
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dropout(0.4)(x)
    output = Dense(1, activation="sigmoid")(x)
    model = Model(inputs=base_model.input, outputs=output)
    model.load_weights(MODEL_PATH)
    return model

def predict_and_learn(img_path, ground_truth_label=None):
    if not os.path.exists(img_path):
        print(f"Error: {img_path} not found!")
        return

    # 1. Prediction
    model = load_robust_model()
    img_orig = image.load_img(img_path, target_size=(IMG_SIZE, IMG_SIZE))
    img_array = image.img_to_array(img_orig)
    img_tensor = preprocess_input(np.expand_dims(img_array, axis=0))
    
    pred_val = model.predict(img_tensor, verbose=0)[0][0]
    pred_label = "Healthy" if pred_val > 0.5 else "Diseased"
    confidence = pred_val if pred_val > 0.5 else (1 - pred_val)
    
    print("\n" + "="*40)
    print(f"PREDICTION FOR: {os.path.basename(img_path)}")
    print(f"Result: {pred_label} ({confidence*100:.2f}%)")
    print("="*40)

    # 2. Continuous Learning (if label provided)
    if ground_truth_label is not None:
        print(f"\nAbsorbing image into model weights (Label: {ground_truth_label})...")
        label_val = 1.0 if ground_truth_label.lower() == 'healthy' else 0.0
        
        # Compile for a quick update
        model.trainable = True
        model.compile(optimizer=Adam(learning_rate=5e-5), loss="binary_crossentropy")
        
        # Create augmented variations for better generalization to SIMILAR images
        datagen = ImageDataGenerator(
            rotation_range=20,
            width_shift_range=0.1,
            height_shift_range=0.1,
            brightness_range=[0.8, 1.2],
            horizontal_flip=True,
            fill_mode='nearest'
        )
        
        # Create 20 augmented versions of this one image
        # Note: input is already preprocessed by preprocess_input (usually -1 to 1 range)
        # ImageDataGenerator transformations work on raw pixel data or preprocessed data 
        # but here we use the already preprocessed tensor.
        aug_it = datagen.flow(np.repeat(img_tensor, 20, axis=0), np.full(20, label_val), batch_size=4)
        
        model.fit(aug_it, epochs=5, verbose=0)
        
        # Save updated weights
        model.save(MODEL_PATH)
        print("Success: Model updated with augmented learning for better generalization.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Predict and optionally learn from a single image.")
    parser.add_argument("image", help="Path to the image file")
    parser.add_argument("--label", help="Ground truth label (Healthy/Diseased) for learning", choices=['Healthy', 'Diseased', 'healthy', 'diseased'])
    
    args = parser.parse_args()
    predict_and_learn(args.image, args.label)
