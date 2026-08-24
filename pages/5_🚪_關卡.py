import streamlit as st
from core.db import get_latest_gate_result, upsert_gate_result
from core.auth import bootstrap_app
from content.gates import GATES, PASS_THRESHOLD
from core.grading import grade_answer
from core.db import get_conn, insert_quiz_attempt
from core.weakness import update_weakness
from core.content_loader import all_concepts
from core.ui import render_sidebar

CONCEPT_LOOKUP = all_concepts()  # concept_id -> (Concept, Unit)


def owning_unit_id(concept_id: str) -> str:
    entry = CONCEPT_LOOKUP.get(concept_id)
    return entry[1].id if entry else concept_id

st.set_page_config(page_title="關卡 | 學習工作台", page_icon="🚪", layout="wide")
user = bootstrap_app()
user_id = user["id"]
render_sidebar(user)

st.title("🚪 Stage Gate 關卡")
st.caption("不是看完最後一頁就自動解鎖下一階段——通過關卡測驗,才能確認你真的準備好了。")

gate_keys = list(GATES.keys())
gate_labels = [GATES[k]["title"] for k in gate_keys]
choice = st.selectbox("選擇關卡", gate_labels)
gate = GATES[gate_keys[gate_labels.index(choice)]]

latest = get_latest_gate_result(user_id, gate["stage"])
if latest:
    status_text = "✅ 已通過" if latest["passed"] else "❌ 尚未通過"
    st.markdown(f"最近一次結果:{status_text}(分數 {latest['score']:.0%})")

st.info(gate["description"])

idx_key = f"gate_idx_{gate['stage']}"
result_key = f"gate_results_{gate['stage']}"
if idx_key not in st.session_state:
    st.session_state[idx_key] = 0
if result_key not in st.session_state:
    st.session_state[result_key] = {}

questions = gate["questions"]
idx = st.session_state[idx_key]

if idx >= len(questions):
    results = st.session_state[result_key]
    correct = sum(1 for v in results.values() if v)
    total = len(questions)
    score = correct / total
    passed = score >= PASS_THRESHOLD
    upsert_gate_result(user_id, gate["stage"], passed, score)

    if passed:
        st.success(f"🎉 通過關卡!分數 {score:.0%}(門檻 {PASS_THRESHOLD:.0%})。下一個階段已經解鎖。")
    else:
        st.error(f"分數 {score:.0%},未達門檻 {PASS_THRESHOLD:.0%}。")
        wrong_concepts = sorted({q.concept_id for q in questions if not results.get(q.id, False)})
        st.markdown("**需要補強的知識點:**")
        for c in wrong_concepts:
            st.markdown(f"- `{c}`")
        st.caption("建議回到對應單元複習後再挑戰一次。")

    if st.button("🔁 重新挑戰關卡"):
        st.session_state[idx_key] = 0
        st.session_state[result_key] = {}
        for q in questions:
            answer_key = f"gate_ans_{gate['stage']}_{q.id}"
            for prefix in ("", "gate_submitted_", "gate_correct_"):
                st.session_state.pop(f"{prefix}{answer_key}", None)
        st.rerun()
    st.stop()

q = questions[idx]
st.progress(idx / len(questions), text=f"第 {idx+1} / {len(questions)} 題")

with st.container(border=True):
    st.markdown(f"**{q.prompt}**")
    if q.code:
        st.code(q.code, language="python")

    answer_key = f"gate_ans_{gate['stage']}_{q.id}"

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

    submitted = st.session_state.get(f"gate_submitted_{answer_key}", False)

    if not submitted:
        if st.button("送出答案", type="primary", disabled=(user_answer is None or user_answer == "")):
            is_correct = grade_answer(q, user_answer)
            conn = get_conn()
            unit_id = owning_unit_id(q.concept_id)
            insert_quiz_attempt(conn, user_id, f"gate::{gate['stage']}", q.id, q.concept_id, is_correct, user_answer)
            update_weakness(conn, user_id, q.concept_id, unit_id, is_correct)
            conn.commit()
            conn.close()
            st.session_state[result_key][q.id] = is_correct
            st.session_state[f"gate_submitted_{answer_key}"] = True
            st.session_state[f"gate_correct_{answer_key}"] = is_correct
            st.rerun()
    else:
        is_correct = st.session_state.get(f"gate_correct_{answer_key}", False)
        st.success("✅ 答對了!") if is_correct else st.error("❌ 答錯了。")
        st.info(f"**說明:** {q.explanation}")
        if st.button("下一題 →"):
            st.session_state[idx_key] += 1
            st.rerun()
