import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(
    page_title="Weather Monitoring Dashboard",
    layout="wide"
)

# Dashboard title
st.title("🌦 Weather Monitoring Dashboard")

# Load data
@st.cache_data(ttl=60)
def load_data():
    df = pd.read_csv("weather_data.csv")
    df["DateTime"] = pd.to_datetime(df["DateTime"])
    
    # Create separate Date column
    df["Date"] = df["DateTime"].dt.date
    
    return df

# Read CSV
try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Latest timestamp
latest_time = df["DateTime"].max()

# Latest records
latest_df = df[df["DateTime"] == latest_time]

# Current slot
current_slot = latest_df.iloc[0]["TimeOfDay"]

# Header info
st.markdown(
    f"""
    ### 🕒 Updated At: {latest_time.strftime('%Y-%m-%d %H:%M IST')}
    ### 🌅 Current Slot: {current_slot}
    """
)

st.divider()

# KPI Section
st.subheader("📊 Current Weather KPIs")

col1, col2, col3 = st.columns(3)

cities = ["Kochi", "Bangalore", "Mumbai"]
columns = [col1, col2, col3]

for city, col in zip(cities, columns):

    city_data = latest_df[latest_df["City"] == city]

    if not city_data.empty:

        temp = city_data.iloc[0]["Temp"]
        humidity = city_data.iloc[0]["Humidity"]

        with col:

            st.metric(
                label=f"🌡 {city} Temperature",
                value=f"{temp} °C"
            )

            st.metric(
                label=f"💧 {city} Humidity",
                value=f"{humidity}%"
            )

st.divider()

# Current Day Data
current_date = latest_time.date()

today_df = df[df["Date"] == current_date]

# Time order
time_order = ["Morning", "Afternoon", "Night"]

# Temperature variation during current day
st.subheader("🌡 Current Day Temperature Variation")

fig_day_temp = px.line(
    today_df,
    x="TimeOfDay",
    y="Temp",
    color="City",
    markers=True,
    category_orders={"TimeOfDay": time_order},
    title="Temperature Variation During Current Day"
)

st.plotly_chart(fig_day_temp, use_container_width=True)

# Humidity variation during current day
st.subheader("💧 Current Day Humidity Variation")

fig_day_humidity = px.line(
    today_df,
    x="TimeOfDay",
    y="Humidity",
    color="City",
    markers=True,
    category_orders={"TimeOfDay": time_order},
    title="Humidity Variation During Current Day"
)

st.plotly_chart(fig_day_humidity, use_container_width=True)

# Filters
st.subheader("🎛 Trend Filters")

filter_col1, filter_col2 = st.columns(2)

with filter_col1:
    selected_slot = st.selectbox(
        "Select Time Of Day",
        ["All", "Morning", "Afternoon", "Night"]
    )

with filter_col2:
    selected_days = st.selectbox(
        "Select Time Range (Days)",
        [7, 14, 30]
    )

# Latest date
latest_date = df["DateTime"].max()

# Filter by days
filtered_df = df[
    df["DateTime"] >= latest_date - pd.Timedelta(days=selected_days)
]

# Filter by time slot
if selected_slot != "All":
    filtered_df = filtered_df[
        filtered_df["TimeOfDay"] == selected_slot
    ]

st.divider()

# Temperature Trend
st.subheader(f"📈 Temperature Trends - Last {selected_days} Days")

fig_temp = px.line(
    filtered_df,
    x="Date",
    y="Temp",
    color="City",
    markers=True,
    title="Temperature Trend by City"
)

st.plotly_chart(fig_temp, use_container_width=True)

# Humidity Trend
st.subheader(f"💧 Humidity Trends - Last {selected_days} Days")

fig_humidity = px.line(
    filtered_df,
    x="Date",
    y="Humidity",
    color="City",
    markers=True,
    title="Humidity Trend by City"
)

st.plotly_chart(fig_humidity, use_container_width=True)

# Average temperature by time slot
st.subheader("🌅 Average Temperature by Time of Day")

avg_temp = (
    filtered_df.groupby(["TimeOfDay", "City"])["Temp"]
    .mean()
    .reset_index()
)

fig_avg = px.bar(
    avg_temp,
    x="TimeOfDay",
    y="Temp",
    color="City",
    barmode="group",
    title="Average Temperature by Time Slot"
)

st.plotly_chart(fig_avg, use_container_width=True)

# Raw Data
st.subheader("📄 Raw Weather Data")

st.dataframe(
    filtered_df.sort_values(by="DateTime", ascending=False),
    use_container_width=True
)
