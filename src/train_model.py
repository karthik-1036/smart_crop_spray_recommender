# src/train_model.py

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
import os

# Load dataset
data_path = os.path.join("data", "spray_dataset_expanded.csv")
df = pd.read_csv(data_path)

# Encode categorical features
cat_cols = ['Crop', 'Growth_Stage', 'Last_Spray']
label_encoders = {}

for col in cat_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# Encode target
target_encoder = LabelEncoder()
df['Target_Spray'] = target_encoder.fit_transform(df['Target_Spray'])

# Save label encoders for prediction phase
os.makedirs("models", exist_ok=True)
joblib.dump(label_encoders, "models/label_encoders.pkl")
joblib.dump(target_encoder, "models/target_encoder.pkl")

# Features & target
X = df.drop('Target_Spray', axis=1)
y = df['Target_Spray']

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Predict on test set
y_pred = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"\n🔍 Test Accuracy: {accuracy * 100:.2f}%")

# Convert class labels to string to avoid error
target_names = [str(cls) for cls in target_encoder.classes_]
labels = list(range(len(target_names)))

# Classification report
print("\n📊 Classification Report:")
print(classification_report(y_test, y_pred, labels=labels, target_names=target_names, zero_division=0))

# Confusion Matrix
print("\n📉 Confusion Matrix:")
print(confusion_matrix(y_test, y_pred, labels=labels))



# Save model
joblib.dump(model, "models/spray_model.pkl")
print("✅ Model and encoders saved in 'models/' folder.")

print("✅ Features used in model:", list(X.columns))
