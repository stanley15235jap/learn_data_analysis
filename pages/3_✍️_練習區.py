import streamlit as st
from core.db import init_db, get_passed_exercise_ids
from core.content_loader import STAGE_ORDER, STAGE_LABELS, units_for_stage, get_unit
from core.grading import submit_exercise
from core.ui import render_sidebar, code_editor

st.set_page_config(page_title="練習區 | 學習工作台", page_icon="✍️", layout="wide")
init_db()

default_unit_id = st.session_state.get("target_unit_id")
if default_unit_id is None or get_unit(default_unit_id) is None:
    default_unit_id = units_for_stage(STAGE_ORDER[0])[0].id

st.title("✍️ 練習區")
st.caption("理解 → 看範例 → 自己操作 → 發現問題 → 修正 → 再嘗試。每題都會實際執行你的程式碼並自動檢查。")

default_stage = get_unit(default_unit_id).stage
chosen_stage = st.radio(
    "選擇階段", STAGE_ORDER, format_func=lambda s: STAGE_LABELS[s],
    index=STAGE_ORDER.index(default_stage), horizontal=True, key="ex_stage_radio",
)

units = [u for u in units_for_stage(chosen_stage) if u.exercises]
if not units:
    st.caption("這個階段沒有練習題。")
    st.stop()

options = {u.title: u.id for u in units}
ids = list(options.values())
default_index = ids.index(default_unit_id) if default_unit_id in ids else 0
choice = st.selectbox("選擇單元", list(options.keys()), index=default_index, key=f"ex_select_{chosen_stage}")
selected_unit = get_unit(options[choice])
st.session_state["target_unit_id"] = selected_unit.id

render_sidebar(active_unit_id=selected_unit.id)
st.markdown("---")
st.header(selected_unit.title)

passed_ids = get_passed_exercise_ids(selected_unit.id)

for exercise in selected_unit.exercises:
    is_passed = exercise.id in passed_ids
    title = f"{'✅' if is_passed else '⬜'} {exercise.prompt[:40]}{'...' if len(exercise.prompt) > 40 else ''}"
    with st.expander(title, expanded=not is_passed):
        st.markdown(f"**題目:** {exercise.prompt}")
        if exercise.hint:
            with st.expander("💡 提示"):
                st.code(exercise.hint, language="python")

        code_key = f"code_{selected_unit.id}_{exercise.id}"
        if code_key not in st.session_state:
            st.session_state[code_key] = exercise.starter_code
        code = code_editor(code_key + "_editor", st.session_state[code_key], height=180)

        result_key = f"result_{selected_unit.id}_{exercise.id}"

        if st.button("▶️ 執行並檢查", key=f"submit_{exercise.id}"):
            st.session_state[code_key] = code
            with st.spinner("執行並檢查中..."):
                result = submit_exercise(selected_unit.id, exercise, code)
            st.session_state[result_key] = result
            st.rerun()

        last_result = st.session_state.get(result_key)
        if last_result:
            if last_result["passed"]:
                st.success(f"✅ 通過!{last_result['message']}")
            else:
                st.error(f"❌ 尚未通過:{last_result['message']}")
            if last_result["stdout"]:
                st.caption("你的程式輸出:")
                st.code(last_result["stdout"], language="text")
