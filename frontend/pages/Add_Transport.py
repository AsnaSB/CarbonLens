import streamlit as st
from api_client import post

st.header("🚗 Add Transport")
st.write("Estimate CO₂ for a trip, then save it as an event.")

col1, col2 = st.columns(2)
with col1:
    from_place = st.text_input("From", placeholder="Kochi")
with col2:
    to_place = st.text_input("To", placeholder="Trivandrum")

mode = st.selectbox("Mode", ["car", "bus", "train", "flight", "bike", "walk"])

if st.button("Estimate Transport CO₂"):
    if not from_place.strip() or not to_place.strip():
        st.error("Please enter both From and To.")
    else:
        try:
            with st.spinner("Estimating distance & CO₂..."):
                estimate = post("/estimate/transport", {
                    "from_place": from_place,
                    "to_place": to_place,
                    "mode": mode
                })

            st.session_state["transport_estimate"] = estimate
            st.session_state["transport_inputs"] = {"from_place": from_place, "to_place": to_place, "mode": mode}

            distance_km = estimate.get("distance_km")
            co2_kg = estimate.get("co2_kg")

            st.success("Estimate ready ✅")
            a, b = st.columns(2)
            a.metric("Distance (km)", f"{distance_km:.2f}" if isinstance(distance_km, (int, float)) else str(distance_km))
            b.metric("CO₂ (kg)", f"{co2_kg:.3f}" if isinstance(co2_kg, (int, float)) else str(co2_kg))

            st.caption("If values show as None, backend response keys differ. Paste the response JSON and I’ll fix the frontend mapping.")

        except Exception as e:
            st.error(f"Error: {e}")

if "transport_estimate" in st.session_state:
    st.divider()
    st.subheader("Save this event")
    notes = st.text_input("Notes (optional)", placeholder="e.g., daily commute")

    if st.button("Save Transport Event"):
        try:
            est = st.session_state["transport_estimate"]
            inp = st.session_state["transport_inputs"]

            with st.spinner("Saving event..."):
                saved = post("/events", {
                    "category": "transport",
                    "mode": inp["mode"],
                    "from_place": inp["from_place"],
                    "to_place": inp["to_place"],
                    "distance_km": est.get("distance_km"),
                    "co2_kg": est.get("co2_kg"),
                    "notes": notes
                })

            st.success("Saved ✅")
            st.json(saved)

        except Exception as e:
            st.error(f"Save failed: {e}")