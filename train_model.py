import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D, BatchNormalization
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
from tensorflow.keras.optimizers import Adam
import os

train_dir = "dataset/train"
test_dir  = "dataset/test"

# Augmentation
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    zoom_range=0.2,
    horizontal_flip=True,
    width_shift_range=0.1,
    height_shift_range=0.1,
    brightness_range=[0.8, 1.2],
    fill_mode='nearest'
)
test_datagen = ImageDataGenerator(rescale=1./255)

train_data = train_datagen.flow_from_directory(
    train_dir, target_size=(224,224),
    batch_size=32, class_mode='categorical', shuffle=True
)
test_data = test_datagen.flow_from_directory(
    test_dir, target_size=(224,224),
    batch_size=32, class_mode='categorical', shuffle=False
)

print(f"Classes : {train_data.num_classes}")
print(f"Train   : {train_data.samples}")
print(f"Test    : {test_data.samples}")

assert train_data.num_classes == test_data.num_classes

# --- MobileNetV2 base (pretrained on ImageNet) ---
base_model = MobileNetV2(input_shape=(224,224,3), include_top=False, weights='imagenet')
base_model.trainable = False  # Freeze base first

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = BatchNormalization()(x)
x = Dense(256, activation='relu')(x)
x = Dropout(0.4)(x)
x = Dense(128, activation='relu')(x)
x = Dropout(0.3)(x)
output = Dense(train_data.num_classes, activation='softmax')(x)

model = Model(inputs=base_model.input, outputs=output)

# Phase 1 — Train only top layers
print("\n🔵 Phase 1: Training top layers...")
model.compile(optimizer=Adam(0.001), loss='categorical_crossentropy', metrics=['accuracy'])

os.makedirs("model", exist_ok=True)

callbacks = [
    EarlyStopping(monitor='val_accuracy', patience=5, restore_best_weights=True, verbose=1),
    ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3, verbose=1),
    ModelCheckpoint('model/best_fruit_model.h5', monitor='val_accuracy', save_best_only=True, verbose=1)
]

model.fit(train_data, validation_data=test_data, epochs=20, callbacks=callbacks)

# Phase 2 — Unfreeze and fine-tune
print("\n🟡 Phase 2: Fine-tuning...")
base_model.trainable = True

# Only unfreeze last 40 layers
for layer in base_model.layers[:-40]:
    layer.trainable = False

model.compile(optimizer=Adam(1e-5), loss='categorical_crossentropy', metrics=['accuracy'])

callbacks2 = [
    EarlyStopping(monitor='val_accuracy', patience=7, restore_best_weights=True, verbose=1),
    ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3, verbose=1),
    ModelCheckpoint('model/best_fruit_model.h5', monitor='val_accuracy', save_best_only=True, verbose=1)
]

history = model.fit(train_data, validation_data=test_data, epochs=30, callbacks=callbacks2)

model.save("model/fruit_model.h5")

print("\n✅ Training complete!")
print(f"Best val accuracy: {max(history.history['val_accuracy']):.4f}")
