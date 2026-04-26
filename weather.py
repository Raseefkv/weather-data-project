import requests
import pandas as pd
from datetime import datetime
import pytz
import os

# API key
API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise ValueError("API_KEY not found. Check GitHub Secrets.")

# Cities
cities = ["Kochi", "Bangalore", "Mumbai"]

# File name
file_name = "weather_data.csv"

# Timezones
utc = pytz.utc
ist = pytz.timezone('Asia/Kolkata')

# Function to classify time of day
def get_time_of_day(hour):
    if 5 <= hour < 12:
        return "Morning"
    elif 12 <= hour < 18:
        return "Afternoon"
    else:
        return "Night"

data = []

# Current IST time
current_time_ist = datetime.utcnow().replace(tzinfo=utc).astimezone(ist)
current_hour = current_time_ist.hour
time_of_day = get_time_of_day(current_hour)

for city in cities:
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url, timeout=10).json()

        if 'main' not in response:
            print(f"API error for {city}: {response}")
            continue

        temp = round(response['main']['temp'], 2)
        humidity = response['main']['humidity']

        data.append([
            current_time_ist.strftime("%Y-%m-%d %H:%M"),
            time_of_day,   # 👈 moved here
            city,
            temp,
            humidity
        ])

    except Exception as e:
        print(f"Error for {city}: {e}")

# Prevent empty save
if not data:
    print("No data to save")
    exit()

# DataFrame with new column order
df = pd.DataFrame(data, columns=["DateTime", "TimeOfDay", "City", "Temp", "Humidity"])

# Save
if os.path.exists(file_name):
    df.to_csv(file_name, mode='a', header=False, index=False)
else:
    df.to_csv(file_name, index=False)

print(f"Data saved at {current_time_ist.strftime('%Y-%m-%d %H:%M IST')}")
