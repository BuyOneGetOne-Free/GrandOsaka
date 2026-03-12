import streamlit as st
from views.home import show_home
from views.day import show_trip_page
from views.expenses import show_expenses_page
from views.checklist import show_checklist_page

def show_page():
    if "page" not in st.session_state:
        st.session_state.page = "home"

    if st.session_state.page == "home":
        show_home()
    elif st.session_state.page == "trip":
        show_trip_page()
    elif st.session_state.page == "expenses":
        show_expenses_page()
    elif st.session_state.page == "checklist":
        show_checklist_page()