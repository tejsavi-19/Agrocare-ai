import tensorflow as tf
import numpy as np
import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV3Large
from tensorflow.keras.applications.mobilenet_v3 import preprocess_input
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.preprocessing import image

# --- CONFIGURATION ---
IMG = 224
BATCH = 16
EPOCHS = 25
LR = 1e-4

# Correct dataset path relative to this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "../Plant dataset/leaves_healthy_or_diseased")
MODEL_SAVE_PATH = os.path.join(BASE_DIR, "leaf_stem_healthy_diseased.h5")
TEST_IMAGE_PATH = os.path.join(BASE_DIR, "../download.jpg")

print(f"Dataset Directory: {DATA_DIR}")
if not os.path.exists(DATA_DIR):
    raise FileNotFoundError(f"Dataset not found at {DATA_DIR}")

# --- DATA GENERATORS ---
from tensorflow.keras.layers import GaussianNoise

# Define a function for the random augmentations that ImageDataGenerator can't handle well
def apply_advanced_aug(img):
    # Preprocess first
    img = preprocess_input(img)
    # Then apply noise
    noise = np.random.normal(0, 0.05, img.shape).astype('float32') # Smaller noise for [-1, 1] range
    return img + noise

train_datagen = ImageDataGenerator(
    preprocessing_function=apply_advanced_aug,
    rotation_range=90, 
    width_shift_range=0.3,
    height_shift_range=0.3,
    shear_range=0.3,
    zoom_range=0.4,
    horizontal_flip=True,
    vertical_flip=True,
    brightness_range=[0.3, 1.7], 
    channel_shift_range=50.0, 
    fill_mode='nearest',
    validation_split=0.2
)

val_datagen = ImageDataGenerator(
    preprocessing_function=preprocess_input,
    validation_split=0.2
)

print("Loading Training Data...")
train_generator = train_datagen.flow_from_directory(
    DATA_DIR,
    target_size=(IMG, IMG),
    batch_size=BATCH,
    class_mode='binary',
    subset='training',
    shuffle=True
)

print("Loading Validation Data...")
validation_generator = val_datagen.flow_from_directory(
    DATA_DIR,
    target_size=(IMG, IMG),
    batch_size=BATCH,
    class_mode='binary',
    subset='validation',
    shuffle=False
)

# --- CLASS WEIGHTS ---
labels = train_generator.classes
class_indices = train_generator.class_indices
print(f"Class Mapping: {class_indices}")
idx_to_class = {v: k for k, v in class_indices.items()}

count_0 = np.sum(labels == 0)
count_1 = np.sum(labels == 1)
total = len(labels)

if count_0 == 0 or count_1 == 0:
    weight_0, weight_1 = 1.0, 1.0
else:
    weight_0 = (1 / count_0) * (total / 2.0)
    weight_1 = (1 / count_1) * (total / 2.0)

class_weights = {0: weight_0, 1: weight_1}
print(f"Class Weights: {class_weights}")

# --- MODEL BUILD ---
print("Building Model (Phase 3: Robustness)...")
base_model = MobileNetV3Large(
    include_top=False,
    input_shape=(IMG, IMG, 3),
    weights="imagenet"
)

# Freeze base model initially
base_model.trainable = False

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dropout(0.5)(x) # Higher dropout
output = Dense(1, activation="sigmoid")(x)

model = Model(inputs=base_model.input, outputs=output)

model.compile(
    optimizer=Adam(learning_rate=LR),
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

# --- CALLBACKS ---
callbacks = [
    EarlyStopping(
        monitor='val_loss',
        patience=5,
        restore_best_weights=True,
        verbose=1
    ),
    ModelCheckpoint(
        MODEL_SAVE_PATH,
        monitor='val_loss',
        save_best_only=True,
        verbose=1
    )
]

# --- TRAINING ---
print("\n=== STARTING TRAINING ===")
history = model.fit(
    train_generator,
    validation_data=validation_generator,
    epochs=EPOCHS,
    class_weight=class_weights,
    callbacks=callbacks
)

# --- FINE TUNING (OPTIONAL but good for accuracy) ---
# Unfreeze top layers
print("\n=== FINE TUNING ===")
base_model.trainable = True
# Freeze all layers except the last 20
for layer in base_model.layers[:-20]:
    layer.trainable = False

model.compile(
    optimizer=Adam(learning_rate=1e-5),  # Lower LR for fine-tuning
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

model.fit(
    train_generator,
    validation_data=validation_generator,
    epochs=10, # Fine tune for a few more epochs
    class_weight=class_weights,
    callbacks=callbacks
)

print(f"\nModel saved to {MODEL_SAVE_PATH}")


# --- TEST ON SINGLE IMAGE ---
print("\n=== TESTING ON download.jpg ===")

if os.path.exists(TEST_IMAGE_PATH):
    img = image.load_img(TEST_IMAGE_PATH, target_size=(IMG, IMG))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    prediction = model.predict(img_array)[0][0]
    
    # Logic: < 0.5 is class 0, >= 0.5 is class 1
    # We need to map probability to class name
    
    # Identify which class is 0 and 1
    # Typically alphabetic order: diseased=0, healthy=1 (if folders are named that way)
    # But we trust class_indices printed above.
    
    print(f"Raw Prediction Probability: {prediction:.4f}")
    
    if prediction < 0.5:
        predicted_class_idx = 0
        confidence = 1.0 - prediction
    else:
        predicted_class_idx = 1
        confidence = prediction

    predicted_label = idx_to_class[predicted_class_idx]
    
    print(f"PREDICTED CLASS: {predicted_label}")
    print(f"CONFIDENCE: {confidence:.2%}")
else:
    print(f"Error: Test image not found at {TEST_IMAGE_PATH}")
