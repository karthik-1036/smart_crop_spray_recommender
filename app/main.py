from weather_api import get_lat_lon, get_weather_data
from recommender import predict_spray

# 🔍 Step 1: Get location from user
city = "Mysore"
lat, lon = get_lat_lon(city)

# 🌤️ Step 2: Fetch weather
weather = get_weather_data(lat, lon)

# 🤖 Step 3: Predict
result = predict_spray(
    crop="Wheat",
    stage="Mature",
    temperature=weather["temperature"],
    humidity=weather["humidity"],
    rainfall=weather["rainfall"],
    wind_speed=weather["wind_speed"],
    pest_infestation=1,
    last_spray="No Spray"
)

print(f"\n📍 Location: {city}")
print(f"🌤️ Weather: {weather}")
print(f"🔮 Recommended Spray: {result}")
