import pickle
import numpy as np
import streamlit as st

with open('final_gb_regressor.pkl', 'rb') as file:
    model = pickle.load(file)

# Title of the app
st.title("Health Insurance Cost Estimation")

# Input fields with no default values
age = st.number_input("Enter age:", min_value=18, max_value=120, value=None)
sex = st.selectbox("Select sex:", options=["Select", "Male", "Female"])
weight = st.number_input("Enter weight (kg):", min_value=30.0, value=None)
height_cm = st.number_input("Enter height (cm):", min_value=50.0, value=None)
children = st.number_input("Enter number of children:", min_value=0, value=None)
smoker = st.selectbox("Are you a smoker?", options=["Select", "Yes", "No"])
region = st.selectbox("Select region:", options=["Select", "Southeast", "Southwest", "Northeast", "Northwest"])

# Button to predict
if st.button("Estimate"):
    # Check if all fields are filled
    if age is None or sex == "Select" or weight is None or height_cm is None or children is None or smoker == "Select" or region == "Select":
        st.error("Please fill all fields before predicting.")
    else:
        # Convert height from cm to meters
        height_m = height_cm / 100

        # Calculate BMI
        bmi = weight / (height_m ** 2)

        # Prepare input data for prediction
        input_data = (age, 0 if sex == "Male" else 1, bmi, children, 0 if smoker == "Yes" else 1, 
                      {"Southeast": 0, "Southwest": 1, "Northeast": 2, "Northwest": 3}[region])
        input_data_as_numpy_array = np.asarray(input_data)
        input_data_reshaped = input_data_as_numpy_array.reshape(1, -1)

        # Make prediction
        cost_prediction = model.predict(input_data_reshaped)
        st.success(f"The predicted insurance cost is {np.round(cost_prediction[0], 2)} USD")
