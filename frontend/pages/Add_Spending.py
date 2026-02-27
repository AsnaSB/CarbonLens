import streamlit as st
from api_client import post

st.header("🛒 Add Spending")
st.write("Enter spending → estimate CO₂ → save event.")

amount = st.number_input("Amount spent", min_value=0.0, step=10.0)
category = st.selectbox("Category", ["groceries", "clothing", "electronics", "dining", "fuel", "other"])

if st.button("Estimate Spending CO₂"):
    try:
        with st.spinner("Estimating CO₂..."):
            estimate = post("/estimate/spending", {"amount": amount, "category": category})

        st.session_state["spending_estimate"] = estimate
        st.session_state["spending_inputs"] = {"amount": amount, "category": category}

        co2_kg = estimate.get("co2_kg")
        st.success("Estimate ready ✅")
        st.metric("CO₂ (kg)", f"{co2_kg:.3f}" if isinstance(co2_kg, (int, float)) else str(co2_kg))

    except Exception as e:
        st.error(f"Error: {e}")

if "spending_estimate" in st.session_state:
    st.divider()
    st.subheader("Save this event")
    notes = st.text_input("Notes (optional)", placeholder="e.g., online order")

    if st.button("Save Spending Event"):
        try:
            est = st.session_state["spending_estimate"]
            inp = st.session_state["spending_inputs"]

            with st.spinner("Saving event..."):
                saved = post("/events", {
                    "category": "spending",
                    "amount": inp["amount"],
                    "spend_category": inp["category"],
                    "co2_kg": est.get("co2_kg"),
                    "notes": notes
                })

            st.success("Saved ✅")
            st.json(saved)

        except Exception as e:
            st.error(f"Save failed: {e}")