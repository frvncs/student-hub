import streamlit as st
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh  # new method

if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Please log in to access Focus.")
    st.stop()

st.set_page_config(page_title="Focus", layout="wide")

st_autorefresh(interval=1000, key="timer_refresh")

if 'end_time' not in st.session_state:
    st.session_state.end_time = None
if 'running' not in st.session_state:
    st.session_state.running = False
if 'timer_label' not in st.session_state:
    st.session_state.timer_label = ""
if 'paused_time_left' not in st.session_state:
    st.session_state.paused_time_left = None

def start_timer(seconds, label):
    st.session_state.timer_label = label
    st.session_state.end_time = datetime.now() + timedelta(seconds=seconds)
    st.session_state.running = True
    st.session_state.paused_time_left = None

def pause_timer():
    if st.session_state.running:
        st.session_state.paused_time_left = max(
            int((st.session_state.end_time - datetime.now()).total_seconds()), 0
        )
        st.session_state.running = False

def resume_timer():
    if not st.session_state.running and st.session_state.paused_time_left:
        st.session_state.end_time = datetime.now() + timedelta(seconds=st.session_state.paused_time_left)
        st.session_state.running = True
        st.session_state.paused_time_left = None

def reset_timer():
    st.session_state.running = False
    st.session_state.end_time = None
    st.session_state.paused_time_left = None
    st.session_state.timer_label = ""

def format_time(seconds):
    mins = seconds // 60
    secs = seconds % 60
    return f"{mins:02d}:{secs:02d}"

st.sidebar.title("🌣  Timer Settings")
if st.sidebar.button("25 mins"):
    start_timer(25*60, "Focus Time")
if st.sidebar.button("90 mins"):
    start_timer(90*60, "Focus Time")
custom_time = st.sidebar.text_input("Custom (min)", "")
if st.sidebar.button("Start Custom Timer"):
    if custom_time.isdigit() and int(custom_time) > 0:
        start_timer(int(custom_time)*60, "Focus Time")
    else:
        st.sidebar.warning("Enter a valid number.")

st.sidebar.subheader("⏱  Breaks")
if st.sidebar.button("Short Break (5 mins)"):
    start_timer(5*60, "Short Break")
if st.sidebar.button("Long Break (10 mins)"):
    start_timer(10*60, "Long Break")

st.markdown("<h1 style='text-align: center;'>Focus Timer</h1>", unsafe_allow_html=True)

if st.session_state.running:
    remaining_seconds = max(int((st.session_state.end_time - datetime.now()).total_seconds()), 0)
    if remaining_seconds == 0:
        st.session_state.running = False
        st.success(f"{st.session_state.timer_label} finished! 🎉")
else:
    remaining_seconds = st.session_state.paused_time_left or 0

st.markdown(
    f"<h1 style='text-align:center;font-size:120px;'>{format_time(remaining_seconds)}</h1>",
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns([1, 2, 1])  

with col2:
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    
with btn_col1:
    if st.button("Pause"):
        pause_timer()
        st.toast("Timer Paused")

with btn_col2:
    if st.button("Resume"):
        resume_timer()
        st.toast("Timer Resumed")

with btn_col3:
    if st.button("Reset"):
        reset_timer()
        st.toast("Timer Reset")