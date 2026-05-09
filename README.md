# 🌦 Weather Monitoring Dashboard

This project is an automated weather analytics dashboard built using Python, Streamlit, GitHub Actions, and the OpenWeather API.

The system automatically collects live weather data for multiple cities, stores the data in CSV format, and updates a dynamic dashboard with visualizations and trend analysis.

---

# 🚀 Live Dashboard

🔗 https://weather-data-project.streamlit.app/

---

# 📌 About the Project

The main idea behind this project was to build a small end-to-end data analytics pipeline instead of performing analysis only on static downloaded datasets.

This project was developed primarily for educational and portfolio purposes to gain practical experience in:
- API integration
- Data collection automation
- Time-series data analysis
- Dashboard development
- Cloud-based workflow automation

The project automatically:
- collects weather data from an API
- stores the data continuously
- updates visualizations dynamically
- performs trend analysis over time

The dashboard tracks:
- Temperature
- Humidity
- Daily variation
- Historical trends

for:
- Kochi
- Bangalore
- Mumbai

The cities Kochi, Bangalore, and Mumbai were selected to compare weather patterns across different urban regions in India with varying climate characteristics. This enables more meaningful trend analysis and city-wise comparisons within the dashboard.

---

# ⚙️ How the Project Works

## 1. Weather Data Collection

A Python script (`weather.py`) fetches live weather data from the OpenWeather API.

The collected fields include:
- Date and time
- Time slot (Morning / Afternoon / Night)
- City
- Temperature
- Humidity

---

## 2. Automation using GitHub Actions

GitHub Actions runs the collection script automatically every 30 minutes.

The script only stores data during specific time windows:
- Morning
- Afternoon
- Night

This helps maintain cleaner and more structured data collection.

Duplicate entries for the same time slot are also prevented.

GitHub Actions scheduling can occasionally experience execution delays.  
To improve reliability and ensure data collection within the required time windows, the workflow runs every 30 minutes while the Python script validates and stores only valid time-slot data.

---

## 3. Dynamic Dashboard

The dashboard is built using Streamlit.

Whenever new data is added to the CSV file, the dashboard automatically reflects the updated values and trends.

The dashboard includes:
- Current weather KPIs
- Current day weather variation
- Temperature trends
- Humidity trends
- Historical filtering options

---

# 📊 Dashboard Features

## 🔹 Current Weather KPIs
Displays the latest:
- Temperature
- Humidity

for all three cities.

---

## 🔹 Current Day Weather Variation
Shows how temperature and humidity change throughout the day using:
- Morning
- Afternoon
- Night

readings.

---

## 🔹 Historical Trend Analysis
Users can filter trends based on:
- Morning
- Afternoon
- Night

and analyze:
- Last 7 days
- Last 14 days
- Last 30 days

---

# 🛠 Technologies Used

- Python
- Pandas
- Streamlit
- Plotly
- GitHub Actions
- OpenWeather API

---

# 📂 Project Structure

```text
weather-data-project/
│
├── .github/
│   └── workflows/
│       └── weather.yml
│
├── app.py
├── weather.py
├── weather_data.csv
├── requirements.txt
└── README.md
```

---

# ▶️ Running the Project Locally

## Install dependencies

```bash
pip install -r requirements.txt
```

---

## Run the dashboard

```bash
streamlit run app.py
```

---

# 🔑 API Key Setup

Create an API key from:

https://openweathermap.org/api

Add your API key as:

```text
API_KEY=your_api_key
```

---

# 📈 Future Improvements

Possible future improvements:
- Machine learning based weather prediction
- Smoothed weather trend analysis
- Downloadable reports
- Database integration
- Alert system for extreme weather
- Optimizing workflow scheduling to reduce unnecessary polling
- Migrating automation to cloud services such as AWS Lambda or Cloud Scheduler for more precise execution timing

---

# 👨‍💻 Author

Raseef Kv
