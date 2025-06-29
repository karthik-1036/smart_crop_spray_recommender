import streamlit as st
import pandas as pd
import plotly.express as px
from weather_api import get_lat_lon, get_weather_data
from recommender import predict_spray, log_prediction

st.set_page_config(page_title="🌾 Smart Crop Spray Recommender", layout="wide")

st.title("🌾 Smart Crop Spray Recommender")

with st.form("spray_form"):
    st.subheader("📍 Location & Crop Info")
    col1, col2 = st.columns(2)
    with col1:
        location = st.text_input("📌 Enter Your Location", "Mysore")
        crop = st.selectbox("🌱 Crop Type", ["Wheat", "Rice", "Maize", "Cotton","Tomato", "Potato"])
        growth_stage = st.selectbox("📈 Growth Stage", ["Seedling", "Vegetative", "Flowering","Mature"])
    with col2:
        pest_level = st.slider("🐛 Pest Infestation Level (0–100)", 0, 100, 10)
        last_spray = st.selectbox("💧 Last Spray Used", ["No Spray", "Fertilizer", "Pesticide", "Fungicide"])

    submitted = st.form_submit_button("🚀 Predict Optimal Spray")

# --- After Submit ---
if submitted:
    try:
        lat, lon = get_lat_lon(location)
        weather = get_weather_data(lat, lon)

        # Display current weather
        st.subheader("🌦️ Current Weather Data")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("🌡️ Temperature", f"{weather['temperature']} °C")
        col2.metric("💧 Humidity", f"{weather['humidity']} %")
        col3.metric("🌧️ Rainfall (2d)", f"{weather['rainfall_2d']} mm")
        col4.metric("🌬️ Wind Speed", f"{weather['wind_speed']} km/h")

        # Predict
        prediction = predict_spray(
            crop=crop,
            growth_stage=growth_stage,
            temperature=weather["temperature"],
            humidity=weather["humidity"],
            rainfall_2d=weather["rainfall_2d"],
            wind_speed=weather["wind_speed"],
            pest_infestation=pest_level,
            last_spray=last_spray
        )

        st.success(f"🔮 **Recommended Spray:** `{prediction}`")

        # Log data
        log_data = {
            "Location": location,
            "Crop": crop,
            "Growth_Stage": growth_stage,
            "Temperature": weather["temperature"],
            "Humidity": weather["humidity"],
            "Rainfall_2d": weather["rainfall_2d"],
            "Wind_Speed": weather["wind_speed"],
            "Pest_Infestation": pest_level,
            "Last_Spray": last_spray,
            "Predicted_Spray": prediction
        }
        log_prediction(log_data)

        # Show dashboard below
        st.subheader("📊 Spray Analytics Dashboard")
        df = pd.read_csv("logs/predictions.csv")

        tab1, tab2 = st.tabs(["🧪 Spray Insights", "🌡️ Environmental Insights"])

        with tab1:
            st.plotly_chart(px.histogram(df, x="Predicted_Spray", color="Predicted_Spray", title="Spray Type Distribution"))
            st.plotly_chart(px.histogram(df, x="Growth_Stage", color="Predicted_Spray", title="Growth Stage vs Spray"))
            st.plotly_chart(px.histogram(df, x="Last_Spray", color="Predicted_Spray", title="Last Spray vs Prediction"))

        with tab2:
            st.plotly_chart(px.histogram(df, x="Pest_Infestation", color="Predicted_Spray", nbins=20, title="Pest Infestation vs Spray"))
            st.plotly_chart(px.histogram(df, x="Temperature", title="Temperature Distribution"))
            st.plotly_chart(px.histogram(df, x="Humidity", title="Humidity Distribution"))

    except Exception as e:
        st.error(f"⚠️ {e}")
