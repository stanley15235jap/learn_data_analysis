"""共用 UI 元件:側邊欄學習路線、狀態徽章、基礎樣式。Operate 模式:資訊層級清楚、狀態一致、可掃描。"""
import streamlit as st
from core.content_loader import STAGE_ORDER, STAGE_LABELS, units_for_stage, get_gate
from core.progress import compute_unit_status, stage_progress, STATUS_LABELS, STATUS_COLORS
from core.weakness import get_due_reviews
from core.db import get_latest_gate_result

BASE_CSS = """
<style>
.status-badge {
    display: inline-block;
    padding: 1px 8px;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 600;
    color: white;
    white-space: nowrap;
}
.unit-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 3px 0;
    font-size: 0.85rem;
}
.gate-box {
    border: 1px solid #E5E7EB;
    border-radius: 8px;
    padding: 10px 12px;
    margin: 6px 0;
    background: #F9FAFB;
}
section[data-testid="stSidebar"] button {
    padding: 2px 8px;
    font-size: 0.82rem;
    min-height: 0;
    height: auto;
    white-space: normal;
    text-align: left;
    justify-content: flex-start;
}
section[data-testid="stSidebar"] div[data-testid="column"] {
    display: flex;
    align-items: center;
}
</style>
"""


def inject_base_css():
    st.markdown(BASE_CSS, unsafe_allow_html=True)


def status_badge_html(status: str) -> str:
    color = STATUS_COLORS.get(status, "#9AA5B1")
    label = STATUS_LABELS.get(status, status)
    return f'<span class="status-badge" style="background:{color}">{label}</span>'


def render_sidebar(user, active_unit_id: str = None):
    inject_base_css()
    user_id = user["id"]
    with st.sidebar:
        st.markdown(f"**{user['username']}**　`{'管理員' if user['role'] == 'admin' else '一般帳號'}`")
        if st.button("登出", key="sidebar_logout", use_container_width=True):
            from core.auth import logout

            logout()
            st.rerun()
        st.markdown("---")

        st.markdown("### 學習路線")

        due, _ = get_due_reviews(user_id)
        if due:
            st.markdown(f"🎯 **{len(due)} 個弱點待複習** — [前往複習](/弱點複習)")

        for stage in STAGE_ORDER:
            units = units_for_stage(stage)
            prog = stage_progress(user_id, units)
            st.markdown(f"**{STAGE_LABELS[stage]}** · {prog['percent']}%")
            st.progress(prog["percent"] / 100)

            gate = get_gate_for_stage_entry(stage)
            if gate is not None:
                gate_row = get_latest_gate_result(user_id, gate["stage"])
                passed = bool(gate_row["passed"]) if gate_row else False
                icon = "✅" if passed else "⭕"
                st.caption(f"{icon} {gate['title']}（可自由挑戰,非強制）")

            for u in units:
                status = compute_unit_status(user_id, u)
                marker = "➤ " if u.id == active_unit_id else ""
                c1, c2 = st.columns([3, 1])
                if c1.button(marker + u.title, key=f"sidebar_nav_{u.id}", use_container_width=True):
                    st.session_state["target_unit_id"] = u.id
                    st.switch_page("pages/1_📖_課程學習.py")
                c2.markdown(status_badge_html(status), unsafe_allow_html=True)
            st.markdown("---")


def get_gate_for_stage_entry(stage: str):
    """回傳『進入這個 stage 之前』要通過的關卡(如果有的話)。"""
    mapping = {"numpy": "python_to_numpy", "pandas": "numpy_to_pandas"}
    gate_key = mapping.get(stage)
    if gate_key is None:
        return None
    return get_gate(gate_key)


def stage_unlocked(stage: str) -> bool:
    """所有階段/單元一律可自由進入,不強制要求先通過前一階段的關卡。
    Stage Gate 測驗仍然存在,可作為自我檢測,但不再阻擋進入下一階段的內容。"""
    return True


def code_editor(key: str, initial_code: str, height: int = 220) -> str:
    """程式碼編輯器:優先用 streamlit-ace(語法高亮),沒安裝時退回 text_area。"""
    try:
        from streamlit_ace import st_ace

        return st_ace(
            value=initial_code,
            language="python",
            theme="github",
            key=key,
            height=height,
            font_size=14,
            tab_size=4,
            auto_update=True,
            show_gutter=True,
        )
    except ImportError:
        return st.text_area("程式碼", value=initial_code, height=height, key=key)


def render_walkthrough(walkthrough):
    """逐段程式碼拆解元件,方法論借用 python-onboarding 的『觸發點→演進脈絡→最終呈現』。"""
    if walkthrough is None:
        return
    st.markdown(f"#### 🔍 程式碼閱讀練習:{walkthrough.title}")
    st.code(walkthrough.full_code, language="python")
    built = ""
    for i, step in enumerate(walkthrough.steps):
        built += step.segment
        label = "觸發點" if i == 0 else ("最終呈現" if i == len(walkthrough.steps) - 1 else f"演進脈絡 {i}")
        with st.expander(f"{label}　`{step.segment}`", expanded=False):
            st.write(step.explain)
            st.code(built, language="python")
    st.success(f"🎯 最終結果:{walkthrough.final_output_note}")
