import streamlit as st
import requests
import pandas as pd

BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="CarbonLens", layout="wide")

# ---------------------------------------------------
# LIGHT BACKGROUND + BLACK TEXT + BLACK LABELS
# ---------------------------------------------------
def set_light_bg(url: str):
    st.markdown(
        f"""
        <style>

        /* Background Image with White Overlay */
        .stApp {{
            background: linear-gradient(rgba(255,255,255,0.30), rgba(255,255,255,0.20)),
                        url("{url}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}

        /* Main Content Container */
        section.main > div {{
            background-color: rgba(255,255,255,0.55);
            padding: 30px;
            border-radius: 18px;
        }}

        /* Force All Text to Black */
        html, body, [class*="css"] {{
            color: black !important;
        }}

        h1, h2, h3, h4 {{
            color: black !important;
        }}

        /* ✅ Force widget labels (Category/Description/Value/Transport Mode) to BLACK */
        div[data-testid="stWidgetLabel"] > label {{
            color: black !important;
        }}

        /* Light Input Fields */
        div[data-baseweb="select"] > div,
        .stTextInput input,
        .stNumberInput input {{
            background-color: #ffffff !important;
            color: black !important;
            border-radius: 8px !important;
        }}

        /* Buttons */
        .stButton button {{
            background-color: #4CAF50;
            color: white;
            border-radius: 8px;
            border: none;
        }}

        .stButton button:hover {{
            background-color: #45a049;
        }}

        /* Dataframe Background */
        .stDataFrame {{
            background-color: white !important;
        }}

        </style>
        """,
        unsafe_allow_html=True
    )

set_light_bg(
    "https://images.unsplash.com/photo-1469474968028-56623f02e42e?auto=format&fit=crop&w=1920&q=80"
)

# ---------------------------------------------------
# UI CONTENT
# ---------------------------------------------------
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