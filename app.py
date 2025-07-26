# ======================================================================================
# 1. IMPORTS
# ======================================================================================
import streamlit as st
import pandas as pd
import joblib
from PIL import Image

# ======================================================================================
# 2. PAGE CONFIGURATION
# ======================================================================================
st.set_page_config(
    page_title="Salary AI - Showcase Version",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ======================================================================================
# 3. CUSTOM CSS
# ======================================================================================
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(to right, #141E30, #243B55);
    }
    .main .block-container { padding: 2rem 3rem; }
    .form-container {
        background: rgba(255, 255, 255, 0.07);
        padding: 2rem;
        border-radius: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(6px);
    }
    .stButton>button {
        background: linear-gradient(to right, #06b6d4, #3b82f6);
        color: white;
        font-size: 1rem;
        padding: 0.7rem 1.5rem;
        border: none;
        border-radius: 0.5rem;
        font-weight: bold;
    }
    .stMetric {
        background-color: #1e293b;
        border-radius: 1rem;
        padding: 1.2rem;
    }
    .stMetric > label {
        font-weight: bold;
        color: #60a5fa;
    }
    .stMetric > div > span {
        font-size: 2.2rem;
        color: #93c5fd;
        font-weight: 700;
    }
    .stExpander {
        background: rgba(30, 41, 59, 0.9);
        border-radius: 0.5rem;
        border: 1px solid #475569;
    }
    .footer {
        text-align: center;
        padding: 2rem;
        color: #cbd5e1;
    }
    .footer a {
        color: #3b82f6;
        text-decoration: none;
        font-weight: 600;
        margin: 0 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ======================================================================================
# 4. LOAD RESOURCES
# ======================================================================================
@st.cache_data
def load_all_assets():
    model_data = joblib.load("salary_predictor.pkl")
    eval_plot = Image.open("images/plot.png")
    return model_data, eval_plot

model_data, eval_plot = load_all_assets()
model = model_data["model"]
label_encoders = model_data["label_encoders"]
scaler = model_data["scaler"]

# ======================================================================================
# 5. SESSION STATE
# ======================================================================================
if 'prediction_made' not in st.session_state:
    st.session_state.prediction_made = False
    st.session_state.predicted_salary = 0.0

# ======================================================================================
# 6. UI LAYOUT - TITLE
# ======================================================================================
st.markdown("""
<div style="text-align: center; padding: 2rem 1rem;">
    <h1 style="font-size: 4rem; font-family: 'Segoe UI', sans-serif; color: #ffffff;">
        💼 <i>"Know Your Worth"</i> 💰
    </h1>
    <h2 style="color: #cbd5e1; font-size: 1.6rem;">
        ✨ Discover your AI-predicted salary in seconds using ML magic! 🧠⚙️
    </h2>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1.2, 1], gap="large")

# --- INPUT FORM ---
with col1:
    with st.form("salary_form"):
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #c7d2fe;'>👤 Employee Profile</h3>", unsafe_allow_html=True)

        form_col1, form_col2 = st.columns(2)
        with form_col1:
            age = st.number_input("Age", min_value=18, max_value=80, value=30)
            education_level = st.selectbox("Education Level", options=label_encoders["Education Level"].classes_, index=2)
        with form_col2:
            years_of_experience = st.number_input("Years of Experience", min_value=0, max_value=40, value=5)
            gender = st.selectbox("Gender", options=label_encoders["Gender"].classes_)

        job_title = st.selectbox("Job Title", options=label_encoders["Job Title"].classes_, index=5)
        submit_button = st.form_submit_button("✨ Divine the Salary")
        st.markdown('</div>', unsafe_allow_html=True)

# --- OUTPUT DISPLAY ---
with col2:
    if not st.session_state.prediction_made:
        st.info("Your prediction will appear here once submitted.", icon="💡")
    else:
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #c7d2fe;'>🔮 Oracle's Vision</h3>", unsafe_allow_html=True)

        # Convert USD to INR (₹)
        exchange_rate = 83
        salary_usd = st.session_state.predicted_salary
        salary_inr = salary_usd * exchange_rate

        st.metric(
            label="Estimated Annual Salary Range (INR)",
            value=f"₹{salary_inr * 0.925:,.0f} - ₹{salary_inr * 1.075:,.0f}",
            delta="Based on your inputs",
            delta_color="off"
        )
        st.success("The vision is clear! Prediction successful.", icon="✅")
        st.markdown('</div>', unsafe_allow_html=True)

# ======================================================================================
# 7. PREDICTION LOGIC
# ======================================================================================
if submit_button:
    input_data = {
        "Age": age,
        "Gender": gender,
        "Education Level": education_level,
        "Job Title": job_title,
        "Years of Experience": years_of_experience
    }
    input_df = pd.DataFrame([input_data])

    for col in ["Gender", "Education Level", "Job Title"]:
        input_df[col] = label_encoders[col].transform(input_df[col])

    input_scaled = scaler.transform(input_df)
    predicted_salary = model.predict(input_scaled)[0]

    st.session_state.predicted_salary = predicted_salary
    st.session_state.prediction_made = True
    st.balloons()
    st.rerun()

# ======================================================================================
# 8. FOOTER + EVALUATION
# ======================================================================================
st.markdown("---")
with st.expander(" 📈 Peek behind the curtain at the model's performance..."):
    st.image(eval_plot, caption="Model Evaluation: Actual vs. Predicted Salaries", use_container_width=True)
    st.info("This plot shows the relationship between the model's predicted salaries and the actual salaries from the test dataset. A strong positive correlation indicates high accuracy.")

st.markdown("---")
st.markdown("""
<div class="footer">
    <p>Crafted with 🧠 & ❤️ by <b>Kalyan Barri</b></p>
    <a href="https://github.com/kalyan-kim" target="_blank">GitHub</a> | 
    <a href="https://www.linkedin.com/in/kalyan-barri/" target="_blank">LinkedIn</a>
</div>
""", unsafe_allow_html=True)
