import streamlit as st
from core.db import init_db
from core.auth import require_login
from core.content_loader import all_concepts
from core.weakness import get_due_reviews
from core.grading import submit_quiz_answer
from core.ui import render_sidebar

st.set_page_config(page_title="弱點複習 | 學習工作台", page_icon="🎯", layout="wide")
init_db()
user = require_login()
user_id = user["id"]
render_sidebar(user)

st.title("🎯 弱點複習")
st.caption("看過不等於學會。這裡列出答錯過、還沒穩定答對的知識點,依到期時間排序。")

flash = st.session_state.pop("flash_message", None)
if flash:
    is_correct, text = flash
    (st.success if is_correct else st.error)(text)

CONCEPT_LOOKUP = all_concepts()
due, upcoming = get_due_reviews(user_id)

if not due and not upcoming:
    st.success("目前沒有需要複習的弱點,狀態很好!繼續保持。")
    st.stop()

if due:
    st.subheader(f"🔴 現在就該複習({len(due)})")
    for row in due:
        entry = CONCEPT_LOOKUP.get(row["concept_id"])
        if entry is None:
            continue
        concept, unit = entry
        with st.expander(f"{unit.title} → {concept.title}　(答錯 {row['wrong_count']} 次)", expanded=True):
            st.markdown(f"**這是什麼?** {concept.what}")
            st.warning(f"**常見錯誤:** {concept.common_errors}")
            st.info(f"**容易混淆:** {concept.confusions}")

            related_qs = [q for q in unit.questions if q.concept_id == concept.id]
            if not related_qs:
                st.caption("這個知識點目前沒有可重複測驗的題目。")
                continue

            q = related_qs[0]
            st.markdown(f"**再測一次:{q.prompt}**")
            if q.code:
                st.code(q.code, language="python")

            answer_key = f"review_ans_{concept.id}"
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

            if st.button("送出", key=f"review_submit_{concept.id}", disabled=(user_answer is None or user_answer == "")):
                is_correct = submit_quiz_answer(user_id, unit.id, q, user_answer)
                msg = "✅ 答對了!再答對一次同一個知識點就會標記為已掌握。" if is_correct else "❌ 還沒答對,再看一次上面的說明,晚點再試試看。"
                st.session_state["flash_message"] = (is_correct, f"{msg}\n\n**說明:** {q.explanation}")
                st.rerun()

if upcoming:
    st.markdown("---")
    st.subheader(f"🟡 稍後會安排複習({len(upcoming)})")
    for row in upcoming:
        entry = CONCEPT_LOOKUP.get(row["concept_id"])
        if entry is None:
            continue
        concept, unit = entry
        st.markdown(f"- {unit.title} → {concept.title}（下次複習時間：{row['next_review_due'][:10] if row['next_review_due'] else '—'}）")
