import streamlit as st
import mysql.connector
from mysql.connector import Error
import pandas as pd
from PIL import Image
import io
import time

# 获取数据库连接
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="",  # MySQL密码
            database="account_fire"  # 数据库名称
        )
        return conn
    except Error as e:
        st.error(f"无法连接到数据库: {e}")
        return None

# 查询当前用户的历史记录
def fetch_user_history(username):
    conn = get_db_connection()
    if conn is None:
        return None

    try:
        cursor = conn.cursor()
        table_name = f"data_{username}"  # 根据用户名动态生成表名
        query = f"SELECT id, name, type, class_name, confidence, data FROM {table_name}"
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows
    except Error as e:
        st.error(f"查询历史记录失败: {e}")
        return None
    finally:
        conn.close()

# 历史记录查询页面
def history_page():
    st.title("📜 历史记录查询")
    st.markdown("---")  # 分隔线

    # 检查用户是否登录
    if "username" not in st.session_state or not st.session_state.username:
        st.warning("请先登录以查看历史记录。")
        return

    # 获取当前用户名
    username = st.session_state.username
    st.subheader(f"当前用户: {username}")

    # 查询历史记录
    history_data = fetch_user_history(username)
    if not history_data:
        st.info("没有找到历史记录。")
        return

    # 将历史记录转换为 DataFrame
    df = pd.DataFrame(history_data, columns=["ID", "名称", "类型", "类别", "置信度", "数据"])
    st.dataframe(df[["ID", "名称", "类型", "类别", "置信度"]])  # 显示基本信息

    # 显示详细信息
    st.markdown("### 📊 详细信息")
    selected_id = st.selectbox("选择记录 ID", df["ID"].tolist())

    # 获取选中的记录
    selected_record = df[df["ID"] == selected_id].iloc[0]

    # 显示记录详情
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 基本信息")
        st.write(f"**ID**: {selected_record['ID']}")
        st.write(f"**名称**: {selected_record['名称']}")
        st.write(f"**类型**: {selected_record['类型']}")
        st.write(f"**类别**: {selected_record['类别']}")
        st.write(f"**置信度**: {selected_record['置信度']:.2f}")

    with col2:
        st.markdown("#### 数据预览")
        # 解码数据
        data = selected_record["数据"]
        if data:
            try:
                if selected_record["类型"] == "图像":
                    # 如果是图像数据
                    image = Image.open(io.BytesIO(data))
                    st.image(image, caption="数据图像", use_container_width=True)
                elif selected_record["类型"] == "视频":
                    # 如果是视频数据
                    st.video(data, format="video/mp4")
                else:
                    st.warning("不支持的数据类型。")
            except Exception as e:
                st.error(f"无法加载数据: {e}")
        else:
            st.warning("没有可用的数据。")

    # 等待5秒后刷新页面
    time.sleep(5)  # 5秒刷新一次
    st.empty()  # 清空容器，重新渲染页面内容

# 运行历史记录查询页面
history_page()