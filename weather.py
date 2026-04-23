import requests
import pandas as pd
from datetime import datetime
import os

API_KEY = os.getenv("API_KEY")

cities = ["Kochi", "Bangalore", "Mumbai"]
file_name = "weather_data.csv"

data = []

for city in cities:
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url).json()

        if 'main' in response:
            temp = response['main'].get('temp')
            humidity = response['main'].get('humidity')
        else:
            temp, humidity = None, None

        data.append([
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            city,
            temp,
            humidity
        ])

    except Exception as e:
        print(f"Error: {e}")

df = pd.DataFrame(data, columns=["Date", "City", "Temp", "Humidity"])

# Save data
if os.path.exists(file_name):
    df.to_csv(file_name, mode='a', header=False, index=False)
else:
    df.to_csv(file_name, index=False)

print("Data saved successfully!")
print(df)