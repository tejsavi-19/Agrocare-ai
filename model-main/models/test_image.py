import tensorflow as tf
import numpy as np
import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications.mobilenet_v3 import MobileNetV3Large, preprocess_input
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping

IMG = 224
BATCH = 16
EPOCHS = 25

TRAIN = "dataset/train"
VAL = "dataset/val"

os.makedirs("models", exist_ok=True)

train_gen = ImageDataGenerator(
    preprocessing_function=preprocess_input,
    rotation_range=25,
    zoom_range=0.25,
    horizontal_flip=True,
    brightness_range=[0.6,1.4]
)

val_gen = ImageDataGenerator(preprocessing_function=preprocess_input)

train = train_gen.flow_from_directory(
    TRAIN,
    target_size=(IMG,IMG),
    batch_size=BATCH,
    class_mode="binary"
)

val = val_gen.flow_from_directory(
    VAL,
    target_size=(IMG,IMG),
    batch_size=BATCH,
    class_mode="binary"
)

print("\nClass mapping:", train.class_indices)

# ---- CLASS WEIGHTS ----
counts = np.bincount(train.classes.astype(int))
total = sum(counts)

class_weights = {
    0: total/(2*counts[0]),
    1: total/(2*counts[1])
}

print("\nClass weights:", class_weights)

base = MobileNetV3Large(
    include_top=False,
    input_shape=(IMG,IMG,3),
    weights="imagenet"
)

base.trainable = False

x = base.output
x = GlobalAveragePooling2D()(x)
x = Dropout(0.3)(x)
out = Dense(1, activation="sigmoid")(x)

model = Model(base.input, out)

model.compile(
    optimizer=Adam(1e-4),
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

stop = EarlyStopping(patience=5, restore_best_weights=True)

print("\n=== PHASE 1 TRAINING ===")

model.fit(
    train,
    validation_data=val,
    epochs=10,
    class_weight=class_weights,
    callbacks=[stop]
)

print("\n=== PHASE 2 FINE TUNING ===")

base.trainable = True

model.compile(
    optimizer=Adam(1e-5),
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

model.fit(
    train,
    validation_data=val,
    epochs=15,
    class_weight=class_weights,
    callbacks=[stop]
)

model.save("models/leaf_stem_healthy_diseased.h5")

print("\nMODEL SAVED: models/leaf_stem_healthy_diseased.h5")
