"""
Binary Leaf/Stem Health Detection Model Training Script
Detects whether a plant leaf or stem is healthy or diseased.
Uses MobileNetV3Large with transfer learning and binary classification.
"""

import os
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV3Large
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam

def create_model():
    """
    Create a binary classification model using MobileNetV3Large.
    
    Returns:
        keras.Model: Compiled model ready for training
    """
    # Load pre-trained MobileNetV3Large with ImageNet weights
    base_model = MobileNetV3Large(
        input_shape=(224, 224, 3),
        weights='imagenet',
        include_top=False
    )
    
    # Freeze base model weights (transfer learning)
    base_model.trainable = False
    
    # Create custom top layers for binary classification
    inputs = keras.Input(shape=(224, 224, 3))
    x = base_model(inputs, training=False)
    x = GlobalAveragePooling2D()(x)
    x = Dropout(0.2)(x)
    x = Dense(128, activation='relu')(x)
    x = Dropout(0.2)(x)
    outputs = Dense(1, activation='sigmoid')(x)  # Binary classification
    
    model = Model(inputs=inputs, outputs=outputs)
    
    # Compile with binary crossentropy loss
    model.compile(
        optimizer=Adam(learning_rate=1e-4),
        loss='binary_crossentropy',
        metrics=['accuracy']
    )
    
    return model

def create_data_generators():
    """
    Create data augmentation generators for training and validation.
    
    Returns:
        tuple: (train_generator, validation_generator)
    """
    # Training data augmentation
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )
    
    # Validation data (only rescaling, no augmentation)
    val_datagen = ImageDataGenerator(rescale=1./255)
    
    return train_datagen, val_datagen

def load_datasets(train_datagen, val_datagen, batch_size=32):
    """
    Load training and validation datasets from directories.
    
    Args:
        train_datagen: Training data generator with augmentation
        val_datagen: Validation data generator without augmentation
        batch_size: Number of samples per batch
    
    Returns:
        tuple: (train_dataset, validation_dataset)
    """
    # Load training dataset (Healthy=0, Diseased=1)
    train_dataset = train_datagen.flow_from_directory(
        'dataset/train',
        target_size=(224, 224),
        batch_size=batch_size,
        class_mode='binary',
        classes={'Healthy': 0, 'Diseased': 1},
        interpolation='bilinear'
    )
    
    # Load validation dataset
    val_dataset = val_datagen.flow_from_directory(
        'dataset/val',
        target_size=(224, 224),
        batch_size=batch_size,
        class_mode='binary',
        classes={'Healthy': 0, 'Diseased': 1},
        interpolation='bilinear'
    )
    
    return train_dataset, val_dataset

def train_model():
    """
    Train the binary classification model end-to-end.
    """
    print("=" * 60)
    print("Binary Leaf/Stem Health Detection Model Training")
    print("=" * 60)
    
    # Ensure model directory exists
    os.makedirs('models', exist_ok=True)
    
    # Create model
    print("\n[1/4] Creating model with MobileNetV3Large...")
    model = create_model()
    model.summary()
    
    # Create data generators
    print("\n[2/4] Creating data augmentation generators...")
    train_datagen, val_datagen = create_data_generators()
    
    # Load datasets
    print("\n[3/4] Loading datasets...")
    train_dataset, val_dataset = load_datasets(train_datagen, val_datagen, batch_size=32)
    
    print(f"Training samples: {train_dataset.samples}")
    print(f"Validation samples: {val_dataset.samples}")
    print(f"Classes: {train_dataset.class_indices}")
    
    # Train model
    print("\n[4/4] Training model for 10 epochs...")
    history = model.fit(
        train_dataset,
        epochs=10,
        validation_data=val_dataset,
        verbose=1
    )
    
    # Save model
    model_path = 'models/leaf_stem_healthy_diseased.keras'
    model.save(model_path)
    print(f"\n✓ Model saved to: {model_path}")
    
    # Print final metrics
    print("\n" + "=" * 60)
    print("Training Complete")
    print("=" * 60)
    final_train_accuracy = history.history['accuracy'][-1]
    final_val_accuracy = history.history['val_accuracy'][-1]
    final_val_loss = history.history['val_loss'][-1]
    
    print(f"Final Training Accuracy: {final_train_accuracy:.4f}")
    print(f"Final Validation Accuracy: {final_val_accuracy:.4f}")
    print(f"Final Validation Loss: {final_val_loss:.4f}")

if __name__ == '__main__':
    train_model()
