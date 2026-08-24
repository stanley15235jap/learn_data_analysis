import streamlit as st
from core.auth import (
    bootstrap_app,
    list_users,
    create_user,
    username_exists,
    set_user_status,
    reset_password,
)
from core.ui import render_sidebar

st.set_page_config(page_title="帳號管理 | 學習工作台", page_icon="🔑", layout="wide")
user = bootstrap_app()
render_sidebar(user)

st.title("🔑 帳號管理")

if user["role"] != "admin":
    st.error("只有管理員可以使用這個頁面。")
    st.stop()

st.caption("目前帳號只能由管理員建立,停用帳號不會刪除該帳號的任何學習進度,重新啟用即可接回原本紀錄。")

st.markdown("### 新增帳號")
with st.form("create_user_form", clear_on_submit=True):
    c1, c2, c3 = st.columns([2, 2, 1])
    new_username = c1.text_input("帳號")
    new_password = c2.text_input("初始密碼", type="password")
    new_role = c3.selectbox("角色", ["user", "admin"], format_func=lambda r: "管理員" if r == "admin" else "一般帳號")
    submitted = st.form_submit_button("建立帳號", type="primary")

if submitted:
    if not new_username or not new_password:
        st.error("帳號與密碼不能空白。")
    elif username_exists(new_username):
        st.error(f"帳號「{new_username}」已經存在。")
    else:
        create_user(new_username, new_password, role=new_role, status="active")
        st.success(f"已建立帳號「{new_username}」。")
        st.rerun()

st.markdown("---")
st.markdown("### 所有帳號")

users = list_users()
for u in users:
    is_self = u["id"] == user["id"]
    status_label = "🟢 使用中" if u["status"] == "active" else "⚪ 已停用"
    role_label = "管理員" if u["role"] == "admin" else "一般帳號"
    title = f"{status_label}　**{u['username']}**　`{role_label}`" + ("　(目前登入)" if is_self else "")

    with st.expander(title):
        st.caption(f"建立時間:{u['created_at']}")

        rc1, rc2 = st.columns([3, 1])
        new_pw = rc1.text_input("重設密碼", type="password", key=f"pw_{u['id']}", label_visibility="collapsed", placeholder="輸入新密碼")
        if rc2.button("重設密碼", key=f"reset_{u['id']}", use_container_width=True):
            if not new_pw:
                st.error("請輸入新密碼。")
            else:
                reset_password(u["id"], new_pw)
                st.success("密碼已更新。")
                st.rerun()

        if u["status"] == "active":
            if is_self:
                st.caption("無法停用目前登入中的帳號。")
            elif st.button("停用這個帳號", key=f"disable_{u['id']}"):
                set_user_status(u["id"], "disabled")
                st.success(f"已停用「{u['username']}」,學習進度資料保留,可隨時重新啟用。")
                st.rerun()
        else:
            if st.button("重新啟用這個帳號", key=f"enable_{u['id']}", type="primary"):
                set_user_status(u["id"], "active")
                st.success(f"已重新啟用「{u['username']}」。")
                st.rerun()
