import streamlit as st
from core.db import init_db
from core.auth import require_login
from core.content_loader import all_units_in_order
from core.executor import run_code
from core.ui import render_sidebar, code_editor

st.set_page_config(page_title="實作區 | 學習工作台", page_icon="💻", layout="wide")
init_db()
user = require_login()
render_sidebar(user)

st.title("💻 Python 實作區")
st.caption("自由寫程式、實際執行、看輸出結果。程式碼會在你自己的電腦上真的被執行(子行程,有逾時保護)。")

units = all_units_in_order()
unit_options = {"(自由練習,不指定單元)": None}
unit_options.update({u.title: u for u in units})
choice = st.selectbox("參考單元(可選,會列出該單元的範例程式碼供載入)", list(unit_options.keys()))
ref_unit = unit_options[choice]

if ref_unit and ref_unit.examples:
    ex_labels = [f"範例 {i+1}" for i in range(len(ref_unit.examples))]
    picked = st.selectbox("載入範例程式碼", ["(不載入)"] + ex_labels)
    if picked != "(不載入)":
        idx = ex_labels.index(picked)
        st.session_state["scratch_code"] = ref_unit.examples[idx].code

if "scratch_code" not in st.session_state:
    st.session_state["scratch_code"] = "# 在這裡自由寫 Python 程式碼\nprint('Hello, 數據分析!')\n"

code = code_editor("scratch_editor", st.session_state["scratch_code"], height=280)

run_clicked = st.button("▶️ 執行程式碼", type="primary")

if run_clicked:
    st.session_state["scratch_code"] = code
    with st.spinner("執行中..."):
        result = run_code(code)
    if result["timed_out"]:
        st.error("⏱️ 執行逾時,請檢查是否有無窮迴圈。")
    if result["stdout"]:
        st.markdown("**輸出:**")
        st.code(result["stdout"], language="text")
    if result["stderr"]:
        st.markdown("**錯誤訊息:**")
        st.code(result["stderr"], language="text")
    if not result["stdout"] and not result["stderr"]:
        st.info("程式執行完成,沒有任何輸出(可以用 print() 印出你想看的結果)。")
