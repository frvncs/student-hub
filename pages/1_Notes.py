import streamlit as st
from streamlit_quill import st_quill
from datetime import datetime
from database import get_db_connection

if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Please log in to access Notes.")
    st.stop()

st.set_page_config(page_title="Notes", layout="wide")

user_id = st.session_state.user["id"]

def load_notes():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, title, content, type, pinned, date, archived
        FROM notes
        WHERE user_id=?
        ORDER BY pinned DESC, date DESC
    """, (user_id,))

    notes = [{
        "id": n[0],
        "title": n[1],
        "content": n[2],
        "type": n[3],
        "pinned": bool(n[4]),
        "date": n[5],
        "archived": bool(n[6])
    } for n in cursor.fetchall()]

    conn.close()
    return notes

def save_note_to_db(title, content, note_type, pinned):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO notes (user_id, title, content, type, pinned, date, archived)
        VALUES (?, ?, ?, ?, ?, ?, 0)
    """, (
        user_id,
        title,
        content,
        note_type,
        int(pinned),
        datetime.now().strftime("%Y-%m-%d")
    ))

    conn.commit()
    conn.close()

def update_note(note_id, content):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE notes
        SET content=?
        WHERE id=? AND user_id=?
    """, (content, note_id, user_id))

    conn.commit()
    conn.close()

def archive_note(note_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE notes
        SET archived=1
        WHERE id=? AND user_id=?
    """, (note_id, user_id))

    conn.commit()
    conn.close()

def restore_note(note_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE notes
        SET archived=0
        WHERE id=? AND user_id=?
    """, (note_id, user_id))

    conn.commit()
    conn.close()

if "page" not in st.session_state:
    st.session_state.page = "home"

if "edit_note" not in st.session_state:
    st.session_state.edit_note = None

st.sidebar.title("✎ Notes")

if st.sidebar.button("Your Notes"):
    st.session_state.page = "home"

if st.sidebar.button("Add Note"):
    st.session_state.page = "create"

if st.sidebar.button("Archived"):
    st.session_state.page = "archive"

if st.session_state.page == "home":

    st.title("Your Notes")

    notes = load_notes()

    search = st.text_input("Search notes")
    filter_option = st.selectbox("Filter", ["All", "Lectures", "Exam", "Personal"])

    st.divider()

    filtered = [
        n for n in notes
        if not n["archived"]
        and search.lower() in n["title"].lower()
        and (filter_option == "All" or n["type"] == filter_option)
    ]

    if not filtered:
        st.info("No notes yet.")
    else:
        cols = st.columns(3)

        for i, note in enumerate(filtered):

            with cols[i % 3]:

                if st.button(note["title"], key=f"note_{note['id']}", use_container_width=True):
                    st.session_state.edit_note = note
                    st.session_state.page = "edit"
                    st.rerun()

                if st.button("Archive", key=f"archive_{note['id']}"):
                    archive_note(note["id"])
                    st.success("Note archived")
                    st.rerun()

elif st.session_state.page == "create":

    st.title("Create Note")

    with st.form("note_form"):

        title = st.text_input("Title")

        note_type = st.selectbox(
            "Type",
            ["Lectures", "Exam", "Personal"]
        )

        pinned = st.checkbox("Pin this note")

        content = st_quill()

        save = st.form_submit_button("Save Note")

        if save:

            if not title:
                st.warning("Title required")
            else:
                save_note_to_db(title, content, note_type, pinned)

                st.success("Note saved!")

                st.session_state.page = "home"
                st.rerun()

elif st.session_state.page == "edit":

    note = st.session_state.edit_note

    st.title(note["title"])

    content = st_quill(value=note["content"])

    if st.button("Update Note"):

        update_note(note["id"], content)

        st.success("Note updated!")

        st.session_state.page = "home"
        st.rerun()

elif st.session_state.page == "archive":

    st.title("Archived Notes")

    notes = load_notes()

    archived = [n for n in notes if n["archived"]]

    if not archived:
        st.info("No archived notes")

    else:

        for note in archived:

            st.markdown(
                f"""
                <div style="padding:20px;border-radius:12px;margin-bottom:10px;background:#f5f5f5;">
                <b>{note['title']}</b><br>
                {note['date']}
                </div>
                """,
                unsafe_allow_html=True
            )

            if st.button("Restore", key=f"restore_{note['id']}"):

                restore_note(note["id"])

                st.success("Restored!")

                st.rerun()