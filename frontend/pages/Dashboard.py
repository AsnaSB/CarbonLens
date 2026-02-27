import streamlit as st
import pandas as pd
import plotly.express as px
from api_client import get, post

st.header("📊 Dashboard")

range_opt = st.selectbox("Range", ["weekly", "monthly", "yearly"], index=0)

col1, col2 = st.columns([3, 1])

with col2:
    st.subheader("Demo")
    if st.button("Load Demo Data"):
        try:
            with st.spinner("Adding demo events..."):
                post("/events", {"category": "transport", "mode": "car", "distance_km": 10, "co2_kg": 2.0, "notes": "demo"})
                post("/events", {"category": "electricity", "kwh": 6, "co2_kg": 4.5, "notes": "demo"})
                post("/events", {"category": "spending", "amount": 500, "spend_category": "groceries", "co2_kg": 1.8, "notes": "demo"})
            st.success("Demo data added ✅")
        except Exception as e:
            st.error(f"Demo failed: {e}")

with col1:
    try:
        with st.spinner("Loading analytics..."):
            summary = get("/analytics/summary", params={"range": range_opt})

        total = summary.get("total_co2_kg")
        st.metric("Total CO₂ (kg)", f"{total:.3f}" if isinstance(total, (int, float)) else str(total))

        breakdown = summary.get("breakdown", [])
        if isinstance(breakdown, list) and breakdown:
            df_b = pd.DataFrame(breakdown)
            if {"category", "co2_kg"}.issubset(df_b.columns):
                st.subheader("Breakdown by Category")
                fig = px.bar(df_b, x="category", y="co2_kg")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Breakdown format mismatch. Showing raw data:")
                st.json(breakdown)
        else:
            st.info("No breakdown yet — add some events first.")

        trend = summary.get("trend", [])
        if isinstance(trend, list) and trend:
            df_t = pd.DataFrame(trend)
            if {"date", "co2_kg"}.issubset(df_t.columns):
                st.subheader("Trend")
                fig2 = px.line(df_t, x="date", y="co2_kg")
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.warning("Trend format mismatch. Showing raw data:")
                st.json(trend)

        hotspot = summary.get("hotspot")
        if isinstance(hotspot, dict):
            st.subheader("Hotspot")
            st.write(f"**Top source:** {hotspot.get('category')} — {hotspot.get('co2_kg')} kg")

    except Exception as e:
        st.error(f"Dashboard not ready: {e}")
        st.info("This needs backend endpoint GET /analytics/summary implemented.")