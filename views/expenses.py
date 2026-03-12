import streamlit as st
import pandas as pd
import os
def show_expenses_page():
    st.title("歡迎進入記帳")

DATA_DIR = "data"
USERS = ["A", "B", "C", "D", "E"]

COLUMNS = ["date", "category", "description", "amount"]


# ---------- 工具函式 ----------
def get_user_file(user):
    return os.path.join(DATA_DIR, f"{user}_expenses.csv")


def load_user_data(user):
    path = get_user_file(user)

    if not os.path.exists(path):
        df = pd.DataFrame(columns=COLUMNS)
        df.to_csv(path, index=False, encoding="utf-8-sig")

    df = pd.read_csv(path)
    return df

def load_users():
    df = pd.read_csv("data/users.csv")
    df.columns = df.columns.str.strip()
    return df

def save_user_data(user, df):
    path = get_user_file(user)
    df.to_csv(path, index=False, encoding="utf-8-sig")


# ---------- 主頁面 ----------
def show_expenses_page():
    st.title("歡迎進入記帳")

    if st.button("回首頁"):
        st.session_state.page = "home"
        st.rerun()

    st.markdown("## 👤 選擇你的身分")

    users_df = load_users()
    cols = st.columns(len(users_df))

    for i, row in users_df.iterrows():
        user_id = row["user_id"]
        name = row["name"]

        with cols[i]:
            if st.button(name, use_container_width=True):
                st.session_state.selected_user = user_id
                st.session_state.selected_user_name = name
                st.rerun()

    user = st.session_state.get("selected_user", None)
    user_name = st.session_state.get("selected_user_name", None)

    if not user:
        st.info("請先選擇身分")
        return

    st.markdown("---")
    st.header(f"🧾 {user_name} 的記帳本")

    # ---------- 預算區 ----------
    st.markdown("### 💰 預算設定")

    budget = st.number_input(
        "請輸入你的總預算",
        min_value=0,
        step=1000,
        value=0
    )

    # ---------- 表格區 ----------
    st.markdown("### ✏️ 記帳明細")

    df = load_user_data(user)

    edited_df = st.data_editor(
        df,
        num_rows="dynamic",
        use_container_width=True,
        key=f"{user}_editor"
    )

    if st.button("💾 儲存記帳資料", use_container_width=True):
        save_user_data(user, edited_df)
        st.success("已儲存")

    # ---------- 統計區 ----------
    st.markdown("---")
    st.markdown("### 📊 花費統計")

    if not edited_df.empty:
        # 金額轉數字
        edited_df["amount"] = pd.to_numeric(edited_df["amount"], errors="coerce").fillna(0)

        total_spent = edited_df["amount"].sum()
        remaining = budget - total_spent

        col1, col2 = st.columns(2)

        with col1:
            st.metric("總花費", f"¥ {int(total_spent)}")

        with col2:
            st.metric("剩餘預算", f"¥ {int(remaining)}")

        st.markdown("### 📅 每日花費")

        daily = edited_df.groupby("date")["amount"].sum().reset_index()

        st.dataframe(
            daily.rename(columns={
                "date": "日期",
                "amount": "當日花費"
            }),
            use_container_width=True
        )

    else:
        st.info("尚未有記帳資料")