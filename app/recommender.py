import joblib
import pandas as pd
import os
from datetime import datetime

# Load model and encoders
model = joblib.load(os.path.join("models", "spray_model.pkl"))
label_encoders = joblib.load(os.path.join("models", "label_encoders.pkl"))
target_encoder = joblib.load(os.path.join("models", "target_encoder.pkl"))

# ✅ Exact feature order used during training
FEATURE_ORDER = [
    'Crop',
    'Growth_Stage',
    'Temperature',
    'Humidity',
    'Rainfall_2d',
    'Wind_Speed',
    'Pest_Infestation',
    'Last_Spray'
]

def predict_spray(
    crop,
    growth_stage,
    temperature,
    humidity,
    rainfall_2d,
    wind_speed,
    pest_infestation,
    last_spray
):
    try:
        crop_encoded = label_encoders['Crop'].transform([crop])[0]
        stage_encoded = label_encoders['Growth_Stage'].transform([growth_stage])[0]
        last_spray_encoded = label_encoders['Last_Spray'].transform([last_spray])[0]
    except ValueError as e:
        print(f"❌ Encoding Error: {e}")
        return "Unknown Spray (Invalid Input)"

    input_dict = {
        'Crop': [crop_encoded],
        'Growth_Stage': [stage_encoded],
        'Temperature': [temperature],
        'Humidity': [humidity],
        'Rainfall_2d': [rainfall_2d],
        'Wind_Speed': [wind_speed],
        'Pest_Infestation': [pest_infestation],
        'Last_Spray': [last_spray_encoded]
    }

    input_df = pd.DataFrame(input_dict)
    input_df = input_df[FEATURE_ORDER]  # Force correct order

    prediction = model.predict(input_df)[0]
    spray = target_encoder.inverse_transform([prediction])[0]
    return spray


def log_prediction(data_dict):
    """
    Append user input and prediction to a CSV log.
    """
    log_path = os.path.join("logs", "predictions.csv")
    os.makedirs("logs", exist_ok=True)

    data_dict["Timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df = pd.DataFrame([data_dict])

    if os.path.exists(log_path):
        df.to_csv(log_path, mode='a', header=False, index=False)
    else:
        df.to_csv(log_path, index=False)
