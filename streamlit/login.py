import streamlit as st
import re

# 初始化会话状态
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

# # Set page config, hide sidebar
# st.set_page_config(page_title="登录", layout="centered")

# 简化后不需要数据库连接和验证函数


# 简化的重置密码功能
def reset_password():
    st.title("重置密码")

    email = st.text_input("请输入邮箱地址")

    if st.button("重置密码"):
        st.success("密码重置链接已发送到您的邮箱！")

    # 返回登录按钮
    if st.button("返回登录"):
        st.session_state.page = "login"  # 设置页面状态为 "login"
        st.rerun()  # 重新加载界面并跳转回登录页面


# 简化的登录功能
def login():
    # 登录界面
    st.title("登录界面")

    # 登录选择普通用户或管理员
    login_type = st.radio("请选择登录身份", ("普通用户", "管理员"))

    # 简化的登录按钮
    if st.button("一键登录"):
        is_admin = (login_type == "管理员")  # 根据选择决定是否是管理员
        
        # 设置默认用户名
        default_username = "12345678910" if is_admin else "13800138000"
        
        # 直接设置登录状态
        st.session_state.logged_in = True
        st.session_state.username = default_username
        st.session_state.is_admin = is_admin  # 记录是否为管理员
        st.success(f"{login_type} 登录成功！")
        st.rerun()  # 重新加载应用以跳转到主页面

    # Register button to navigate to the register page
    if st.button("注册新账号"):
        st.session_state.page = "register"
        st.rerun()  # Jump to the registration page

    # Forgot password button
    if st.button("忘记密码"):
        st.session_state.page = "reset_password"
        st.rerun()  # Jump to reset password page


# 简化的注册页面功能
def register():
    st.title("注册界面")

    # 简化的注册按钮
    if st.button("一键注册"):
        st.success("注册成功！")
        st.session_state.page = "login"
        st.rerun()  # 注册后跳转回登录页面

    # Return to login button
    if st.button("返回登录"):
        st.session_state.page = "login"
        st.rerun()  # Jump back to login page


# 退出登录功能
def logout():
    if st.button("退出登录"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.success("已退出登录！")
        st.rerun()  # Re-run the app to jump to the login page


# 页面导航设置
page1 = st.Page("func_pages/1_About.py", title="关于")
page2 = st.Page("func_pages/2_object_detection.py", title="目标检测")
page3 = st.Page("func_pages/3_Setting.py", title="设置")
page4 = st.Page("func_pages/Setting_administer.py", title="管理员设置")
page5 = st.Page("func_pages/history.py", title="历史记录查询")
login_page = st.Page(login, title="登录")
logout_page = st.Page(logout, title="退出登录")

# 默认，只有登录页面可用
pg = st.navigation([login_page])

# 登录后，显示其他页面

# 登录后，显示不同页面内容
if st.session_state.logged_in:
    if st.session_state.is_admin:
        pg = st.navigation(
            {
                "管理功能": [page1, page2],  # 管理员可访问所有功能
                "账户管理": [page4, logout_page]
            }
        )
    else:
        pg = st.navigation(
            {
                "主要功能": [page1, page2],  # 普通用户可访问部分功能
                "账户管理": [page3, logout_page]
            }
        )


# 根据页面状态决定显示哪个页面
if st.session_state.get("page", "login") == "register":
    register()
elif st.session_state.get("page", "login") == "reset_password":
    reset_password()
else:
    pg.run()
