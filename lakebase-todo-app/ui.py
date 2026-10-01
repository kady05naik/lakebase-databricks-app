import streamlit as st
from db import get_todos, toggle_todo, delete_todo


@st.fragment
def display_todos():
    st.subheader("Your Todos")

    todos = get_todos()

    if not todos:
        st.info("No todos yet! Add one above to get started.")
    else:
        for todo_id, task, completed, created_at in todos:
            col1, col2, col3 = st.columns([0.1, 0.7, 0.2])

            with col1:
                if st.checkbox("", value=completed, key=f"check_{todo_id}"):
                    if not completed:
                        toggle_todo(todo_id)
                        st.rerun(scope="fragment")
                elif completed:
                    toggle_todo(todo_id)
                    st.rerun(scope="fragment")

            with col2:
                st.markdown(f"~~{task}~~" if completed else task)
                st.caption(f"Created: {created_at.strftime('%Y-%m-%d %H:%M')}")

            with col3:
                if st.button("Delete", key=f"delete_{todo_id}"):
                    delete_todo(todo_id)
                    st.rerun(scope="fragment")
