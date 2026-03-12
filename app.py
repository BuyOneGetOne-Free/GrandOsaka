import streamlit as st
from router import show_page

st.set_page_config(
    page_title="日本畢業旅行網站",
    page_icon="✈️",
    layout="centered"
)

show_page()