import streamlit as st
from api_client import get

st.header("🏅 Credits & Progress")

try:
    with st.spinner("Loading weekly credits..."):
        data = get("/credits/weekly")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("CO₂ Saved (kg)", data.get("co2_saved", 0))
    c2.metric("Credits Earned", data.get("credits_earned", 0))
    c3.metric("Weekly Bonus", data.get("weekly_bonus", 0))
    c4.metric("Streak", data.get("streak_count", 0))

    st.subheader("Week comparison")
    st.write(f"- This week CO₂: **{data.get('total_co2_week')} kg**")
    st.write(f"- Previous week CO₂: **{data.get('total_co2_prev_week')} kg**")

    if (data.get("co2_saved") or 0) > 0:
        st.success("Great! You reduced emissions vs last week ✅")
    else:
        st.warning("No reduction yet — reduce one category to earn credits.")

    st.subheader("Debug")
    st.json(data)

except Exception as e:
    st.error(f"Credits page not ready: {e}")
    st.info("This needs backend endpoint GET /credits/weekly implemented.")