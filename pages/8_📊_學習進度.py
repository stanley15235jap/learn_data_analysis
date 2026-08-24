import streamlit as st
import pandas as pd
from core.db import get_all_capstone_steps
from core.auth import bootstrap_app
from core.content_loader import STAGE_ORDER, STAGE_LABELS, units_for_stage, CAPSTONE_STEPS
from core.progress import compute_unit_status, stage_progress, STATUS_LABELS
from core.weakness import get_due_reviews, get_all_weak_concepts
from core.ui import render_sidebar

st.set_page_config(page_title="學習進度 | 學習工作台", page_icon="📊", layout="wide")
user = bootstrap_app()
user_id = user["id"]
render_sidebar(user)

st.title("📊 學習進度")

overview_cols = st.columns(len(STAGE_ORDER) + 1)
for col, stage in zip(overview_cols, STAGE_ORDER):
    units = units_for_stage(stage)
    prog = stage_progress(user_id, units)
    with col:
        st.metric(STAGE_LABELS[stage], f"{prog['percent']}%", f"{prog['counts']['mastered']}/{prog['total']} 已掌握")

due, upcoming = get_due_reviews(user_id)
with overview_cols[-1]:
    st.metric("待複習弱點", len(due) + len(upcoming), f"{len(due)} 個現在就該複習")

st.markdown("---")

for stage in STAGE_ORDER:
    st.subheader(STAGE_LABELS[stage])
    units = units_for_stage(stage)
    rows = []
    for u in units:
        status = compute_unit_status(user_id, u)
        rows.append({"單元": u.title, "狀態": STATUS_LABELS[status]})
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)

st.markdown("---")
st.subheader("弱點總覽")
weak_rows = get_all_weak_concepts(user_id)
if weak_rows:
    weak_df = pd.DataFrame(
        [
            {
                "知識點": r["concept_id"],
                "狀態": {"needs_review": "需要複習", "recovering": "恢復中"}.get(r["status"], r["status"]),
                "答錯次數": r["wrong_count"],
                "下次複習": (r["next_review_due"] or "—")[:10] if r["next_review_due"] else "—",
            }
            for r in weak_rows
        ]
    )
    st.dataframe(weak_df, use_container_width=True, hide_index=True)
else:
    st.caption("目前沒有記錄中的弱點。")

st.markdown("---")
st.subheader("Stage 1 綜合實作進度")
cap_rows = get_all_capstone_steps(user_id)
cap_done = sum(1 for s in CAPSTONE_STEPS if cap_rows.get(s.id) and cap_rows[s.id]["passed"])
st.progress(cap_done / len(CAPSTONE_STEPS), text=f"{cap_done} / {len(CAPSTONE_STEPS)} 個步驟已完成")
