import streamlit as st
from core.auth import bootstrap_app
from core.content_loader import STAGE_ORDER, STAGE_LABELS, units_for_stage
from core.progress import compute_unit_status, stage_progress, next_recommended_unit
from core.weakness import get_due_reviews
from core.ui import render_sidebar, status_badge_html

st.set_page_config(page_title="數據分析學習工作台", page_icon="📊", layout="wide")
user = bootstrap_app()
user_id = user["id"]
render_sidebar(user)

st.title("📊 數據分析 × 機器學習學習工作台")
st.caption("第一階段:Python 基礎 → NumPy → Pandas")

# ---- 今天可以學什麼 ----
recommendation = None
recommend_kind = None  # "unit" | "capstone"

for stage in STAGE_ORDER:
    units = units_for_stage(stage)
    nxt = next_recommended_unit(user_id, units)
    if nxt is not None:
        recommendation = nxt
        recommend_kind = "unit"
        break
else:
    recommend_kind = "capstone"

due, upcoming = get_due_reviews(user_id)

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("今天可以做什麼")
    if recommend_kind == "unit":
        st.info(f"📖 建議繼續學習:**{recommendation.title}**({STAGE_LABELS[recommendation.stage]})")
        if st.button("前往這個單元 →", type="primary"):
            st.session_state["target_unit_id"] = recommendation.id
            st.switch_page("pages/1_📖_課程學習.py")
    elif recommend_kind == "capstone":
        st.success("🏆 三個階段的單元都已掌握!前往 Stage 1 綜合實作,完成一次完整的資料分析。")
        if st.button("前往綜合實作 →", type="primary"):
            st.switch_page("pages/7_🏆_綜合實作.py")

    if due:
        st.markdown(f"🎯 另外有 **{len(due)} 個知識點**已經到了複習時間。")
        if st.button("前往弱點複習"):
            st.switch_page("pages/6_🎯_弱點複習.py")

with col2:
    st.subheader("整體進度")
    for stage in STAGE_ORDER:
        units = units_for_stage(stage)
        prog = stage_progress(user_id, units)
        st.markdown(f"**{STAGE_LABELS[stage]}**")
        st.progress(prog["percent"] / 100, text=f"{prog['counts']['mastered']}/{prog['total']} 已掌握")

st.markdown("---")
st.subheader("學習路線總覽")

tabs = st.tabs([STAGE_LABELS[s] for s in STAGE_ORDER])
for tab, stage in zip(tabs, STAGE_ORDER):
    with tab:
        units = units_for_stage(stage)
        for u in units:
            status = compute_unit_status(user_id, u)
            c1, c2, c3 = st.columns([3, 1, 1])
            c1.markdown(f"**{u.title}**")
            c1.caption(u.summary)
            c2.markdown(status_badge_html(status), unsafe_allow_html=True)
            if c3.button("進入", key=f"go_{u.id}"):
                st.session_state["target_unit_id"] = u.id
                st.switch_page("pages/1_📖_課程學習.py")
