import streamlit as st
import pandas as pd
import random

# 讀取日本小知識 CSV
def load_japan_facts(csv_path="data/japan_facts.csv"):
    try:
        df = pd.read_csv(csv_path)
        facts = df["fact"].dropna().tolist()
        return facts
    except Exception as e:
        st.error(f"讀取日本小知識失敗：{e}")
        return []

def show_home():
    st.title("歡迎來到畢業旅行網站")
    st.write("請選擇你想進入的功能：")

    # ---------------------------
    # 網站使用說明 Text Box
    # ---------------------------
    st.markdown("## 📘 網站使用說明")
    usage_text = """
1. 【行程】
   可以查看旅遊行程安排，幫助大家掌握每天要去哪裡、做什麼。

2. 【記帳】
   可以記錄旅行中的花費，方便大家統整每個人的支出。
   記帳功能可能會突然資料消失。

3. 【行前準備】
   可以確認出發前需要攜帶或完成的事項，例如護照、行李、票券等。

4. 【日本小知識】
   每次回到首頁都可以抽一則日本小知識，增加旅遊樂趣！
"""
    st.text_area("使用說明", usage_text, height=220, disabled=True)

    # ---------------------------
    # 功能按鈕
    # ---------------------------
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("行程", use_container_width=True):
            st.session_state.page = "trip"
            st.rerun()

    with col2:
        if st.button("記帳", use_container_width=True):
            st.session_state.page = "expenses"
            st.rerun()

    with col3:
        if st.button("行前準備", use_container_width=True):
            st.session_state.page = "checklist"
            st.rerun()

    st.markdown("---")

    # ---------------------------
    # 日本小知識區塊
    # ---------------------------
    st.markdown("## 🎌 抽一個日本小知識")

    facts = load_japan_facts()

    if "current_fact" not in st.session_state:
        if facts:
            st.session_state.current_fact = random.choice(facts)
        else:
            st.session_state.current_fact = "目前沒有可顯示的小知識。"

    col_fact, col_btn = st.columns([4, 1])

    with col_fact:
        st.text_area(
            "今日小知識",
            st.session_state.current_fact,
            height=120,
            disabled=True
        )

    with col_btn:
        if st.button("🎲 Reroll", use_container_width=True):
            if facts:
                st.session_state.current_fact = random.choice(facts)
            else:
                st.session_state.current_fact = "目前沒有可顯示的小知識。"
            st.rerun()