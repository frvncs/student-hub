import streamlit as st
import pandas as pd
from datetime import datetime, date
from database import get_db_connection

if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Please log in to access Task Manager.")
    st.stop()

st.set_page_config(page_title="Task Manager", layout="wide")

user_id = st.session_state.user["id"]

def load_tasks():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, Task, Deadline, SubmissionTime, Priority, Progress
        FROM tasks
        WHERE user_id=?
        ORDER BY Deadline ASC
    """, (user_id,))

    tasks = [{
        "id": t[0],
        "Task": t[1],
        "Deadline": datetime.strptime(t[2], "%Y-%m-%d").date() if t[2] else None,
        "Submission Time": datetime.strptime(t[3], "%H:%M:%S").time() if t[3] else None,
        "Priority": t[4],
        "Progress": t[5]
    } for t in cursor.fetchall()]

    conn.close()
    return tasks


def add_task_to_db(task_name, deadline, submission_time, priority, progress):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tasks (user_id, Task, Deadline, SubmissionTime, Priority, Progress)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        task_name,
        deadline.strftime("%Y-%m-%d"),
        submission_time.strftime("%H:%M:%S") if submission_time else None,
        priority,
        progress
    ))

    conn.commit()
    conn.close()

def update_task_db(task_id, priority, progress):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tasks
        SET Priority=?, Progress=?
        WHERE id=? AND user_id=?
    """, (priority, progress, task_id, user_id))

    conn.commit()
    conn.close()

def delete_task_db(task_id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM tasks
        WHERE id=? AND user_id=?
    """, (task_id, user_id))

    conn.commit()
    conn.close()

st.sidebar.header("✙ New Task")

task_name = st.sidebar.text_input("Task Name")
deadline = st.sidebar.date_input("Deadline")
submission_time = st.sidebar.time_input("Submission Time")
priority = st.sidebar.selectbox("Priority", ["Low", "Medium", "High"])
progress = st.sidebar.selectbox(
    "Progress",
    ["Not Started", "On Going", "On Review", "Completed"]
)

if st.sidebar.button("Add Task"):

    if task_name.strip() == "":
        st.sidebar.warning("Enter a task name")

    else:
        add_task_to_db(task_name, deadline, submission_time, priority, progress)
        st.sidebar.success("Task added!")
        st.rerun()

tasks = load_tasks()

st.title("Task Manager")

df = pd.DataFrame(tasks)

filter_priority = st.selectbox("Filter by Priority", ["All", "Low", "Medium", "High"])

if filter_priority != "All":
    df = df[df["Priority"] == filter_priority]

st.subheader("Manage Tasks")

if not df.empty:

    for task in tasks:

        col1, col2, col3, col4 = st.columns([3,2,2,1])

        with col1:
            st.write(task["Task"])

        with col2:
            new_progress = st.selectbox(
                "Progress",
                ["Not Started","On Going","On Review","Completed"],
                index=["Not Started","On Going","On Review","Completed"].index(task["Progress"]),
                key=f"prog{task['id']}"
            )

        with col3:
            new_priority = st.selectbox(
                "Priority",
                ["Low","Medium","High"],
                index=["Low","Medium","High"].index(task["Priority"]),
                key=f"prio{task['id']}"
            )

        with col4:
            if st.button("🗑️", key=f"del{task['id']}"):

                delete_task_db(task["id"])

                st.rerun()

        if new_progress != task["Progress"] or new_priority != task["Priority"]:

            update_task_db(task["id"], new_priority, new_progress)

            st.rerun()

else:
    st.info("No tasks available yet.")

st.subheader("Task Progress Overview")

if not df.empty:

    import plotly.express as px

    progress_chart = df["Progress"].value_counts().reset_index()
    progress_chart.columns = ["Progress", "Tasks"]

    fig = px.bar(progress_chart, x="Progress", y="Tasks", color="Progress", text="Tasks")

    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("No tasks available yet.")

st.subheader("Kanban Board")

if not df.empty:

    col1, col2, col3, col4 = st.columns(4)

    progress_columns = ["Not Started", "On Going", "On Review", "Completed"]

    columns = [col1, col2, col3, col4]

    for i, prog in enumerate(progress_columns):

        with columns[i]:

            st.markdown(f"### {prog}")

            for task in tasks:

                if task["Progress"] == prog:

                    st.markdown(
                        f"""
                        <div style="
                        background:#f3f4f6;
                        padding:12px;
                        border-radius:10px;
                        margin-bottom:10px;
                        border-left:6px solid #4a6cf7;
                        font-weight:500;
                        color:#222">
                        {task["Task"]}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

else:
    st.info("No tasks available yet.")