"""單元/階段掌握程度判定。狀態不只看『看過沒』,而是綜合練習與測驗表現。所有查詢以 user_id 區分帳號。"""
from core.db import get_conn, get_unit_progress_row
from core.weakness import unit_has_unresolved_weakness

STATUS_LABELS = {
    "not_started": "尚未開始",
    "in_progress": "學習中",
    "practiced": "已練習",
    "needs_review": "需要複習",
    "mastered": "已掌握",
}

STATUS_COLORS = {
    "not_started": "#9AA5B1",
    "in_progress": "#3B82F6",
    "practiced": "#8B5CF6",
    "needs_review": "#F59E0B",
    "mastered": "#22C55E",
}

MASTERY_QUIZ_THRESHOLD = 0.8


def compute_unit_status(user_id: int, unit) -> str:
    prog_row = get_unit_progress_row(user_id, unit.id)
    if prog_row is None:
        return "not_started"

    conn = get_conn()

    ex_passed = 0
    if unit.exercises:
        rows = conn.execute(
            "SELECT DISTINCT exercise_id FROM exercise_submissions WHERE user_id=? AND unit_id=? AND passed=1",
            (user_id, unit.id),
        ).fetchall()
        ex_passed = len(rows)
    practiced = (not unit.exercises) or ex_passed >= len(unit.exercises)

    quiz_correct = 0
    for q in unit.questions:
        last = conn.execute(
            "SELECT is_correct FROM quiz_attempts WHERE user_id=? AND unit_id=? AND question_id=? ORDER BY id DESC LIMIT 1",
            (user_id, unit.id, q.id),
        ).fetchone()
        if last and last["is_correct"]:
            quiz_correct += 1
    conn.close()

    quiz_ratio = (quiz_correct / len(unit.questions)) if unit.questions else 1.0
    tested = quiz_ratio >= MASTERY_QUIZ_THRESHOLD

    if unit_has_unresolved_weakness(user_id, unit.id):
        return "needs_review"
    if tested and practiced:
        return "mastered"
    if practiced:
        return "practiced"
    return "in_progress"


def stage_progress(user_id: int, units_in_stage):
    total = len(units_in_stage)
    counts = {"not_started": 0, "in_progress": 0, "practiced": 0, "needs_review": 0, "mastered": 0}
    for u in units_in_stage:
        counts[compute_unit_status(user_id, u)] += 1
    mastered = counts["mastered"]
    percent = round(100 * mastered / total) if total else 0
    return {"total": total, "counts": counts, "percent": percent}


def capstone_readiness_summary(user_id: int, all_units, all_concepts_lookup):
    """給 Stage 1 綜合實作結尾用:已掌握 / 需加強 / 主要弱點 / 下一階段準備度。"""
    from core.weakness import get_all_weak_concepts
    from core.db import get_conn

    mastered_units = []
    needs_practice_units = []
    for u in all_units:
        status = compute_unit_status(user_id, u)
        if status == "mastered":
            mastered_units.append(u.title)
        else:
            needs_practice_units.append(f"{u.title}({STATUS_LABELS[status]})")

    weak_rows = get_all_weak_concepts(user_id)
    weak_concepts = []
    for row in weak_rows:
        entry = all_concepts_lookup.get(row["concept_id"])
        if entry:
            concept, unit = entry
            weak_concepts.append(f"{unit.title} → {concept.title}")

    conn = get_conn()
    ever_wrong = conn.execute(
        "SELECT concept_id, wrong_count FROM concept_weakness WHERE user_id=? AND wrong_count >= 2 ORDER BY wrong_count DESC",
        (user_id,),
    ).fetchall()
    conn.close()
    frequent_mistakes = []
    for row in ever_wrong:
        entry = all_concepts_lookup.get(row["concept_id"])
        if entry:
            concept, unit = entry
            frequent_mistakes.append(f"{unit.title} → {concept.title}(答錯 {row['wrong_count']} 次)")

    total = len(all_units)
    mastered_ratio = len(mastered_units) / total if total else 0
    if mastered_ratio >= 0.9 and not weak_concepts:
        readiness = "準備度高"
        readiness_note = "三個階段的核心觀念都已掌握,且沒有未解決的弱點,適合往下一階段(進階數據分析/機器學習基礎)前進。"
    elif mastered_ratio >= 0.7:
        readiness = "準備度中等"
        readiness_note = "大部分單元已掌握,但仍有少數弱點或未完成的單元,建議先處理「主要弱點」清單再往下一階段前進。"
    else:
        readiness = "尚未準備好"
        readiness_note = "還有不少單元需要加強,建議先把「需要加強」清單中的單元練熟,再考慮進入下一階段。"

    return {
        "mastered_units": mastered_units,
        "needs_practice_units": needs_practice_units,
        "weak_concepts": weak_concepts,
        "frequent_mistakes": frequent_mistakes,
        "readiness": readiness,
        "readiness_note": readiness_note,
    }


def next_recommended_unit(user_id: int, units_in_order):
    """依序找出第一個還沒『已掌握』的單元。"""
    for u in units_in_order:
        if compute_unit_status(user_id, u) != "mastered":
            return u
    return None
