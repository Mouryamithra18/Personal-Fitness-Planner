import streamlit as st
import requests
import plotly.express as px
from fpdf import FPDF

# ---------------------------
# APP CONFIG
# ---------------------------
st.set_page_config(
    page_title="AI Fitness Coach",
    page_icon="💪",
    layout="wide"
)

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

# ---------------------------
# PAGE 1: HOME (Enhanced Design)
# ---------------------------
if page == "🏠 Home":
    st.markdown("""
        <style>
        .main-title {
            font-size: 2.4rem;
            font-weight: 800;
            color: #1E293B;
            text-align: center;
            margin-bottom: 0.5rem;
        }
        .sub-title {
            font-size: 1.2rem;
            color: #0ea5e9;
            text-align: center;
            margin-bottom: 2.2rem;
            font-weight: 500;
        }
        .logo-container {
            display: flex;
            justify-content: center;
            margin-top: 1.5rem;
            margin-bottom: 1.5rem;
        }
        .logo-img {
            border-radius: 50%;
            width: 120px;
            height: 120px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            border: 3px solid #f1f5f9;
            object-fit: cover;
        }
        .banner {
            display: flex;
            justify-content: center;
            margin-bottom: 2rem;
        }
        .description {
            text-align: center;
            color: #475569;
            font-size: 1rem;
            max-width: 750px;
            margin: auto;
            line-height: 1.7;
        }
        .footer {
            text-align: center;
            font-size: 0.85rem;
            color: #94A3B8;
            margin-top: 3rem;
        }
        </style>
    """, unsafe_allow_html=True)

    # Visible circular logo (replace with your logo URL if available)
    st.markdown("""
        <div class="logo-container">
            <img src="https://www.citypng.com/public/uploads/preview/gym-fitness-club-black-logo-png-701751694772438pqqjnhp9nj.png" width="120"" class="logo-img">
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<h1 class="main-title">AI Fitness Coach</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Your Smart AI Partner for Personalized Fitness Planning</p>', unsafe_allow_html=True)

    st.markdown("""
        <p class="description">
        This platform leverages <b>Artificial Intelligence</b> to design <b>personalized, 1-month fitness plans</b> 
        tailored to your health conditions, daily activity, and fitness goals.
        It’s ideal for healthcare startups, wellness research, and smart lifestyle systems.
        </p>
    """, unsafe_allow_html=True)

    st.markdown("### ⭐ Key Features")
    st.write("- 🧠 AI-based customized workout generation")
    st.write("- 🩺 Health-condition–aware recommendations")
    st.write("- 📱 Integration with fitness-tracker data")
    st.write("- 🎯 Goal-based plans (Weight Loss, Strength, Endurance)")
    st.write("- 📄 Export PDF reports & visualize weekly progress")

    st.markdown("---")
    # ✅ Proper redirect using rerun
    if st.button("🚀 Get Started", use_container_width=True):
        st.session_state.page = "📋 Input Form"
        st.rerun()

    st.markdown('<p class="footer">© 2025 AI Fitness Coach | Developed as part of a Smart Health-Tech Initiative</p>', unsafe_allow_html=True)

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

            api_url = "https://your-backend-url/api/generate-plan"  # replace with your backend
            try:
                response = requests.post(api_url, json=user_input)
                if response.status_code == 200:
                    st.session_state.plan = response.json()
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
        chart_data = {
            "Week": ["Week 1", "Week 2", "Week 3", "Week 4"],
            "Steps Target": [8000, 8500, 9000, 9500],
            "Calories Target": [1800, 1850, 1900, 2000]
        }
        fig = px.line(chart_data, x="Week", y=["Steps Target", "Calories Target"], markers=True)
        st.plotly_chart(fig, use_container_width=True)

        st.download_button(
            label="📥 Download Plan as PDF",
            data="Personalized fitness plan content will go here.",
            file_name="Fitness_Plan_Report.pdf",
            mime="application/pdf"
        )

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
    api_url = st.text_input("Backend API URL", "https://your-backend-url/api/generate-plan")
    st.caption("Replace this URL with your actual ML backend endpoint when deployed.")

    st.markdown("---")
    st.markdown("#### 🧑‍💻 Developed By")
    st.write("""
    **Smart Health-Tech AI Team**  
    Guided by: Department of Computer Science & Engineering  
    Year: 2025  
    """)

    st.markdown("---")
    st.caption("© 2025 AI Fitness Coach | All Rights Reserved.")
