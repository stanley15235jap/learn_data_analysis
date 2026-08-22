import streamlit as st
from core.db import init_db, mark_unit_opened
from core.content_loader import STAGE_ORDER, STAGE_LABELS, units_for_stage, get_unit
from core.progress import compute_unit_status
from core.ui import render_sidebar, status_badge_html, render_walkthrough

st.set_page_config(page_title="課程學習 | 學習工作台", page_icon="📖", layout="wide")
init_db()

default_unit_id = st.session_state.get("target_unit_id")
if default_unit_id is None or get_unit(default_unit_id) is None:
    default_unit_id = units_for_stage(STAGE_ORDER[0])[0].id

st.title("📖 課程學習")

default_stage = get_unit(default_unit_id).stage
chosen_stage = st.radio(
    "選擇階段", STAGE_ORDER, format_func=lambda s: STAGE_LABELS[s],
    index=STAGE_ORDER.index(default_stage), horizontal=True, key="course_stage_radio",
)

units = units_for_stage(chosen_stage)
options = {u.title: u.id for u in units}
ids = list(options.values())
default_index = ids.index(default_unit_id) if default_unit_id in ids else 0
choice = st.selectbox("選擇單元", list(options.keys()), index=default_index, key=f"select_{chosen_stage}")
selected_unit = get_unit(options[choice])
st.session_state["target_unit_id"] = selected_unit.id

render_sidebar(active_unit_id=selected_unit.id)
mark_unit_opened(selected_unit.id)
status = compute_unit_status(selected_unit)

st.markdown("---")
h1, h2 = st.columns([4, 1])
h1.header(selected_unit.title)
h2.markdown(status_badge_html(status), unsafe_allow_html=True)
st.caption(selected_unit.summary)

for concept in selected_unit.concepts:
    with st.container(border=True):
        st.markdown(f"### {concept.title}")
        st.markdown(f"**1. 這是什麼?** {concept.what}")
        st.markdown(f"**2. 為什麼需要它?** {concept.why}")
        st.markdown(f"**3. 它解決什麼問題?** {concept.problem}")
        st.markdown("**4. 語法怎麼寫?**")
        st.code(concept.syntax, language="python")
        st.markdown(f"**5. 數據分析情境:** {concept.usage}")
        st.warning(f"**⚠️ 常見錯誤:** {concept.common_errors}")
        st.info(f"**🤔 容易混淆:** {concept.confusions}")

st.markdown("### 範例")
for i, ex in enumerate(selected_unit.examples, 1):
    st.code(ex.code, language="python")
    st.caption(ex.explain)

if selected_unit.code_walkthrough:
    st.markdown("---")
    render_walkthrough(selected_unit.code_walkthrough)

st.markdown("---")
c1, c2 = st.columns(2)
with c1:
    if selected_unit.exercises and st.button("✍️ 前往練習", type="primary", use_container_width=True):
        st.session_state["target_unit_id"] = selected_unit.id
        st.switch_page("pages/3_✍️_練習區.py")
with c2:
    if selected_unit.questions and st.button("🧠 前往測驗", use_container_width=True):
        st.session_state["target_unit_id"] = selected_unit.id
        st.switch_page("pages/4_🧠_測驗.py")
