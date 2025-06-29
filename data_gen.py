# data_gen.py

import pandas as pd
import random
import os

# Create data directory if it doesn't exist
os.makedirs("data", exist_ok=True)

# Valid options
crops = ['Rice', 'Wheat', 'Cotton', 'Maize', 'Tomato', 'Potato']
growth_stages = ['Seedling', 'Vegetative', 'Flowering', 'Mature']
last_spray_options = ['Fertilizer', 'Fungicide', 'Pesticide', 'No Spray']  # Safe string
target_sprays = ['Fertilizer', 'Fungicide', 'Pesticide', 'No Spray']

# Data generation logic
def generate_sample():
    crop = random.choice(crops)
    stage = random.choice(growth_stages)
    temp = round(random.uniform(20, 40), 1)
    humidity = random.randint(30, 100)
    rainfall = round(random.uniform(0, 50), 1)
    wind = round(random.uniform(0.5, 15), 1)
    pest = random.randint(0, 1)
    last_spray = random.choice(last_spray_options)

    # Rule-based spray recommendation
    if pest == 1 and humidity > 70 and crop in ['Rice', 'Tomato']:
        spray = 'Fungicide'
    elif pest == 1 and humidity <= 70:
        spray = 'Pesticide'
    elif stage == 'Mature' and rainfall < 10:
        spray = 'Fertilizer'
    else:
        spray = 'No Spray'

    return [
        str(crop),
        str(stage),
        temp,
        humidity,
        rainfall,
        wind,
        pest,
        str(last_spray),
        str(spray)
    ]

# Generate 1200 samples
data = [generate_sample() for _ in range(1200)]

# Define column names
columns = [
    'Crop',
    'Growth_Stage',
    'Temperature',
    'Humidity',
    'Rainfall_2d',
    'Wind_Speed',
    'Pest_Infestation',
    'Last_Spray',
    'Target_Spray'
]

# Create DataFrame
df = pd.DataFrame(data, columns=columns)

# Ensure proper data types
df = df.astype({
    'Crop': str,
    'Growth_Stage': str,
    'Last_Spray': str,
    'Target_Spray': str
})

# Save to CSV
df.to_csv("data/spray_dataset_expanded.csv", index=False)
print("✅ Dataset generated at data/spray_dataset_expanded.csv")
