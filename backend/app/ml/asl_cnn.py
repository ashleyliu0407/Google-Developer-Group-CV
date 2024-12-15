# -*- coding: utf-8 -*-
"""asl_cnn.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1DLG9I_C6K2MdWo16Qucj49gYCMCXTvNc
"""

!pip install kaggle
!mkdir -p ~/.kaggle

from google.colab import files
files.upload()

!mv kaggle.json ~/.kaggle/
!chmod 600 ~/.kaggle/kaggle.json

!kaggle datasets download ayuraj/asl-dataset
!unzip asl-dataset.zip

"""# Final Model"""

import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os
import shutil
import matplotlib.pyplot as plt
from pathlib import Path

class ASLBinaryClassifier:
    def __init__(self, target_letter, dataset_path='asl_dataset'):
        self.target_letter = target_letter
        self.dataset_path = dataset_path
        self.img_height = 64
        self.img_width = 64
        self.batch_size = 32
        self.model = None
        self.temp_dir = Path('temp_dataset')

    def prepare_data(self):
        """Prepare binary classification dataset for specific letter"""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
        os.makedirs(self.temp_dir / 'correct', exist_ok=True)
        os.makedirs(self.temp_dir / 'incorrect', exist_ok=True)

        source_dir = Path(self.dataset_path) / self.target_letter
        if not source_dir.exists():
            raise ValueError(f"No directory found for letter {self.target_letter}")

        for img in source_dir.glob('*'):
            if img.is_file() and img.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                shutil.copy2(img, self.temp_dir / 'correct')

        for letter_dir in Path(self.dataset_path).iterdir():
            if letter_dir.is_dir() and letter_dir.name != self.target_letter:
                for img in letter_dir.glob('*'):
                    if img.is_file() and img.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                        shutil.copy2(img, self.temp_dir / 'incorrect')

        train_datagen = ImageDataGenerator(
            rescale=1./255,
            rotation_range=15,
            width_shift_range=0.1,
            height_shift_range=0.1,
            zoom_range=0.1,
            horizontal_flip=False,
            validation_split=0.2
        )

        print(f"\nPreparing data for letter {self.target_letter}")
        self.train_generator = train_datagen.flow_from_directory(
            str(self.temp_dir),
            target_size=(self.img_height, self.img_width),
            batch_size=self.batch_size,
            class_mode='binary',
            subset='training'
        )

        self.validation_generator = train_datagen.flow_from_directory(
            str(self.temp_dir),
            target_size=(self.img_height, self.img_width),
            batch_size=self.batch_size,
            class_mode='binary',
            subset='validation'
        )

    def build_model(self):
        """Build binary classification model"""
        input_layer = layers.Input(shape=(self.img_height, self.img_width, 3))

        x = layers.Conv2D(32, (3, 3), activation='relu')(input_layer)
        x = layers.BatchNormalization()(x)
        x = layers.MaxPooling2D((2, 2))(x)
        x = layers.Dropout(0.25)(x)

        x = layers.Conv2D(64, (3, 3), activation='relu')(x)
        x = layers.BatchNormalization()(x)
        x = layers.MaxPooling2D((2, 2))(x)
        x = layers.Dropout(0.25)(x)

        x = layers.Conv2D(128, (3, 3), activation='relu')(x)
        x = layers.BatchNormalization()(x)
        x = layers.MaxPooling2D((2, 2))(x)
        x = layers.Dropout(0.25)(x)

        x = layers.Flatten()(x)
        x = layers.Dense(256, activation='relu')(x)
        x = layers.BatchNormalization()(x)
        x = layers.Dropout(0.5)(x)
        output_layer = layers.Dense(1, activation='sigmoid')(x)

        self.model = models.Model(inputs=input_layer, outputs=output_layer)
        self.model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy']
        )

        print(self.model.summary())

    def train(self, epochs=20):
        """Train the model"""
        callbacks = [
            tf.keras.callbacks.EarlyStopping(
                monitor='val_accuracy',
                patience=5,
                restore_best_weights=True
            ),
            tf.keras.callbacks.ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.2,
                patience=3,
                min_lr=1e-6
            )
        ]

        history = self.model.fit(
            self.train_generator,
            validation_data=self.validation_generator,
            epochs=epochs,
            callbacks=callbacks
        )

        return history

    def save_model(self):
        """Save the model"""
        save_path = Path('models')
        save_path.mkdir(exist_ok=True)
        self.model.save(save_path / f'asl_model_{self.target_letter}.keras')
        print(f"Model saved as 'models/asl_model_{self.target_letter}.keras'")

def train_letter_classifier(letter, dataset_path):
    try:
        print(f"\nTraining classifier for {letter}")
        classifier = ASLBinaryClassifier(letter, dataset_path)
        classifier.prepare_data()
        classifier.build_model()
        history = classifier.train()
        classifier.save_model()
        return classifier
    except Exception as e:
        print(f"Error training classifier for {letter}: {str(e)}")
        return None

dataset_path = './asl_dataset/asl_dataset'
for sign in 'abcdefghijklmnopqrstuvwxyz0123456789':
    classifier = train_letter_classifier(sign, dataset_path)

!zip -r /content/models.zip models/
from google.colab import files
files.download('/content/models.zip')
