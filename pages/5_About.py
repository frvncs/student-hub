import streamlit as st

if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Please log in to access About.")
    st.stop()

st.set_page_config(layout="wide", page_title="Student Hub - About", page_icon="🎓")

st.markdown(
    """
    <div style='
        text-align:center; 
        padding:60px 20px; 
        background: linear-gradient(135deg, #B497BD, #6A8CAF); 
        border-radius: 20px; 
        color:white;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
    '>
        <h1 style='font-size:52px; margin-bottom:10px; font-weight:bold;'>Focused on What Matters</h1>
        <p style='font-size:20px; color: rgba(255,255,255,0.9); max-width:700px; margin:auto;'>
        Student Hub is your companion for academic success and organization
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("## What the App Does")
st.markdown(
    """
Student Hub is a productivity web application built to help students take control of their academic life—all in one intuitive platform.

With Student Hub, you can:
- Manage Notes: Create, organize, and quickly access all your study materials.
- Track Tasks & Deadlines: Stay on top of assignments, projects, and exams, with live progress updates as you complete tasks.
- Plan Focused Study Sessions: Use timers and focus tools to maximize productivity.
- Monitor Expenses: Keep track of tuition, books, and daily school expenses effortlessly.
- Visualize Your Progress: See your tasks, deadlines, and goals in one dashboard with real-time updates.
- Stay Organized Anywhere: Everything you need is in a single platform, eliminating the need to juggle multiple apps.
- Student Hub empowers you to stay organized, focused, and productive—helping you achieve more with less stress.
    """
)

st.markdown("## Target Users")
st.markdown(
    """
Student Hub is designed for students who want a simple and efficient way to stay on track with their academic life.
Whether you're a high school student managing classes and extracurricular activities, a college student balancing 
coursework and part-time job.
Student Hub will help you stay organized, focused, and in control of your daily tasks.
    """
)

st.markdown("## Features Overview")
col1, col2 = st.columns(2)

card_style = """
    <div style='
        background: linear-gradient(135deg, #B497BD, #6A8CAF); 
        padding:20px; 
        border-radius:15px; 
        margin-bottom:20px;
        color:white;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    ' onmouseover="this.style.transform='scale(1.05)';" onmouseout="this.style.transform='scale(1)';">
        <h3 style='margin-bottom:10px;'>{} </h3>
        <p style='margin:0;'>{}</p>
    </div>
"""

with col1:
    st.subheader("Inputs")
    st.markdown(card_style.format("Notes & Media", "- Text & Images for Notes"), unsafe_allow_html=True)
    st.markdown(card_style.format("Tasks & Deadlines", "- To-do items & Deadlines"), unsafe_allow_html=True)
    st.markdown(card_style.format("Pomodoro Timer", "- Study session durations"), unsafe_allow_html=True)
    st.markdown(card_style.format("Expenses", "- Budget & Spending details"), unsafe_allow_html=True)

with col2:
    st.subheader("Outputs")
    st.markdown(card_style.format("Saved Notes", "- Access anytime"), unsafe_allow_html=True)
    st.markdown(card_style.format("Reminders", "- Deadlines & Alerts"), unsafe_allow_html=True)
    st.markdown(card_style.format("Pomodoro Reports", "- Track study sessions"), unsafe_allow_html=True)
    st.markdown(card_style.format("Expense Summary", "- Remaining balance & history"), unsafe_allow_html=True)


st.markdown(
    """
    <div style="
        text-align:center; 
        margin-top:40px; 
        padding:40px 20px; 
        background: linear-gradient(135deg, #6A8CAF, #B497BD);
        border-radius:20px;
        color:white;
        box-shadow:0 8px 32px rgba(0,0,0,0.2);
    ">
        <h2 style='margin-bottom:15px;'>Ready to take control of your student life?</h2>
        <p style='margin-bottom:25px; font-size:18px;'>Explore Student Hub today and start organizing smarter, not harder</p>
        <a href="#" style="
            padding:12px 25px; 
            background:white; 
            color:#6A8CAF; 
            font-weight:bold; 
            border-radius:10px; 
            text-decoration:none;
            box-shadow:0 4px 20px rgba(0,0,0,0.2);
        ">Get Started</a>
    </div>
    """,
    unsafe_allow_html=True
)