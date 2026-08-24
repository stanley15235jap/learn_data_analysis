import streamlit as st
from core.db import init_db, get_all_capstone_steps, upsert_capstone_step
from core.auth import require_login
from core.content_loader import CAPSTONE_STEPS, CAPSTONE_META, all_units_in_order, all_concepts
from core.executor import run_exercise
from core.progress import capstone_readiness_summary
from core.ui import render_sidebar, code_editor

st.set_page_config(page_title="綜合實作 | 學習工作台", page_icon="🏆", layout="wide")
init_db()
user = require_login()
user_id = user["id"]
render_sidebar(user)

st.title("🏆 " + CAPSTONE_META["title"])
st.caption(CAPSTONE_META["description"])

step_rows = get_all_capstone_steps(user_id)
passed_map = {sid: bool(row["passed"]) for sid, row in step_rows.items()}

all_passed = all(passed_map.get(s.id, False) for s in CAPSTONE_STEPS)

st.markdown("### 進度")
progress_cols = st.columns(len(CAPSTONE_STEPS))
for col, step in zip(progress_cols, CAPSTONE_STEPS):
    icon = "✅" if passed_map.get(step.id) else "⬜"
    col.markdown(f"{icon}\n\n{step.title}")

st.markdown("---")

for i, step in enumerate(CAPSTONE_STEPS):
    is_passed = passed_map.get(step.id, False)
    prior_passed = all(passed_map.get(CAPSTONE_STEPS[j].id, False) for j in range(i))
    locked = not prior_passed and not is_passed

    with st.expander(f"{'✅' if is_passed else ('🔒' if locked else '⬜')} {step.title}", expanded=(not is_passed and not locked)):
        if locked:
            st.caption("請先完成前一個步驟。")
            continue
        st.markdown(step.prompt)
        if step.hint:
            with st.expander("💡 提示"):
                st.code(step.hint, language="python")

        code_key = f"cap_code_{step.id}"
        if code_key not in st.session_state:
            existing = step_rows.get(step.id)
            st.session_state[code_key] = existing["submitted_code"] if existing and existing["submitted_code"] else step.starter_code
        code = code_editor(code_key + "_editor", st.session_state[code_key], height=220)

        cap_result_key = f"cap_result_{step.id}"

        if st.button("▶️ 執行並檢查", key=f"cap_submit_{step.id}"):
            st.session_state[code_key] = code
            with st.spinner("執行中..."):
                result = run_exercise(code, step.checker_code)
            upsert_capstone_step(user_id, step.id, "passed" if result["passed"] else "attempted", code, result["passed"], result["message"])
            st.session_state[cap_result_key] = result
            st.rerun()

        last_result = st.session_state.get(cap_result_key)
        if last_result:
            if last_result["passed"]:
                st.success(f"✅ {last_result['message']}")
            else:
                st.error(f"❌ {last_result['message']}")
            if last_result["stdout"]:
                st.code(last_result["stdout"], language="text")

st.markdown("---")

if all_passed:
    st.success("🎉 恭喜完成 Stage 1 綜合實作!以下是根據你目前所有學習紀錄產生的總結報告。")
    summary = capstone_readiness_summary(user_id, all_units_in_order(), all_concepts())

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### ✅ 已掌握")
        for t in summary["mastered_units"]:
            st.markdown(f"- {t}")
        st.markdown("#### ⚠️ 需要加強")
        if summary["needs_practice_units"]:
            for t in summary["needs_practice_units"]:
                st.markdown(f"- {t}")
        else:
            st.caption("沒有需要加強的單元。")

    with c2:
        st.markdown("#### 🎯 主要弱點")
        if summary["frequent_mistakes"]:
            for t in summary["frequent_mistakes"]:
                st.markdown(f"- {t}")
        elif summary["weak_concepts"]:
            for t in summary["weak_concepts"]:
                st.markdown(f"- {t}")
        else:
            st.caption("目前沒有明顯的弱點,很好!")

        st.markdown("#### 🚀 下一階段準備度")
        st.info(f"**{summary['readiness']}**　{summary['readiness_note']}")
        st.caption("（第一版工作台僅呈現準備度,尚未包含進階數據分析/機器學習課程內容。）")
else:
    st.caption("完成所有步驟後,這裡會顯示你的完整分析總結報告。")
