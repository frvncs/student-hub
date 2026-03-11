import streamlit as st
from database import create_tables, get_db_connection
from auth import signup_user, login_user
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
import random

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(page_title="Student Hub", layout="wide")

create_tables()

# -------------------------
# SESSION STATE
# -------------------------
if "user" not in st.session_state:
    st.session_state.user = None


# -------------------------
# DATABASE FUNCTIONS
# -------------------------

def count_notes(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM notes WHERE user_id=? AND archived=0",
        (user_id,)
    )

    count = cursor.fetchone()[0]
    conn.close()
    return count


def count_tasks(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM tasks WHERE user_id=? AND Progress!='Completed'",
        (user_id,)
    )

    count = cursor.fetchone()[0]
    conn.close()
    return count


def load_budget(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT budget FROM budgets WHERE user_id=?",
        (user_id,)
    )

    row = cursor.fetchone()
    conn.close()

    return float(row[0]) if row else 0.0


def load_expenses(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT Amount FROM expenses WHERE user_id=?",
        (user_id,)
    )

    rows = cursor.fetchall()
    conn.close()

    return sum(float(r[0]) for r in rows) if rows else 0.0


# -------------------------
# LOGIN / SIGNUP PAGE
# -------------------------
def login_page():

    st.title("Login to Student Hub")

    menu = ["Login", "Sign Up"]
    choice = st.selectbox("Select an option", menu)

    if choice == "Login":

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):

            user = login_user(username, password)

            if user:
                st.session_state.user = user
                st.success(f"Welcome {user['username']}!")
                st.rerun()

            else:
                st.error("Invalid username or password")


    elif choice == "Sign Up":

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Sign Up"):

            if not username or not password:
                st.warning("Please fill in all fields")

            else:
                success, msg = signup_user(username, password)

                if success:
                    st.success(msg)
                else:
                    st.error(msg)


# -------------------------
# DASHBOARD
# -------------------------
def dashboard():

    user = st.session_state.user
    user_id = user["id"]
    username = user["username"]

    # Auto refresh every 2 seconds
    st_autorefresh(interval=2000, key="dashboard_refresh")

    st.title("Student Hub Dashboard")

    hour = datetime.now().hour

    if 2 <= hour <= 11:
        greeting = "🌅 Good Morning"
    elif 12 <= hour <= 18:
        greeting = "☀️ Good Afternoon"
    else:
        greeting = "🌙 Good Evening"

    st.subheader(f"{greeting}, {username}!")

    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()

    st.subheader("Your Overview")

    # -------------------------
    # LOAD METRICS (FROM DATABASE)
    # -------------------------

    notes_created = count_notes(user_id)
    upcoming_deadlines = count_tasks(user_id)

    total_budget = load_budget(user_id)
    total_spent = load_expenses(user_id)

    available_balance = total_budget - total_spent

    # -------------------------
    # CARD STYLE
    # -------------------------
    st.markdown("""
    <style>
    .card {
        background: linear-gradient(135deg, #B497BD, #6A8CAF);
        border-radius: 15px;
        padding: 20px;
        color: white;
        text-align:center;
        transition: all 0.4s ease;
        box-shadow:0 8px 25px rgba(0,0,0,0.2);
    }

    .card:hover{
        transform:translateY(-6px) scale(1.03);
    }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="card">
        <h3>Notes Created</h3>
        <p>{notes_created}</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="card">
        <h3>Active Tasks</h3>
        <p>{upcoming_deadlines}</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="card">
        <h3>Available Balance</h3>
        <p>₱ {available_balance:,.2f}</p>
        </div>
        """, unsafe_allow_html=True)

    # -------------------------
    # INFO ROW
    # -------------------------

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("At a Glance")
    frosted = """
    background: rgba(255,255,255,0.15);
    border-radius:15px;
    padding:20px;
    text-align:center;
    backdrop-filter:blur(10px);
    box-shadow:0 8px 30px rgba(0,0,0,0.2);
    """

    col1, col2, col3 = st.columns(3)

    with col1:

        today = datetime.today().strftime("%A, %B %d, %Y")

        st.markdown(
            f"<div style='{frosted}'>📅 <b>Today</b><br>{today}</div>",
            unsafe_allow_html=True
        )

    with col2:

        now = datetime.now().strftime("%H:%M:%S")

        st.markdown(
            f"<div style='{frosted}'>⏰ <b>Current Time</b><br>{now}</div>",
            unsafe_allow_html=True
        )

    with col3:

        quotes = [
            "Believe you can and you're halfway there.",
            "Push yourself because no one else will.",
            "Small progress is still progress.",
            "Success starts with discipline.",
            "Dream big. Start small. Act now."
        ]

        quote = random.choice(quotes)

        st.markdown(
            f"<div style='{frosted}'>💡 <b>Motivation</b><br>{quote}</div>",
            unsafe_allow_html=True
        )


# -------------------------
# MAIN FLOW
# -------------------------

if st.session_state.user is None:
    login_page()

else:

    st.sidebar.title("Action Center")

    dashboard()