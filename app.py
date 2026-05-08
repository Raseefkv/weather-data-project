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

# Load CSV
@st.cache_data(ttl=60)
def load_data():
    df = pd.read_csv("weather_data.csv")
    df["DateTime"] = pd.to_datetime(df["DateTime"])
    return df

# Read data
try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Latest timestamp
latest_time = df["DateTime"].max()

# Latest snapshot
latest_df = df[df["DateTime"] == latest_time]

# Current slot
current_slot = latest_df.iloc[0]["TimeOfDay"]

# Top section
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

# Temperature Trend
st.subheader("📈 Temperature Trends")

fig_temp = px.line(
    df,
    x="DateTime",
    y="Temp",
    color="City",
    markers=True,
    title="Temperature Trend by City"
)

st.plotly_chart(fig_temp, use_container_width=True)

# Humidity Trend
st.subheader("💧 Humidity Trends")

fig_humidity = px.line(
    df,
    x="DateTime",
    y="Humidity",
    color="City",
    markers=True,
    title="Humidity Trend by City"
)

st.plotly_chart(fig_humidity, use_container_width=True)

# Average Temperature by Time Slot
st.subheader("🌅 Average Temperature by Time of Day")

avg_temp = (
    df.groupby(["TimeOfDay", "City"])["Temp"]
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
    df.sort_values(by="DateTime", ascending=False),
    use_container_width=True
)
