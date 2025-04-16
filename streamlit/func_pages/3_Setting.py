import streamlit as st


def setting_page():
    st.title("设置页面")
    st.markdown("## 欢迎来到账户设置中心")
    st.write("在这里，您可以修改您的个人信息、密码、通知设置等。")

    # 显示当前登录用户信息
    if "username" in st.session_state:
        st.markdown(f"### 当前用户: {st.session_state.username}")
    else:
        st.warning("未登录用户")

    # 添加一个分隔线
    st.markdown("---")

    # 修改密码功能
    st.subheader("🔒 修改密码")
    current_password = st.text_input("当前密码", type="password", placeholder="请输入当前密码")
    new_password = st.text_input("新密码", type="password", placeholder="请输入新密码")
    confirm_password = st.text_input("确认新密码", type="password", placeholder="请再次输入新密码")

    if st.button("保存新密码"):
        if new_password == confirm_password:
            # 这里可以添加密码验证和更新逻辑
            st.success("密码修改成功！")
        else:
            st.error("新密码和确认密码不匹配！")

    # 添加一个分隔线
    st.markdown("---")

    # 主题切换功能
    st.subheader("🎨 主题设置")
    theme = st.selectbox("选择主题", ["浅色模式", "深色模式"])

    if theme == "深色模式":
        st.write("已切换至深色模式")
        # 这里可以添加主题切换的逻辑
        # 使用 CSS 或自定义样式表设置深色模式
        st.markdown("<style>body {background-color: #121212; color: white;}</style>", unsafe_allow_html=True)
    else:
        st.write("已切换至浅色模式")
        # 这里可以添加主题切换的逻辑
        # 使用 CSS 或自定义样式表设置浅色模式
        st.markdown("<style>body {background-color: white; color: black;}</style>", unsafe_allow_html=True)

    # 添加一个分隔线
    st.markdown("---")

    # 通知设置功能
    st.subheader("🔔 通知设置")
    email_notifications = st.checkbox("接收邮件通知", value=True)
    push_notifications = st.checkbox("接收推送通知", value=True)

    if st.button("保存通知设置"):
        # 这里可以添加保存通知设置的逻辑
        st.success("通知设置已保存！")

    # 添加退出登录按钮
    st.markdown("---")
    if st.button("退出登录"):
        st.session_state.logged_in = False  # 设置登录状态为 False
        st.session_state.pop("username", None)  # 清除用户名
        st.success("已退出登录！")
        st.experimental_set_query_params(logout=True)  # 强制刷新页面
        st.rerun()  # 重新运行应用以跳转到登录页面


# 运行设置页面
setting_page()
