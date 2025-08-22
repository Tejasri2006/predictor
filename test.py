import streamlit as st
import pandas as pd
import joblib

# Load the trained model
model = joblib.load("rf_insurance_model.joblib")

st.title("Medical Care Expense")

# Input fields
age = st.number_input("Age", min_value=18, max_value=100, step=1)
sex = st.selectbox("Sex", ["male", "female"])
bmi = st.number_input("BMI", min_value=10.0, max_value=50.0, step=0.1)
children = st.number_input("Number of Children", min_value=0, max_value=10, step=1)
smoker = st.selectbox("Smoker", ["yes", "no"])
region = st.selectbox("Region", ["southeast", "southwest", "northeast", "northwest"])

# Create dataframe with correct column names (match training data)
input_df = pd.DataFrame([{
    "age": age,
    "sex": sex,
    "bmi": bmi,
    "children": children,
    "smoker": smoker,
    "region": region
}])

if st.button("Predict"):
    prediction = model.predict(input_df)
    st.success(f"Predicted Annual Insurance Cost: ₹{prediction[0]:,.2f}")
