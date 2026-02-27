import streamlit as st

st.set_page_config(page_title="CarbonLens", page_icon="🌍", layout="wide")

st.title("🌍 CarbonLens")
st.caption("Personal Lifestyle Emission Analyzer — Transport • Electricity • Spending")

st.markdown("""
### Demo Flow (2–3 minutes)
1. Go to **Add Transport** → estimate → save  
2. Go to **Add Electricity** → estimate → save  
3. Go to **Add Spending** → estimate → save  
4. Open **Dashboard** → show totals + breakdown  
5. Open **Credits & Progress** → show streak + bonus *(if backend ready)*  
6. Open **Community Simulation** → show societal impact
""")

st.info("Make sure backend is running. Set BACKEND_URL in frontend/.env (example: http://127.0.0.1:8000).")