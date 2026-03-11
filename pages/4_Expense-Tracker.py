import streamlit as st
import pandas as pd
from datetime import date
from database import get_db_connection

if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Please log in to access Expense Tracker.")
    st.stop()

st.set_page_config(page_title="Student Expense Tracker", layout="wide")

user_id = st.session_state.user["id"]

def load_budget():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT budget, budget_type FROM budgets WHERE user_id=?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return float(row[0]), row[1]
    else:
        return 0.0, "Monthly"

def save_budget(budget, budget_type):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM budgets WHERE user_id=?", (user_id,))
    if cursor.fetchone():
        cursor.execute(
            "UPDATE budgets SET budget=?, budget_type=? WHERE user_id=?",
            (budget, budget_type, user_id)
        )
    else:
        cursor.execute(
            "INSERT INTO budgets (user_id, budget, budget_type) VALUES (?, ?, ?)",
            (user_id, budget, budget_type)
        )
    conn.commit()
    conn.close()

def load_expenses():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, Category, Amount, Date FROM expenses WHERE user_id=? ORDER BY Date DESC", 
        (user_id,)
    )
    expenses = [
        {
            "id": e[0],
            "Category": e[1],
            "Amount": float(e[2]),
            "Date": pd.to_datetime(e[3]).date()
        } for e in cursor.fetchall()
    ]
    conn.close()
    return expenses

def add_expense(category, amount, expense_date):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO expenses (user_id, Category, Amount, Date) VALUES (?, ?, ?, ?)",
        (user_id, category, float(amount), expense_date.strftime("%Y-%m-%d"))
    )
    conn.commit()
    conn.close()

budget, budget_type = load_budget()
expenses = load_expenses()
df = pd.DataFrame(expenses)

st.sidebar.title("Student Budget")

new_budget = st.sidebar.number_input(
    "Set Budget Limit", min_value=0.0, value=budget, step=0.01, format="%.2f"
)
new_budget_type = st.sidebar.selectbox(
    "Budget Type", ["Weekly", "Monthly"], index=0 if budget_type=="Weekly" else 1
)

if st.sidebar.button("Save Budget"):
    save_budget(new_budget, new_budget_type)
    st.success("Budget saved!")
    budget, budget_type = load_budget()

st.sidebar.markdown("---")
st.sidebar.subheader("✙ New Expense")

category = st.sidebar.selectbox(
    "Category",
    ["Tuition", "Food", "Transportation", "School Supplies", "Printing", "Projects", "Miscellaneous"]
)

amount = st.sidebar.number_input(
    "Amount", min_value=0.0, step=0.01, format="%.2f"
)
expense_date = st.sidebar.date_input("Date", date.today())

if st.sidebar.button("Add Expense"):
    add_expense(category, amount, expense_date)
    st.success("Expense added!")
    expenses = load_expenses()
    df = pd.DataFrame(expenses)

st.title("Student Expense Tracker Dashboard")

if not df.empty:
    df["Amount"] = df["Amount"].astype(float)

total_spent = float(df["Amount"].sum()) if not df.empty else 0.0
budget_limit = float(budget)
available_balance = budget_limit - total_spent

col1, col2 = st.columns(2)
with col1:
    st.metric("Available Balance", f"₱ {available_balance:,.2f}")
with col2:
    st.metric("Budget Limit", f"₱ {budget_limit:,.2f}")

st.subheader("Budget Usage")
if budget_limit > 0:
    progress = total_spent / budget_limit
    st.progress(min(progress, 1.0))
st.write(f"Spent: ₱ {total_spent:,.2f}")

st.subheader("Recent Payments")
if not df.empty:
    recent = df.sort_values("Date", ascending=False).head(5)
    st.table(recent)
else:
    st.info("No expenses yet.")

st.subheader("Monthly Expenses by Category")
if not df.empty:
    chart_data = df.groupby("Category")["Amount"].sum()
    st.bar_chart(chart_data)
else:
    st.info("No data for chart.")