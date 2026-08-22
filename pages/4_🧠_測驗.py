import streamlit as st
from core.db import init_db
from core.content_loader import STAGE_ORDER, STAGE_LABELS, units_for_stage, get_unit
from core.grading import submit_quiz_answer
from core.ui import render_sidebar

st.set_page_config(page_title="測驗 | 學習工作台", page_icon="🧠", layout="wide")
init_db()

default_unit_id = st.session_state.get("target_unit_id")
if default_unit_id is None or get_unit(default_unit_id) is None:
    default_unit_id = units_for_stage(STAGE_ORDER[0])[0].id

st.title("🧠 測驗")
st.caption("混合題型:選擇 / 判斷 / 看程式猜結果 / 找 Bug / 簡答。答錯的知識點會被記錄為弱點,之後會安排複習。")

default_stage = get_unit(default_unit_id).stage
chosen_stage = st.radio(
    "選擇階段", STAGE_ORDER, format_func=lambda s: STAGE_LABELS[s],
    index=STAGE_ORDER.index(default_stage), horizontal=True, key="quiz_stage_radio",
)

units = [u for u in units_for_stage(chosen_stage) if u.questions]
if not units:
    st.caption("這個階段沒有測驗題。")
    st.stop()

options = {u.title: u.id for u in units}
ids = list(options.values())
default_index = ids.index(default_unit_id) if default_unit_id in ids else 0
choice = st.selectbox("選擇單元", list(options.keys()), index=default_index, key=f"quiz_select_{chosen_stage}")
selected_unit = get_unit(options[choice])
st.session_state["target_unit_id"] = selected_unit.id

render_sidebar(active_unit_id=selected_unit.id)
st.markdown("---")
st.header(f"測驗:{selected_unit.title}")

idx_key = f"quiz_idx_{selected_unit.id}"
result_key = f"quiz_results_{selected_unit.id}"
if idx_key not in st.session_state:
    st.session_state[idx_key] = 0
if result_key not in st.session_state:
    st.session_state[result_key] = {}

questions = selected_unit.questions
idx = st.session_state[idx_key]

if idx >= len(questions):
    results = st.session_state[result_key]
    correct = sum(1 for v in results.values() if v)
    total = len(questions)
    st.success(f"測驗完成!答對 {correct} / {total} 題。")
    if correct / total < 0.8:
        st.warning("答對率未達 80%,答錯的知識點已被記錄為弱點,建議之後到「弱點複習」再練習一次。")
    if st.button("🔁 重新測驗"):
        st.session_state[idx_key] = 0
        st.session_state[result_key] = {}
        for q in questions:
            answer_key = f"ans_{selected_unit.id}_{q.id}"
            for prefix in ("", "submitted_", "correct_"):
                st.session_state.pop(f"{prefix}{answer_key}", None)
        st.rerun()
    st.stop()

q = questions[idx]
st.progress((idx) / len(questions), text=f"第 {idx+1} / {len(questions)} 題")

with st.container(border=True):
    st.markdown(f"**{q.prompt}**")
    if q.code:
        st.code(q.code, language="python")

    answer_key = f"ans_{selected_unit.id}_{q.id}"

    if q.options:
        labels = [label for _, label in q.options]
        keys = [key for key, _ in q.options]
        picked_label = st.radio("選擇答案", labels, key=answer_key, index=None)
        user_answer = keys[labels.index(picked_label)] if picked_label else None
    elif q.qtype == "tf":
        picked = st.radio("判斷", ["對", "錯"], key=answer_key, index=None)
        user_answer = {"對": "true", "錯": "false"}.get(picked)
    elif q.qtype in ("short", "explain"):
        user_answer = st.text_area("你的回答", key=answer_key)
    else:
        user_answer = st.text_input("你的答案", key=answer_key)

    submitted = st.session_state.get(f"submitted_{answer_key}", False)

    if not submitted:
        if st.button("送出答案", type="primary", disabled=(user_answer is None or user_answer == "")):
            is_correct = submit_quiz_answer(selected_unit.id, q, user_answer)
            st.session_state[result_key][q.id] = is_correct
            st.session_state[f"submitted_{answer_key}"] = True
            st.session_state[f"correct_{answer_key}"] = is_correct
            st.rerun()
    else:
        is_correct = st.session_state.get(f"correct_{answer_key}", False)
        if is_correct:
            st.success("✅ 答對了!")
        else:
            st.error("❌ 答錯了。")
        st.info(f"**說明:** {q.explanation}")
        if st.button("下一題 →"):
            st.session_state[idx_key] += 1
            st.rerun()
