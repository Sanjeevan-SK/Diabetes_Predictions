import streamlit as st
import joblib
import numpy as np
import sqlite3
import warnings

warnings.filterwarnings("ignore")


# Load model and scaler
model = joblib.load("diabetes_model.pkl")
scaler = joblib.load("scaler.pkl")


# Create or connect to database
conn = sqlite3.connect("user_data.db")
cursor = conn.cursor()


# Create table if not exists
cursor.execute('''CREATE TABLE IF NOT EXISTS health_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT,
    age INTEGER,
    bmi REAL,
    glucose REAL,
    blood_pressure REAL,
    insulin REAL,
    pregnancies INTEGER,
    skin_thickness REAL,
    dpf REAL,
    risk_level TEXT,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)''')
conn.commit()


# Streamlit app UI
st.set_page_config(page_title="🩺 Diabetes Risk Predictor", page_icon="💉", layout="centered")
st.title("🩺 Diabetes Risk Prediction App")
st.write("Enter your details below to predict your diabetes risk and store your results securely.")


# Input fields
user_name = st.text_input("Enter your name")
col1, col2 = st.columns(2)


with col1:
    Pregnancies = st.number_input("Pregnancies", 0, 20, 1)
    Glucose = st.number_input("Glucose Level", 0, 300, 120)
    BloodPressure = st.number_input("Blood Pressure", 0, 200, 70)
    SkinThickness = st.number_input("Skin Thickness", 0, 100, 20)

with col2:
    Insulin = st.number_input("Insulin Level", 0, 900, 80)
    BMI = st.number_input("BMI", 0.0, 70.0, 25.0)
    DPF = st.number_input("Diabetes Pedigree Function", 0.0, 3.0, 0.5)
    Age = st.number_input("Age", 1, 120, 30)

if st.button("🔍 Predict Diabetes Risk"):
    # Prepare input
    input_data = np.array([[Pregnancies, Glucose, BloodPressure, SkinThickness,
                            Insulin, BMI, DPF, Age]])
    input_scaled = scaler.transform(input_data)
    prediction = model.predict(input_scaled)[0]

    # Show result
    if prediction == 1:
        risk = "High Risk"
        st.error("🚨 High risk of diabetes. Please consult a doctor.")
    else:
        risk = "Low Risk"
        st.success("✅ Low risk of diabetes. Maintain a healthy lifestyle!")

    # Save to database
    if user_name.strip() != "":
        cursor.execute('''INSERT INTO health_records 
            (user_name, age, bmi, glucose, blood_pressure, insulin, pregnancies, skin_thickness, dpf, risk_level)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (user_name, Age, BMI, Glucose, BloodPressure, Insulin,
             Pregnancies, SkinThickness, DPF, risk)
        )
        conn.commit()
        st.info("💾 Your result has been saved securely!")
    else:
        st.warning("⚠️ Please enter your name before saving.")

# # Show all records button
# if st.button("📋 Show All Records"):
#     df = st.dataframe(
#         st.session_state.get(
#             "data",
#             cursor.execute("SELECT * FROM health_records ORDER BY date DESC").fetchall()
#         )
#     )

st.markdown("---")
st.markdown("Developed with ❤️ by **Sanjeevan** using Streamlit + Machine Learning")
