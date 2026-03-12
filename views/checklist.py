import streamlit as st
import pandas as pd
import os
def show_checklist_page():
    st.title("歡迎進入行前準備")


DATA_PATH = "data/checklist.csv"


def load_checklist():
    if not os.path.exists(DATA_PATH):
        df = pd.DataFrame(columns=["item"])
        df.to_csv(DATA_PATH, index=False, encoding="utf-8-sig")

    df = pd.read_csv(DATA_PATH)
    df.columns = df.columns.str.strip()
    return df


def show_checklist_page():
    st.title("行前準備")

    if st.button("回首頁"):
        st.session_state.page = "home"
        st.rerun()

    st.markdown("## 🧳 出發前確認清單")

    df = load_checklist()

    total_items = len(df)
    checked_count = 0

    for i, row in df.iterrows():
        item = row["item"]

        checked = st.checkbox(
            item,
            key=f"check_{i}"
        )

        if checked:
            checked_count += 1

    # ---------- 進度 ----------
    st.markdown("---")
    st.markdown("### 📊 準備進度")

    progress = checked_count / total_items if total_items > 0 else 0
    st.progress(progress)

    st.write(f"完成度：{checked_count} / {total_items}")

    # ---------- 完成動畫 ----------
    if total_items > 0 and checked_count == total_items:
        st.success("🎉 準備完成！可以安心出發囉～")
        st.balloons()