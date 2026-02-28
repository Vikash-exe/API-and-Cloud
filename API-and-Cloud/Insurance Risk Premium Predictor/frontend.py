import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/predict"

st.title("Health Premier Risk Prediction App DEMO")
st.markdown("Enter your details to predict your health risk category.")

# Collect user input
age = st.number_input("Age", min_value=1, max_value=120, value=30)
weight = st.number_input("Weight (kg)", min_value=1.0, max_value=300.0, value=70.0)
height = st.number_input("Height (m)", min_value=1.0, max_value=2.5, value=1.70)
income_lpa = st.number_input("Income Level (LPA)", min_value=0.0, max_value=100.0, value=50.0)
smoker = st.selectbox("Smoker", options=[True, False])
city = st.selectbox("City", options=['Delhi','Mumbai','Bangalore','Hyderabad','Kolkata','Jaipur', 'Chennai', 'Indore', 'Kota','Chandigarh', 'Pune',  'Lucknow', 'Gaya',
'Jalandhar', 'Mysore'])
occupation = st.selectbox("Occupation", options=['retired', 'freelancer', 'student', 'government_job',
       'business_owner', 'unemployed', 'private_job'])

if st.button("Predict Risk Category"):
    user_data = {
        "age": age,
        "weight": weight,
        "height": height,
        "income_lpa": income_lpa,
        "smoker": smoker,
        "city": city,
        "occupation": occupation
    }
    
    try:
        response = requests.post(API_URL, json=user_data)
        if response.status_code == 200:
            result = response.json()
            st.success(f"Your predicted health risk category is: {result['risk_category']}")
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while connecting to the API: {e}")