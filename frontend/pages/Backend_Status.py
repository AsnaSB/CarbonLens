import streamlit as st
from api_client import get, post

st.header("🩺 Backend Status / API Contract Check")
st.write("This page helps you verify which endpoints are live and what JSON they return.")

checks = [
    ("GET", "/health", None),
    ("POST", "/estimate/transport", {"from_place": "Kochi", "to_place": "Trivandrum", "mode": "car"}),
    ("POST", "/estimate/electricity", {"kwh": 10}),
    ("POST", "/estimate/spending", {"amount": 500, "category": "groceries"}),
    ("GET", "/analytics/summary", {"range": "weekly"}),
    ("GET", "/credits/weekly", None),
]

st.info("Run backend first: uvicorn app.main:app --reload, then refresh this page.")

for method, path, payload in checks:
    with st.expander(f"{method} {path}"):
        try:
            if method == "GET":
                params = payload if isinstance(payload, dict) else None
                data = get(path, params=params)
            else:
                data = post(path, payload)

            st.success("OK ✅")
            st.json(data)

        except Exception as e:
            st.error(f"Not ready / error: {e}")
            st.caption("If backend not implemented yet, this is expected.")