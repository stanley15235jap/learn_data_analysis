"""帳號系統:密碼雜湊、登入驗證、帳號管理(CRUD)、Streamlit 登入閘門。

設計依據見「帳號系統設計說明」:
- 密碼一律以 PBKDF2-HMAC-SHA256 雜湊儲存,不存明碼(core.auth 內部)。
- 刪除帳號採「停用」而非硬刪除,底下進度資料完整保留(core.db 的 user_id 外鍵不受影響)。
- 帳號建立目前僅開放管理員操作,但建立邏輯(create_user)本身與呼叫者身份無關,
  未來要加開放註冊頁面,直接呼叫 create_user 即可,不需要重構。
"""
import hashlib
import hmac
import secrets

import streamlit as st

from core.db import get_conn, now_iso

PBKDF2_ITERATIONS = 200_000


def _hash_password(password: str, salt: bytes = None) -> str:
    salt = salt or secrets.token_bytes(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, PBKDF2_ITERATIONS)
    return salt.hex() + ":" + dk.hex()


def _verify_password(password: str, stored_hash: str) -> bool:
    try:
        salt_hex, dk_hex = stored_hash.split(":")
    except ValueError:
        return False
    salt = bytes.fromhex(salt_hex)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, PBKDF2_ITERATIONS)
    return hmac.compare_digest(dk.hex(), dk_hex)


# ---------- 帳號 CRUD(供管理員頁面 / 未來註冊頁面共用) ----------

def any_users_exist() -> bool:
    conn = get_conn()
    row = conn.execute("SELECT COUNT(*) c FROM users").fetchone()
    conn.close()
    return row["c"] > 0


def username_exists(username: str) -> bool:
    conn = get_conn()
    row = conn.execute("SELECT id FROM users WHERE username=?", (username,)).fetchone()
    conn.close()
    return row is not None


def create_user(username: str, password: str, role: str = "user", status: str = "active"):
    """建立帳號。不論由管理員頁面或未來的自助註冊頁面呼叫,都是同一份邏輯。"""
    conn = get_conn()
    conn.execute(
        "INSERT INTO users (username, password_hash, role, status, created_at) VALUES (?,?,?,?,?)",
        (username, _hash_password(password), role, status, now_iso()),
    )
    conn.commit()
    conn.close()


def get_user_by_username(username: str):
    conn = get_conn()
    row = conn.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
    conn.close()
    return row


def get_user_by_id(user_id: int):
    conn = get_conn()
    row = conn.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()
    conn.close()
    return row


def list_users():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM users ORDER BY created_at").fetchall()
    conn.close()
    return rows


def set_user_status(user_id: int, status: str):
    """status: 'active' 或 'disabled'。停用不會刪除該帳號的任何學習進度資料。"""
    conn = get_conn()
    conn.execute("UPDATE users SET status=? WHERE id=?", (status, user_id))
    conn.commit()
    conn.close()


def reset_password(user_id: int, new_password: str):
    conn = get_conn()
    conn.execute("UPDATE users SET password_hash=? WHERE id=?", (_hash_password(new_password), user_id))
    conn.commit()
    conn.close()


def authenticate(username: str, password: str):
    """回傳使用者 row(驗證成功且帳號為 active),否則回傳 None。"""
    row = get_user_by_username(username)
    if row is None:
        return None
    if row["status"] != "active":
        return None
    if not _verify_password(password, row["password_hash"]):
        return None
    return row


# ---------- Streamlit 登入閘門 ----------

def current_user():
    """回傳目前登入者的 user row,未登入則回傳 None。"""
    user_id = st.session_state.get("user_id")
    if user_id is None:
        return None
    row = get_user_by_id(user_id)
    if row is None or row["status"] != "active":
        st.session_state.pop("user_id", None)
        return None
    return row


def logout():
    st.session_state.pop("user_id", None)


def require_login():
    """放在每個頁面最上方。已登入回傳 user row;未登入則顯示登入畫面並中止本次渲染。"""
    user = current_user()
    if user is not None:
        return user

    if not any_users_exist():
        _render_bootstrap_form()
    else:
        _render_login_form()
    st.stop()


def _render_login_form():
    st.title("🔐 登入")
    st.caption("數據分析學習工作台 — 請先登入才能開始學習。")
    with st.form("login_form"):
        username = st.text_input("帳號")
        password = st.text_input("密碼", type="password")
        submitted = st.form_submit_button("登入", type="primary")
    if submitted:
        user = authenticate(username, password)
        if user is None:
            st.error("帳號或密碼錯誤,或此帳號已被停用。")
        else:
            st.session_state["user_id"] = user["id"]
            st.rerun()


def _render_bootstrap_form():
    st.title("🔐 初始設定")
    st.caption("這是這個工作台第一次啟動,請先建立你的管理員帳號。")
    with st.form("bootstrap_form"):
        username = st.text_input("設定管理員帳號")
        password = st.text_input("設定密碼", type="password")
        confirm = st.text_input("再輸入一次密碼", type="password")
        submitted = st.form_submit_button("建立管理員帳號並登入", type="primary")
    if submitted:
        if not username or not password:
            st.error("帳號與密碼不能空白。")
        elif password != confirm:
            st.error("兩次輸入的密碼不一致。")
        elif username_exists(username):
            st.error("這個帳號已經存在。")
        else:
            create_user(username, password, role="admin", status="active")
            user = get_user_by_username(username)
            st.session_state["user_id"] = user["id"]
            st.rerun()
