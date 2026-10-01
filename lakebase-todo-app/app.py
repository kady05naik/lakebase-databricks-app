import streamlit as st
from db import init_database, add_todo
from ui import display_todos


def main():
    st.set_page_config(
        page_title="Todo List App",
        page_icon="",
        layout="wide"
    )

    st.title("Todo List App")
    st.markdown("---")

    # Initialize database on startup
    if not init_database():
        st.stop()

    # Add new todo form
    st.subheader("Add New Todo")
    with st.form("add_todo_form", clear_on_submit=True):
        new_task = st.text_input("Enter a new task:", placeholder="What do you need to do?")
        submitted = st.form_submit_button("Add Todo", type="primary")

        if submitted and new_task.strip():
            if add_todo(new_task.strip()):
                st.success("Todo added successfully!")

    st.markdown("---")
    display_todos()


if __name__ == "__main__":
    main()
