import streamlit as st
import pandas as pd
import numpy as np

@st.cache_data
def load_data():
    weather = pd.read_csv("data/weather.csv")
    weather = weather.rename(columns={"YEAR": "Year", "MO": "Month", "DY": "Day",
                                      "T2M_MAX": "TMax", "T2M_MIN": "TMin"})
    weather = weather.dropna().copy()
    return weather

weather = load_data()

st.sidebar.header("Filters")

### Selecting the years ###
year_min, year_max = int(weather["Year"].min()), int(weather["Year"].max())

yr_range = st.sidebar.slider(
    "Year range",
    min_value=year_min, max_value=year_max,
    value=(year_min, year_max), step=1
)

### Selecting the month ###
month_names = {
    1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June",
    7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"
}

month = st.sidebar.selectbox(
    "Month",
    options=list(month_names.keys()),
    format_func=lambda m: month_names[m],
    index=0  # default: January
)

### Filtering the data
def filter_data(data, yr_range, month):
    mask = (data["Year"].between(yr_range[0], yr_range[1])) & (data["Month"] == month)
    sub = data.loc[mask, ["Day", "TMax", "TMin"]].copy()
    return sub

sub = filter_data(weather, yr_range, month)

st.title("Visualization of meteorological data in Paris over the selected period")
st.caption(f"Years {yr_range[0]}–{yr_range[1]} • {month_names[month]}")

if sub.empty:
    st.warning("No data for the selected period")
    st.stop()

### Averaging by day
daily = (
    sub.groupby("Day", as_index=False)
       .mean(numeric_only=True)
       .sort_values("Day")
)

### Plotting the data
col1, col2 = st.columns([2, 1], gap="large")

with col1:
    st.subheader(f"Average daily temperatures in {month_names[month]} ({yr_range[0]}-{yr_range[1]})")
    # Streamlit simple line chart (interactive enough, no extra dependencies)
    plot_df = daily.set_index("Day")[["TMax", "TMin"]]
    st.line_chart(plot_df, height=360)
    st.caption("Daily TMax/TMin averaged across the selected years.")

with col2:
    st.subheader("Quick stats")
    st.metric("Monthly average TMax", f"{sub['TMax'].mean():.2f} °C")
    st.metric("Monthly average TMin", f"{sub['TMin'].mean():.2f} °C")

st.write("Daily averages overview:")
st.dataframe(
    daily.rename(columns={
        "Day": "Day",
        "TMax": "TMax (°C)",
        "TMin": "TMin (°C)"
    }),
    use_container_width=True
)