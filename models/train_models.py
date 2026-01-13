"""
Machine Learning Model Training Script
Trains Logistic Regression, Random Forest, SVM, and CNN models
for UPI Fraud Detection
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv1D, MaxPooling1D, Flatten, Dropout, Reshape
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
import joblib
import os

print("=" * 60)
print("UPI Fraud Detection - Model Training")
print("=" * 60)

# Step 1: Load Dataset
print("\n[Step 1] Loading dataset...")
dataset_path = 'data/upi_transactions.csv'

if not os.path.exists(dataset_path):
    print(f"Error: Dataset not found at {dataset_path}")
    print("Please run: python data/generate_dataset.py")
    exit(1)

df = pd.read_csv(dataset_path)
print(f"Dataset loaded: {len(df)} transactions")
print(f"Features: {df.columns.tolist()}")

# Step 2: Data Preprocessing
print("\n[Step 2] Preprocessing data...")

# Separate features and target
X = df.drop(['transaction_id', 'fraud'], axis=1)
y = df['fraud']

# Display class distribution
print(f"\nClass Distribution:")
print(f"Legitimate (0): {sum(y == 0)} ({sum(y == 0)/len(y)*100:.2f}%)")
print(f"Fraudulent (1): {sum(y == 1)} ({sum(y == 1)/len(y)*100:.2f}%)")

# Split data: 70% train, 15% validation, 15% test
X_train, X_temp, y_train, y_temp = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)
X_val, X_test, y_val, y_test = train_test_split(
    X_temp, y_temp, test_size=0.5, random_state=42, stratify=y_temp
)

print(f"\nData Split:")
print(f"Training: {len(X_train)} samples")
print(f"Validation: {len(X_val)} samples")
print(f"Test: {len(X_test)} samples")

# Feature Scaling (important for ML models)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)
X_test_scaled = scaler.transform(X_test)

# Save scaler for later use in production
scaler_path = 'models/scaler.pkl'
os.makedirs('models', exist_ok=True)
joblib.dump(scaler, scaler_path)
print(f"\nScaler saved to: {scaler_path}")

# Step 3: Train Logistic Regression
print("\n" + "=" * 60)
print("[Step 3] Training Logistic Regression Model...")
print("=" * 60)

lr_model = LogisticRegression(random_state=42, max_iter=1000, class_weight='balanced')
lr_model.fit(X_train_scaled, y_train)

# Predictions
y_train_pred_lr = lr_model.predict(X_train_scaled)
y_val_pred_lr = lr_model.predict(X_val_scaled)
y_test_pred_lr = lr_model.predict(X_test_scaled)

# Accuracy
train_acc_lr = accuracy_score(y_train, y_train_pred_lr)
val_acc_lr = accuracy_score(y_val, y_val_pred_lr)
test_acc_lr = accuracy_score(y_test, y_test_pred_lr)

print(f"\nLogistic Regression Results:")
print(f"Training Accuracy: {train_acc_lr*100:.2f}%")
print(f"Validation Accuracy: {val_acc_lr*100:.2f}%")
print(f"Test Accuracy: {test_acc_lr*100:.2f}%")

# Save model
lr_path = 'models/fraud_detection_lr.pkl'
joblib.dump(lr_model, lr_path)
print(f"Model saved to: {lr_path}")

# Step 4: Train Random Forest
print("\n" + "=" * 60)
print("[Step 4] Training Random Forest Model...")
print("=" * 60)

rf_model = RandomForestClassifier(
    n_estimators=100,
    max_depth=20,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    class_weight='balanced',
    n_jobs=-1
)
rf_model.fit(X_train, y_train)  # RF doesn't always need scaling

# Predictions
y_train_pred_rf = rf_model.predict(X_train)
y_val_pred_rf = rf_model.predict(X_val)
y_test_pred_rf = rf_model.predict(X_test)

# Accuracy
train_acc_rf = accuracy_score(y_train, y_train_pred_rf)
val_acc_rf = accuracy_score(y_val, y_val_pred_rf)
test_acc_rf = accuracy_score(y_test, y_test_pred_rf)

print(f"\nRandom Forest Results:")
print(f"Training Accuracy: {train_acc_rf*100:.2f}%")
print(f"Validation Accuracy: {val_acc_rf*100:.2f}%")
print(f"Test Accuracy: {test_acc_rf*100:.2f}%")

# Save model
rf_path = 'models/fraud_detection_rf.pkl'
joblib.dump(rf_model, rf_path)
print(f"Model saved to: {rf_path}")

# Step 5: Train SVM
print("\n" + "=" * 60)
print("[Step 5] Training SVM Model...")
print("=" * 60)

svm_model = SVC(
    kernel='rbf',
    C=1.0,
    gamma='scale',
    random_state=42,
    class_weight='balanced',
    probability=True
)
svm_model.fit(X_train_scaled, y_train)

# Predictions
y_train_pred_svm = svm_model.predict(X_train_scaled)
y_val_pred_svm = svm_model.predict(X_val_scaled)
y_test_pred_svm = svm_model.predict(X_test_scaled)

# Accuracy
train_acc_svm = accuracy_score(y_train, y_train_pred_svm)
val_acc_svm = accuracy_score(y_val, y_val_pred_svm)
test_acc_svm = accuracy_score(y_test, y_test_pred_svm)

print(f"\nSVM Results:")
print(f"Training Accuracy: {train_acc_svm*100:.2f}%")
print(f"Validation Accuracy: {val_acc_svm*100:.2f}%")
print(f"Test Accuracy: {test_acc_svm*100:.2f}%")

# Save model
svm_path = 'models/fraud_detection_svm.pkl'
joblib.dump(svm_model, svm_path)
print(f"Model saved to: {svm_path}")

# Step 6: Train CNN (Convolutional Neural Network)
print("\n" + "=" * 60)
print("[Step 6] Training CNN Model...")
print("=" * 60)

# Reshape data for CNN (1D convolution expects 3D input: samples, timesteps, features)
# We'll treat features as a sequence for 1D convolution
X_train_cnn = X_train_scaled.reshape(X_train_scaled.shape[0], X_train_scaled.shape[1], 1)
X_val_cnn = X_val_scaled.reshape(X_val_scaled.shape[0], X_val_scaled.shape[1], 1)
X_test_cnn = X_test_scaled.reshape(X_test_scaled.shape[0], X_test_scaled.shape[1], 1)

print(f"CNN Input Shape: {X_train_cnn.shape}")

# Build CNN Model
cnn_model = Sequential([
    # First Convolutional Layer
    Conv1D(filters=64, kernel_size=3, activation='relu', input_shape=(X_train_cnn.shape[1], 1)),
    MaxPooling1D(pool_size=2),
    Dropout(0.25),
    
    # Second Convolutional Layer
    Conv1D(filters=32, kernel_size=3, activation='relu'),
    MaxPooling1D(pool_size=2),
    Dropout(0.25),
    
    # Flatten for Dense layers
    Flatten(),
    
    # Dense layers
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(64, activation='relu'),
    Dropout(0.5),
    
    # Output layer (binary classification)
    Dense(1, activation='sigmoid')
])

# Compile model
cnn_model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

print("\nCNN Model Architecture:")
cnn_model.summary()

# Callbacks
early_stopping = EarlyStopping(
    monitor='val_loss',
    patience=10,
    restore_best_weights=True
)

checkpoint = ModelCheckpoint(
    'models/fraud_detection_cnn_best.h5',
    monitor='val_accuracy',
    save_best_only=True,
    mode='max'
)

# Train CNN
print("\nTraining CNN model (this may take several minutes)...")
history = cnn_model.fit(
    X_train_cnn, y_train,
    batch_size=32,
    epochs=50,
    validation_data=(X_val_cnn, y_val),
    callbacks=[early_stopping, checkpoint],
    verbose=1
)

# Load best model
cnn_model.load_weights('models/fraud_detection_cnn_best.h5')

# Predictions
y_train_pred_cnn = (cnn_model.predict(X_train_cnn) > 0.5).astype(int).flatten()
y_val_pred_cnn = (cnn_model.predict(X_val_cnn) > 0.5).astype(int).flatten()
y_test_pred_cnn = (cnn_model.predict(X_test_cnn) > 0.5).astype(int).flatten()

# Accuracy
train_acc_cnn = accuracy_score(y_train, y_train_pred_cnn)
val_acc_cnn = accuracy_score(y_val, y_val_pred_cnn)
test_acc_cnn = accuracy_score(y_test, y_test_pred_cnn)

print(f"\nCNN Results:")
print(f"Training Accuracy: {train_acc_cnn*100:.2f}%")
print(f"Validation Accuracy: {val_acc_cnn*100:.2f}%")
print(f"Test Accuracy: {test_acc_cnn*100:.2f}%")

# Save final CNN model
cnn_path = 'models/fraud_detection_cnn.h5'
cnn_model.save(cnn_path)
print(f"Model saved to: {cnn_path}")

# Step 7: Model Comparison
print("\n" + "=" * 60)
print("[Step 7] Model Comparison (Test Set Accuracy)")
print("=" * 60)
print(f"{'Model':<25} {'Accuracy':<15}")
print("-" * 40)
print(f"{'Logistic Regression':<25} {test_acc_lr*100:>6.2f}%")
print(f"{'Random Forest':<25} {test_acc_rf*100:>6.2f}%")
print(f"{'SVM':<25} {test_acc_svm*100:>6.2f}%")
print(f"{'CNN (Final Model)':<25} {test_acc_cnn*100:>6.2f}%")
print("=" * 60)

# Detailed CNN Report
print("\n" + "=" * 60)
print("CNN Model - Detailed Classification Report")
print("=" * 60)
print(classification_report(y_test, y_test_pred_cnn, target_names=['Legitimate', 'Fraud']))

print("\n" + "=" * 60)
print("CNN Model - Confusion Matrix")
print("=" * 60)
cm = confusion_matrix(y_test, y_test_pred_cnn)
print("                Predicted")
print("              Legit  Fraud")
print(f"Actual Legit   {cm[0][0]:4d}   {cm[0][1]:4d}")
print(f"       Fraud   {cm[1][0]:4d}   {cm[1][1]:4d}")

# Summary
print("\n" + "=" * 60)
print("TRAINING COMPLETE!")
print("=" * 60)
print("\nBest Model: CNN (Convolutional Neural Network)")
print(f"Final Test Accuracy: {test_acc_cnn*100:.2f}%")
print("\nAll models saved in 'models/' directory:")
print("  - fraud_detection_lr.pkl (Logistic Regression)")
print("  - fraud_detection_rf.pkl (Random Forest)")
print("  - fraud_detection_svm.pkl (SVM)")
print("  - fraud_detection_cnn.h5 (CNN - Final Model)")
print("  - scaler.pkl (Feature Scaler)")
print("\nYou can now use the CNN model for real-time fraud detection!")
