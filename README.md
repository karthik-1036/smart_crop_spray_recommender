# 🌾 Smart Crop Spray Recommender

An AI-powered web app that recommends the right type of spray (Pesticide, Fungicide, Fertilizer, or No Spray) based on real-time weather, crop stage, and pest infestation levels. Built with Streamlit, Scikit-Learn, and OpenWeatherMap API.

---

## 🚀 Live Demo

> [Streamlit Cloud](https://ai-crop-spray-recommender.streamlit.app/)

---

## 📌 Features

✅ Real-time weather integration using OpenWeatherMap  
✅ Predicts best spray using a trained machine learning model  
✅ Dashboard with spray analytics and visualizations  
✅ Logs user inputs and predictions to CSV for future training  
✅ Clean, modern UI with Streamlit + Plotly  

---

## 🧠 How It Works

1. **User inputs**:
   - Location (e.g., Mysore)
   - Crop type (Wheat, Rice, Tomato, etc.)
   - Growth stage (Seedling, Vegetative, Flowering, Mature)
   - Pest infestation level
   - Last spray used

2. **Weather data** is fetched for that location via OpenWeatherMap

3. **Pre-trained Random Forest model** predicts the ideal spray type

4. **Prediction is displayed + logged** to `logs/predictions.csv`

5. A **dashboard** provides insights on past predictions

---

## 🖥️ Tech Stack

- Python
- Streamlit
- Scikit-Learn
- Pandas
- Plotly
- Joblib
- OpenWeatherMap API
