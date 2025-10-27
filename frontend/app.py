import streamlit as st
import requests
import plotly.express as px
from fpdf import FPDF
import io

from planner.planner_utils import generate_mock_plan, generate_diet_plan

# ---------------------------
# APP CONFIG
# ---------------------------
st.set_page_config(
    page_title="AI Fitness Coach",
    page_icon="💪",
    layout="wide"
)

# Global responsive styles (make buttons full-width on small viewports and improve form spacing)
st.markdown("""
    <style>
    /* Make Streamlit button controls expand to full width in their containers */
    div.stButton > button, div.stDownloadButton > button {
        width: 100% !important;
        padding: 0.6rem 0.8rem !important;
    }
    /* Tighter form field spacing */
    .stTextInput, .stNumberInput, .stSelectbox, .stMultiSelect {
        margin-bottom: 0.6rem;
    }
    @media (min-width: 900px) {
        div.stButton > button, div.stDownloadButton > button { width: 60% !important; }
    }
    </style>
""", unsafe_allow_html=True)

# Session state initialization
if "plan" not in st.session_state:
    st.session_state.plan = None
if "page" not in st.session_state:
    st.session_state.page = "🏠 Home"

# ---------------------------
# SIDEBAR NAVIGATION
# ---------------------------
st.sidebar.title("AI Fitness Coach")
page = st.sidebar.radio("Navigation", ["🏠 Home", "📋 Input Form", "📈 My Plan", "⚙️ Settings / About"])
st.session_state.page = page

# Small defaults and helpers
DEFAULT_API_URL = "http://localhost:8000/api/generate-plan"

# ---------------------------
# PAGE 1: HOME (Enhanced Design)
# ---------------------------
if page == "🏠 Home":
    st.markdown('<h1 class="main-title">AI Fitness Coach</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Your Smart AI Partner for Personalized Fitness Planning</p>', unsafe_allow_html=True)
    st.markdown("""
        <p class="description">
        This platform leverages <b>Artificial Intelligence</b> to design <b>personalized, 1-month fitness plans</b>
        tailored to your health conditions, daily activity, and fitness goals.
        </p>
    """, unsafe_allow_html=True)
    if st.button("🚀 Get Started", use_container_width=True):
        st.session_state.page = "📋 Input Form"
        st.rerun()

# ---------------------------
# PAGE 2: INPUT FORM
# ---------------------------
elif page == "📋 Input Form":
    st.title("📋 Enter Your Fitness Details")

    with st.form("input_form"):
        st.subheader("🧍 Basic Information")
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Full Name")
            age = st.number_input("Age", 10, 100, step=1)
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        with c2:
            height = st.number_input("Height (cm)", 100, 250)
            weight = st.number_input("Weight (kg)", 20, 200)

        st.subheader("🩺 Health & Conditions")
        conditions = st.multiselect("Existing Conditions", ["Heart issue", "Back pain", "Arthritis", "Asthma", "Diabetes", "Hypertension", "None"])
        limitations = st.multiselect("Physical Limitations", ["Cannot run", "Cannot lift weights", "Joint pain", "None"])
        doctor = st.radio("Doctor Approved?", ["Yes", "No"], horizontal=True)

        st.subheader("🏃 Fitness Tracker Inputs")
        c3, c4 = st.columns(2)
        with c3:
            steps = st.number_input("Average Steps / Day", 0, 50000, step=100)
            heart_rate = st.number_input("Average Heart Rate", 40, 200)
            calories = st.number_input("Calories Burned / Day", 0, 10000)
        with c4:
            sleep = st.number_input("Sleep Duration (hours)", 0.0, 24.0, step=0.5)
            active = st.number_input("Active Minutes", 0, 1440)
            sedentary = st.number_input("Sedentary Minutes", 0, 1440)

        st.subheader("🎯 Fitness Goals")
        goal = st.selectbox("Main Goal", ["Weight loss", "Flexibility", "Endurance", "Strength", "General fitness"])
        duration = st.selectbox("Workout Duration (min/day)", [15, 30, 45, 60])
        days = st.selectbox("Days per Week", [3, 4, 5, 6, 7])
        exercise_type = st.multiselect("Preferred Exercises", ["Yoga", "Walking", "Cycling", "Stretching", "Cardio", "Strength Training"])

        submitted = st.form_submit_button("🚀 Generate My Plan")

        if submitted:
            user_input = {
                "name": name, "age": age, "gender": gender,
                "height": height, "weight": weight,
                "existing_conditions": conditions,
                "physical_limitations": limitations,
                "doctor_approval": doctor,
                "daily_steps": steps, "heart_rate": heart_rate,
                "calories_burned": calories, "sleep_duration": sleep,
                "active_minutes": active, "sedentary_minutes": sedentary,
                "goal": goal, "duration_pref": duration, "days_per_week": days,
                "exercise_types": exercise_type
            }

            st.info("⏳ Generating your personalized plan...")
            api_url = st.session_state.get('api_url', DEFAULT_API_URL)
            use_mock = st.session_state.get('mock_mode', False) or (DEFAULT_API_URL in api_url)

            if use_mock:
                plan = generate_mock_plan(user_input)
                plan['diet_plan'] = generate_diet_plan(plan.get('plan_type', 'balanced'), user_input, plan.get('calories_target', 1800))
                st.session_state.plan = plan
                st.success("✅ Mock plan + diet generated (demo mode). Go to 'My Plan' tab to view it.")
            else:
                try:
                    response = requests.post(api_url, json=user_input, timeout=10)
                    if response.status_code == 200:
                        plan = response.json()
                        if plan.get('diet_plan') is None and plan.get('plan_type'):
                            calories_target = plan.get('calories_target', 1800)
                            plan['diet_plan'] = generate_diet_plan(plan.get('plan_type'), user_input, calories_target)
                        st.session_state.plan = plan
                        st.success("✅ Plan generated successfully! Go to 'My Plan' tab to view it.")
                    else:
                        st.error("❌ Model Error: " + response.text)
                except Exception as e:
                    st.warning(f"⚠️ Could not connect to backend: {e}")

# ---------------------------
# PAGE 3: MY PLAN
# ---------------------------
elif page == "📈 My Plan":
    st.title("📈 Your AI-Generated 1-Month Plan")

    plan = st.session_state.plan
    if not plan:
        st.warning("⚠️ No plan generated yet. Please go to the Input Form tab first.")
    else:
        st.subheader("🏃 Summary")
        st.write(f"**Activity Level:** {plan.get('activity_level', 'Moderate')}")
        st.write(f"**Calories Target per Day:** {plan.get('calories_target', '1800 kcal')}")
        st.write(f"**Step Goal per Day:** {plan.get('step_goal', '8000 steps')}")
        st.write(f"**Rest Days per Week:** {plan.get('rest_days', 2)}")

        st.markdown("### 🗓️ Weekly Schedule Overview")
        st.write(plan.get("plan", "Your personalized schedule will appear here."))

        st.markdown("### 📊 Weekly Progress Goal Visualization")
        weekly = plan.get('weekly_targets', None)
        if weekly and all(k in weekly for k in ("Week", "Steps Target", "Calories Target")):
            chart_data = weekly
        else:
            chart_data = {
                "Week": ["Week 1", "Week 2", "Week 3", "Week 4"],
                "Steps Target": [8000, 8500, 9000, 9500],
                "Calories Target": [1800, 1850, 1900, 2000]
            }

        fig = px.line(chart_data, x="Week", y=["Steps Target", "Calories Target"], markers=True)
        st.plotly_chart(fig, use_container_width=True)

        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=14)
            pdf.cell(0, 10, txt="AI Fitness Coach - 1 Month Plan", ln=True, align='C')
            pdf.ln(4)
            pdf.set_font("Arial", size=11)
            pdf.cell(0, 8, txt=f"Name: {plan.get('name', 'User')}", ln=True)
            pdf.cell(0, 8, txt=f"Activity Level: {plan.get('activity_level', 'Moderate')}", ln=True)
            pdf.cell(0, 8, txt=f"Calories Target (per day): {plan.get('calories_target', '1800')}", ln=True)
            pdf.cell(0, 8, txt=f"Step Goal (per day): {plan.get('step_goal', '8000')}", ln=True)
            pdf.ln(6)
            pdf.cell(0, 8, txt="Weekly Schedule:", ln=True)
            pdf.ln(2)
            schedule = plan.get('plan', {})
            if isinstance(schedule, dict):
                for wk, text in schedule.items():
                    pdf.multi_cell(0, 6, txt=f"{wk}: {text}")
                    pdf.ln(1)
            else:
                pdf.multi_cell(0, 6, txt=str(schedule))

                pdf.ln(4)
                pdf.cell(0, 8, txt="Diet Plan (7 days):", ln=True)
                diet = plan.get('diet_plan', {})
                if isinstance(diet, dict) and diet.get('meals'):
                    for day, items in diet.get('meals').items():
                        pdf.set_font("Arial", size=10)
                        pdf.cell(0, 6, txt=f"{day}:", ln=True)
                        for m in items:
                            pdf.multi_cell(0, 6, txt=f"  - {m['meal']} ({m['cal']} kcal): {m['suggestion']}")
                else:
                    pdf.multi_cell(0, 6, txt=str(diet))

            raw = pdf.output(dest='S')
            if isinstance(raw, str):
                raw = raw.encode('latin-1')

            st.download_button(
                label="📥 Download Plan as PDF",
                data=raw,
                file_name="Fitness_Plan_Report.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.warning(f"⚠️ Could not generate PDF: {e}")

# ---------------------------
# PAGE 4: SETTINGS / ABOUT
# ---------------------------
elif page == "⚙️ Settings / About":
    st.title("⚙️ Settings & About")
    st.write("""
    **AI Fitness Coach** is an intelligent health assistant that generates 
    safe, personalized fitness plans using AI and health analytics.
    """)

    st.markdown("#### 🔗 Backend Configuration")
    api_url = st.text_input("Backend API URL", st.session_state.get('api_url', DEFAULT_API_URL))
    st.session_state['api_url'] = api_url
    st.caption("Replace this URL with your actual ML backend endpoint when deployed.")

    mock_mode = st.checkbox("Enable mock/demo mode (no backend required)", value=st.session_state.get('mock_mode', False))
    st.session_state['mock_mode'] = mock_mode

    st.markdown("---")
    st.markdown("#### 🧑‍💻 Developed By")
    st.write("""
    **Smart Health-Tech AI Team**  
    Guided by: Department of Computer Science & Engineering  
    Year: 2025  
    """)

    st.markdown("---")
    st.caption("© 2025 AI Fitness Coach | All Rights Reserved.")
