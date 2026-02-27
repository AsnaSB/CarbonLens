import streamlit as st
from api_client import post

st.header("💡 Add Electricity")
st.write("Enter kWh → estimate CO₂ → save event.")

kwh = st.number_input("Electricity used (kWh)", min_value=0.0, step=1.0)

if st.button("Estimate Electricity CO₂"):
    try:
        with st.spinner("Estimating CO₂..."):
            estimate = post("/estimate/electricity", {"kwh": kwh})

        st.session_state["electricity_estimate"] = estimate
        st.session_state["electricity_inputs"] = {"kwh": kwh}

        co2_kg = estimate.get("co2_kg")
        st.success("Estimate ready ✅")
        st.metric("CO₂ (kg)", f"{co2_kg:.3f}" if isinstance(co2_kg, (int, float)) else str(co2_kg))

    except Exception as e:
        st.error(f"Error: {e}")

if "electricity_estimate" in st.session_state:
    st.divider()
    st.subheader("Save this event")
    notes = st.text_input("Notes (optional)", placeholder="e.g., Feb bill")

    if st.button("Save Electricity Event"):
        try:
            est = st.session_state["electricity_estimate"]
            inp = st.session_state["electricity_inputs"]

            with st.spinner("Saving event..."):
                saved = post("/events", {
                    "category": "electricity",
                    "kwh": inp["kwh"],
                    "co2_kg": est.get("co2_kg"),
                    "notes": notes
                })

            st.success("Saved ✅")
            st.json(saved)

        except Exception as e:
            st.error(f"Save failed: {e}")