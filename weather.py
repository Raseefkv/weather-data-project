import requests
import pandas as pd
from datetime import datetime
import pytz
import os

API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise ValueError("API_KEY not found.")

cities = ["Kochi", "Bangalore", "Mumbai"]
file_name = "weather_data.csv"

utc = pytz.utc
ist = pytz.timezone('Asia/Kolkata')

def get_time_slot(hour):
    if 7 <= hour <= 8:
        return "Morning"
    elif 13 <= hour <= 14:
        return "Afternoon"
    elif 21 <= hour <= 22:
        return "Night"
    else:
        return None  

current_time = datetime.utcnow().replace(tzinfo=utc).astimezone(ist)
current_hour = current_time.hour

time_slot = get_time_slot(current_hour)

if time_slot is None:
    print("Outside allowed time window. Skipping run.")
    exit()

if os.path.exists(file_name):
    existing_df = pd.read_csv(file_name)
    
    today_str = current_time.strftime("%Y-%m-%d")
    
    if not existing_df.empty:
        existing_df["Date"] = pd.to_datetime(existing_df["DateTime"]).dt.date
        
        today_data = existing_df[existing_df["Date"] == pd.to_datetime(today_str).date()]
        
        if time_slot in today_data["TimeOfDay"].values:
            print(f"{time_slot} data already exists for today. Skipping.")
            exit()

data = []

for city in cities:
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url, timeout=10).json()

        if 'main' not in response:
            print(f"API error for {city}")
            continue

        temp = round(response['main']['temp'], 2)
        humidity = response['main']['humidity']

        data.append([
            current_time.strftime("%Y-%m-%d %H:%M"),
            time_slot,
            city,
            temp,
            humidity
        ])

    except Exception as e:
        print(f"Error: {e}")

if not data:
    print("No data collected.")
    exit()

df = pd.DataFrame(data, columns=["DateTime", "TimeOfDay", "City", "Temp", "Humidity"])

if os.path.exists(file_name):
    df.to_csv(file_name, mode='a', header=False, index=False)
else:
    df.to_csv(file_name, index=False)

print(f"{time_slot} data saved at {current_time.strftime('%Y-%m-%d %H:%M IST')}")
