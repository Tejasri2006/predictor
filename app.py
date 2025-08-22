import streamlit as st
import json
import os
import pandas as pd
import joblib

# Load your ML model from test.py logic
import test  # You can also just import the predict function from test.py

# ----------------- Constants -----------------
CREDENTIALS_FILE = "users.json"

# ----------------- Helper Functions -----------------
def load_users():
    """Load users safely."""
    if os.path.exists(CREDENTIALS_FILE):
        try:
            with open(CREDENTIALS_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}

def save_users(users):
    """Save users to local JSON file."""
    with open(CREDENTIALS_FILE, "w") as f:
        json.dump(users, f, indent=4)

# ----------------- Streamlit UI -----------------
st.set_page_config(page_title="Medical Care Expense", layout="centered")
st.title("🔒 Login & Signup for Medical Care Expense")

# --- Session State ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# ----------------- LOGIN / SIGNUP -----------------
if not st.session_state.logged_in:
    tab1, tab2 = st.tabs(["Login", "Signup"])

    with tab1:
        st.subheader("Login")
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            users = load_users()
            if username in users and users[username] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"✅ Welcome back, {username}!")
            else:
                st.error("❌ Invalid username or password")

    with tab2:
        st.subheader("Signup")
        new_user = st.text_input("New Username", key="signup_user")
        new_pass = st.text_input("New Password", type="password", key="signup_pass")
        if st.button("Signup"):
            users = load_users()
            if new_user in users:
                st.error("❌ Username already exists.")
            else:
                users[new_user] = new_pass
                save_users(users)
                st.success("✅ Account created successfully! Please login now.")

# ----------------- PREDICTION PAGE -----------------
if st.session_state.logged_in:
    st.subheader("💰 Insurance Price Prediction")
    st.write(f"Welcome, **{st.session_state.username}**! Enter the details below:")

    # Input fields matching your model
    age = st.number_input("Age", min_value=18, max_value=100, step=1)
    sex = st.selectbox("Sex", ["male", "female"])
    bmi = st.number_input("BMI", min_value=10.0, max_value=50.0, step=0.1)
    children = st.number_input("Number of Children", min_value=0, max_value=10, step=1)
    smoker = st.selectbox("Smoker", ["yes", "no"])
    region = st.selectbox("Region", ["southeast", "southwest", "northeast", "northwest"])

    if st.button("Predict"):
        input_df = pd.DataFrame([{
            "age": age,
            "sex": sex,
            "bmi": bmi,
            "children": children,
            "smoker": smoker,
            "region": region
        }])
        # Use your test.py model predict function
        prediction = test.model.predict(input_df)
        st.success(f"💵 Predicted Annual Insurance Cost: ₹{prediction[0]:,.2f}")

    # Logout
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.success("✅ Logged out successfully!")
