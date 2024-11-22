import streamlit as st
import numpy as np
import joblib
from tensorflow.keras.models import load_model

# Load the scaler and model
scaler = joblib.load('sc_house.h5')  # Ensure the path is correct
model = load_model('house_prediction.h5')  # Ensure the path is correct

# Title and Description
st.title("🏠 House Price Prediction App for USA")
st.write("""
Welcome to the House Price Prediction App! Adjust the sliders to set the house details, and the AI model will predict its estimated price.
""")

# Sidebar Instructions
with st.sidebar:
    # App Description
    st.header("Customize Slider Ranges")
    income_range = st.slider(
        "Average Area Income Range ($)",
        min_value=50000, max_value=200000, value=(50000, 150000), step=5000
    )
    population_range = st.slider(
        "Area Population Range",
        min_value=1000, max_value=200000, value=(10000, 50000), step=1000
    )
    st.title("About the App")
    st.subheader("📌 What is this App?")
    st.write("""
    This is a **House Price Prediction App** that uses AI and Machine Learning to estimate the price of a house based on user inputs.
    """)

    st.subheader("⚙️ How does this App work?")
    st.write("""
    1. Adjust the sliders to set the features of the house.
    2. Click **Predict Price** to get the estimated house price.
    3. The app uses a trained Neural Network model to make predictions based on your inputs.
    """)

    st.subheader("🔍 Overview")
    st.write("""
    - **Input Features:** Average income, house age, number of rooms, bedrooms, and population in the area.
    - **Output:** The predicted price of the house in dollars.
    - **Technology:** Built with Streamlit and powered by a TensorFlow deep learning model.
    """)

    # Allow users to define slider ranges

# Input Fields using Sliders
st.header("📋 Set House Details")

col1, col2 = st.columns(2)

with col1:
    avg_area_income = st.slider(
        "Average Area Income ($)",
        min_value=income_range[0],
        max_value=income_range[1],
        value=70000,
        step=1000
    )
    avg_area_house_age = st.slider(
        "Average Area House Age (years)",
        min_value=0,
        max_value=100,
        value=5,
        step=1
    )

with col2:
    avg_area_number_of_rooms = st.slider(
        "Average Number of Rooms",
        min_value=1,
        max_value=20,
        value=7,
        step=1
    )
    avg_area_number_of_bedrooms = st.slider(
        "Average Number of Bedrooms",
        min_value=1,
        max_value=10,
        value=4,
        step=1
    )

area_population = st.slider(
    "Area Population",
    min_value=population_range[0],
    max_value=population_range[1],
    value=30000,
    step=100
)

# Collect user input into an array
user_input = np.array([[avg_area_income, avg_area_house_age, avg_area_number_of_rooms,
                        avg_area_number_of_bedrooms, area_population]])

# Predict Button
if st.button("🔮 Predict Price", key="predict_button"):
    try:
        # Progress bar and spinner
        with st.spinner("Analyzing the data..."):
            st.progress(0)  # Initialize progress bar
            scaled_input = scaler.transform(user_input)  # Scale the inputs
            prediction = model.predict(scaled_input)  # Predict price
            st.progress(100)  # Progress completes

        # Display prediction result
        predicted_price = prediction[0][0]
        st.success(f"💰 The predicted house price is **${predicted_price:,.2f}**!")

        # Add celebratory animation
        st.balloons()

    except Exception as e:
        st.error(f"An error occurred while making predictions: {e}")
