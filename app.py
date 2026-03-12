import streamlit as st
import requests

st.title("🔐 Secure BMI Calculator")

# User Inputs
weight = st.number_input("Enter weight (kg)", min_value=1.0)
height = st.number_input("Enter height (cm)", min_value=1.0)

# Button
if st.button("Calculate BMI"):

    payload = {
        "weight": weight,
        "height": height
    }

    try:
        response = requests.post(
            "http://127.0.0.1:8000/bmi",
            json=payload
        )

        if response.status_code == 200:
            result = response.json()

            st.success(f"Your BMI is: {result['bmi']}")
            st.write("Status:", result["status"])
            st.write("Advice:", result["advice"])

            st.subheader("Recommended Foods")
            for food in result["recommended_foods"]:
                st.write("•", food)

        else:
            st.error("Backend error")

    except requests.exceptions.ConnectionError:
        st.error("⚠️ Backend not running. Please start FastAPI server.")
