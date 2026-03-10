import streamlit as st
import requests

# -----------------------------

# PAGE CONFIG

# -----------------------------

st.set_page_config(page_title="Secure BMI Calculator", page_icon="⚕️", layout="centered")

st.title("🔐 Secure BMI Health Analyzer")

st.write("Enter your height and weight to calculate BMI and get health insights.")

# -----------------------------

# USER INPUT

# -----------------------------

weight = st.number_input("Enter Weight (kg)", min_value=1.0, step=0.1)
height = st.number_input("Enter Height (cm)", min_value=50.0, step=0.1)

# Replace this with your Render FastAPI URL

API_URL = "https://YOUR_RENDER_API_URL/bmi"

# -----------------------------

# CALCULATE BMI BUTTON

# -----------------------------

if st.button("Calculate BMI"):

```
payload = {
    "weight": weight,
    "height": height
}

try:
    response = requests.post(API_URL, json=payload)

    if response.status_code == 200:

        result = response.json()

        st.success(f"Your BMI: {result['bmi']}")

        st.subheader("📊 BMI Status")
        st.info(result["status"])

        st.subheader("💡 Advice")
        st.write(result["advice"])

        # Recommended Foods
        if "recommended_foods" in result:
            st.subheader("🥗 Recommended Foods")
            for food in result["recommended_foods"]:
                st.write(f"• {food}")

        # Possible Health Risks
        if "possible_health_risks" in result:
            st.subheader("⚠️ Possible Health Risks")
            for risk in result["possible_health_risks"]:
                st.write(f"• {risk}")

        # Cholesterol Risk
        if "cholesterol_risk" in result:
            st.subheader("🫀 Cholesterol Risk")
            st.write(result["cholesterol_risk"])

    else:
        st.error("❌ Backend returned an error.")

except requests.exceptions.ConnectionError:
    st.error("⚠️ Cannot connect to BMI API. Please check if the backend is running.")
```
