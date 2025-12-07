import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# 👇 Read your local dataset
# Make sure diabetes.csv is in the same folder as this file
data = pd.read_csv("diabetes.csv")

# Check first few rows (optional, for debugging)
print("✅ Dataset Loaded Successfully!")
print(data.head())

# Make sure your dataset has the correct columns
# If it doesn’t have headers, use:
# columns = ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness",
#            "Insulin", "BMI", "DiabetesPedigreeFunction", "Age", "Outcome"]
# data = pd.read_csv("diabetes.csv", names=columns, header=None)

# Split into input (X) and output (y)
X = data.drop("Outcome", axis=1)
y = data["Outcome"]

# Split into train & test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train a Random Forest model
model = RandomForestClassifier(random_state=42)
model.fit(X_train_scaled, y_train)

# Evaluate accuracy
y_pred = model.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)
print(f"🎯 Model Accuracy: {accuracy * 100:.2f}%")

# Save model & scaler
joblib.dump(model, "diabetes_model.pkl")
joblib.dump(scaler, "scaler.pkl")

print("💾 Model and scaler saved successfully!")
