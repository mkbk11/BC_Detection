import streamlit as st
import mysql.connector
import hashlib

# 初始化会话状态
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False


# 连接到 MySQL 数据库
def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="",  # Your MySQL password
        database="account_fire"  # Database name
    )
    return conn


# 哈希密码
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# 获取所有用户的姓名和对应的账号
def get_all_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT account, name FROM login_information')
    users = cursor.fetchall()
    conn.close()
    return users  # 返回[(账号, 姓名), (账号, 姓名), ...]


# 查看所有用户
def view_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM login_information')
    users = cursor.fetchall()
    conn.close()

    if users:
        st.write("### 用户信息列表")
        for user in users:
            st.write(
                f"**账号:** {user[1]} | **姓名:** {user[3]} | **性别:** {user[4]} | **邮箱:** {user[5]} | **角色:** {'管理员' if user[6] == 1 else '普通用户'}")
    else:
        st.warning("当前没有用户信息。")


# 修改用户信息
def modify_user():
    st.title("修改用户信息")

    users = get_all_users()  # 获取所有用户姓名和账号
    user_names = [user[1] for user in users]  # 获取所有姓名
    selected_name = st.selectbox("选择要修改的用户", user_names)  # 显示姓名作为选择项

    # 获取选中的用户名对应的账号
    selected_user_account = next(user[0] for user in users if user[1] == selected_name)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM login_information WHERE account = %s', (selected_user_account,))
    user = cursor.fetchone()
    conn.close()

    if user:
        st.write(f"### 修改用户: {user[3]}")
        new_name = st.text_input("新姓名", user[3])
        new_email = st.text_input("新邮箱", user[5])
        new_sex = st.selectbox("新性别", ["男", "女", "其他"], index=["男", "女", "其他"].index(user[4]))
        new_role = st.selectbox("新角色", ["普通用户", "管理员"], index=0 if user[6] == 0 else 1)

        if st.button("保存修改"):
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE login_information SET name = %s, email = %s, sex = %s, is_admin = %s WHERE account = %s',
                (new_name, new_email, new_sex, 1 if new_role == "管理员" else 0, selected_user_account))
            conn.commit()
            conn.close()
            st.success("用户信息已更新！")
    else:
        st.error("未找到该用户！")


# 删除用户
def delete_user():
    st.title("删除用户")

    users = get_all_users()  # 获取所有用户姓名和账号
    user_names = [user[1] for user in users]  # 获取所有姓名
    selected_name = st.selectbox("选择要删除的用户", user_names)  # 显示姓名作为选择项

    # 获取选中的用户名对应的账号
    selected_user_account = next(user[0] for user in users if user[1] == selected_name)

    if st.button("删除用户"):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM login_information WHERE account = %s', (selected_user_account,))
        user = cursor.fetchone()

        if user:
            cursor.execute('DELETE FROM login_information WHERE account = %s', (selected_user_account,))
            conn.commit()
            st.success(f"用户 {selected_name} 已删除！")
        else:
            st.error("未找到该用户！")
        conn.close()


# 添加新用户
def add_user():
    st.title("添加新用户")

    new_username = st.text_input("用户名")
    new_name = st.text_input("姓名")
    new_email = st.text_input("邮箱")
    new_sex = st.selectbox("性别", ["男", "女", "其他"])
    new_role = st.selectbox("角色", ["普通用户", "管理员"])
    new_password = st.text_input("密码", type="password")

    if st.button("添加用户"):
        if new_username and new_password and new_name and new_email:
            hashed_password = hash_password(new_password)

            conn = get_db_connection()
            cursor = conn.cursor()
            try:
                cursor.execute(
                    'INSERT INTO login_information (account, password, name, sex, email, is_admin) VALUES (%s, %s, %s, %s, %s, %s)',
                    (new_username, hashed_password, new_name, new_sex, new_email, 1 if new_role == "管理员" else 0))
                conn.commit()
                st.success(f"用户 {new_name} 添加成功！")
            except mysql.connector.IntegrityError:
                st.error("该用户名已存在，请选择其他用户名。")
            finally:
                conn.close()
        else:
            st.warning("请填写所有字段。")


# 管理员设置页面
def admin_settings():
    st.title("管理员设置页面")

    st.write("选择操作：")

    option = st.selectbox("请选择要执行的操作", ["查看所有用户", "修改用户信息", "删除用户", "添加新用户"])

    if option == "查看所有用户":
        view_users()
    elif option == "修改用户信息":
        modify_user()
    elif option == "删除用户":
        delete_user()
    elif option == "添加新用户":
        add_user()


# 登录后，显示管理员设置页面
if st.session_state.logged_in and st.session_state.is_admin:
    admin_settings()
else:
    st.error("请先登录管理员账号！")
