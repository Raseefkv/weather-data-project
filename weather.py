import requests
import pandas as pd
from datetime import datetime
import pytz
import os

API_KEY = os.getenv("API_KEY")

cities = ["Kochi", "Bangalore", "Mumbai"]
file_name = "weather_data.csv"

# IST timezone
ist = pytz.timezone('Asia/Kolkata')

data = []

for city in cities:
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url).json()

        temp = response['main'].get('temp')
        humidity = response['main'].get('humidity')

        data.append([
            datetime.now(ist).strftime("%Y-%m-%d %H:%M"),  # ✅ IST time
            city,
            temp,
            humidity
        ])

    except Exception as e:
        print(f"Error: {e}")

df = pd.DataFrame(data, columns=["DateTime", "City", "Temp", "Humidity"])

# Save
if os.path.exists(file_name):
    df.to_csv(file_name, mode='a', header=False, index=False)
else:
    df.to_csv(file_name, index=False)

print("Data saved!")
