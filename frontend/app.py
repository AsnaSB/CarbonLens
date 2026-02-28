import streamlit as st
import requests
import pandas as pd

BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="CarbonLens", layout="wide")

st.title("🌱 CarbonLens Dashboard")

# ---------------------------------------------------
# ADD EVENT SECTION
# ---------------------------------------------------
st.header("Add New Event")

category = st.selectbox(
    "Category",
    ["transport", "electricity", "spending"]
)

description = st.text_input("Description")
value = st.number_input("Value", min_value=0.0)

transport_mode = None
spend_category = None

if category == "transport":
    transport_mode = st.selectbox(
        "Transport Mode",
        ["car", "bus", "train", "bike"]
    )

if category == "spending":
    spend_category = st.selectbox(
        "Spending Category",
        ["food", "shopping", "travel", "clothing", "default"]
    )

if st.button("Save Event"):

    payload = {
        "category": category,
        "description": description,
        "value": value
    }

    if transport_mode:
        payload["transport_mode"] = transport_mode

    if spend_category:
        payload["spend_category"] = spend_category

    response = requests.post(f"{BASE_URL}/events", json=payload)

    if response.status_code == 200:
        st.success("Event Saved Successfully!")
        st.json(response.json())
    else:
        st.error("Error")
        st.json(response.json())

# ---------------------------------------------------
# VIEW EVENTS
# ---------------------------------------------------
st.header("All Events")

if st.button("Refresh Events"):
    response = requests.get(f"{BASE_URL}/events")
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data)
        st.dataframe(df)
    else:
        st.error("Could not fetch events")

# ---------------------------------------------------
# ANALYTICS SUMMARY
# ---------------------------------------------------
st.header("Analytics Summary")

range_option = st.selectbox(
    "Select Range",
    ["weekly", "monthly", "yearly"]
)

if st.button("Get Summary"):
    response = requests.get(
        f"{BASE_URL}/events/analytics/summary",
        params={"range": range_option}
    )
    if response.status_code == 200:
        st.json(response.json())
    else:
        st.error("Failed to fetch summary")

# ---------------------------------------------------
# ANALYTICS TRENDS
# ---------------------------------------------------
st.header("Trends")

if st.button("Show Trends"):
    response = requests.get(
        f"{BASE_URL}/events/analytics/trends",
        params={"range": range_option}
    )
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data)
        st.line_chart(df.set_index("period")["total_co2"])
    else:
        st.error("Failed to fetch trends")

# ---------------------------------------------------
# WEEKLY CREDITS
# ---------------------------------------------------
st.header("Weekly Credits")

if st.button("Check Credits"):
    response = requests.get(f"{BASE_URL}/events/credits/weekly")
    if response.status_code == 200:
        st.json(response.json())
    else:
        st.error("Failed to fetch credits")