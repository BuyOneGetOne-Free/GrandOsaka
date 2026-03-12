import streamlit as st
import pandas as pd
import os
import urllib.parse

DATA_PATH = "data/activities.csv"

SEGMENT_LABELS = {
    "morning": "早上",
    "noon": "中午",
    "afternoon": "下午",
    "night": "晚上"
}

DAY_TITLES = {
    "6/29": "6/29 行程",
    "6/30": "6/30 行程",
    "7/1": "7/1 行程",
    "7/2": "7/2 行程",
    "7/3": "7/3 行程"
}


def load_activities():
    if not os.path.exists(DATA_PATH):
        return pd.DataFrame(columns=[
            "date", "segment", "order", "title",
            "detail", "start_time", "end_time",
            "link", "map_query"
        ])

    df = pd.read_csv(DATA_PATH)

    # 避免欄位名稱前後有空白
    df.columns = df.columns.str.strip()

    # 如果缺少欄位，自動補上
    required_cols = [
        "date", "segment", "order", "title",
        "detail", "start_time", "end_time",
        "link", "map_query"
    ]
    for col in required_cols:
        if col not in df.columns:
            df[col] = ""

    # order 轉成數字方便排序
    df["order"] = pd.to_numeric(df["order"], errors="coerce")

    # 文字欄位清理
    text_cols = ["date", "segment", "title", "detail", "start_time", "end_time", "link", "map_query"]
    for col in text_cols:
        df[col] = df[col].fillna("").astype(str).str.strip()

    return df


def build_google_maps_url(row):
    """
    優先使用 CSV 裡的 link。
    如果沒有 link，就用 map_query 或 title 自動組 Google Maps 搜尋連結。
    """
    link = row.get("link", "")
    map_query = row.get("map_query", "")
    title = row.get("title", "")

    if link:
        return link

    keyword = map_query if map_query else title
    if keyword:
        encoded = urllib.parse.quote(keyword)
        return f"https://www.google.com/maps/search/?api=1&query={encoded}"

    return ""



def render_segment_schedule(day_df, segment_key):
    segment_df = day_df[day_df["segment"] == segment_key].copy()

    if segment_df.empty:
        st.info(f"目前沒有{SEGMENT_LABELS[segment_key]}行程")
        return

    segment_df = segment_df.sort_values(by="order", na_position="last")

    for _, row in segment_df.iterrows():
        title = row.get("title", "")
        detail = row.get("detail", "")
        start_time = row.get("start_time", "")
        end_time = row.get("end_time", "")
        map_url = build_google_maps_url(row)

        with st.container(border=True):
            st.subheader(title if title else "未命名行程")

            if start_time or end_time:
                if start_time and end_time:
                    st.write(f"**時間：** {start_time} ~ {end_time}")
                elif start_time:
                    st.write(f"**開始時間：** {start_time}")
                elif end_time:
                    st.write(f"**結束時間：** {end_time}")

            if detail:
                st.write(f"**內容：** {detail}")

            if map_url:
                col1, col2 = st.columns([1, 2])

                with col1:
                    st.link_button("開啟 Google Maps", map_url, use_container_width=True)

                with col2:
                    st.caption("地圖預覽")

            else:
                st.caption("此行程尚未設定地圖資訊")


def show_trip_page():
    st.title("歡迎進入行程")

    if st.button("回首頁"):
        st.session_state.page = "home"
        st.rerun()

    df = load_activities()

    day_list = ["6/29", "6/30", "7/1", "7/2", "7/3"]

    st.subheader("請選擇日期")
    cols = st.columns(len(day_list))

    if "selected_trip_day" not in st.session_state:
        st.session_state.selected_trip_day = "6/29"

    for i, day in enumerate(day_list):
        with cols[i]:
            if st.button(day, use_container_width=True):
                st.session_state.selected_trip_day = day
                st.rerun()

    selected_day = st.session_state.selected_trip_day

    st.markdown("---")
    st.header(DAY_TITLES.get(selected_day, f"{selected_day} 行程"))

    day_df = df[df["date"].astype(str).str.strip() == selected_day].copy()

    if day_df.empty:
        st.warning(f"{selected_day} 目前沒有行程資料")
        return

    tab1, tab2, tab3, tab4 = st.tabs(["早上", "中午", "下午", "晚上"])

    with tab1:
        render_segment_schedule(day_df, "morning")

    with tab2:
        render_segment_schedule(day_df, "noon")

    with tab3:
        render_segment_schedule(day_df, "afternoon")

    with tab4:
        render_segment_schedule(day_df, "night")