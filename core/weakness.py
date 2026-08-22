"""弱點追蹤與簡易間隔複習排程。"""
from datetime import datetime, timedelta, timezone
from core.db import get_conn, now_iso


def update_weakness(conn, concept_id: str, unit_id: str, is_correct: bool):
    row = conn.execute("SELECT * FROM concept_weakness WHERE concept_id=?", (concept_id,)).fetchone()
    now = datetime.now(timezone.utc)

    if row is None:
        wrong_count = 0 if is_correct else 1
        correct_streak = 1 if is_correct else 0
        status = "resolved" if is_correct else "needs_review"
        next_due = None if is_correct else (now + timedelta(days=1)).isoformat()
        conn.execute(
            """INSERT INTO concept_weakness
               (concept_id, unit_id, wrong_count, correct_streak, status, next_review_due, last_seen_at)
               VALUES (?,?,?,?,?,?,?)""",
            (concept_id, unit_id, wrong_count, correct_streak, status, next_due, now.isoformat()),
        )
        return

    wrong_count = row["wrong_count"]
    correct_streak = row["correct_streak"]
    status = row["status"]
    next_due = row["next_review_due"]

    if is_correct:
        correct_streak += 1
        if status in ("needs_review", "recovering"):
            if correct_streak >= 2:
                status = "resolved"
                next_due = None
            else:
                status = "recovering"
                days = 3 if wrong_count <= 1 else 7
                next_due = (now + timedelta(days=days)).isoformat()
        else:
            status = "resolved"
    else:
        wrong_count += 1
        correct_streak = 0
        status = "needs_review"
        next_due = (now + timedelta(days=1)).isoformat()

    conn.execute(
        """UPDATE concept_weakness
           SET unit_id=?, wrong_count=?, correct_streak=?, status=?, next_review_due=?, last_seen_at=?
           WHERE concept_id=?""",
        (unit_id, wrong_count, correct_streak, status, next_due, now.isoformat(), concept_id),
    )


def get_weakness_row(concept_id: str):
    conn = get_conn()
    row = conn.execute("SELECT * FROM concept_weakness WHERE concept_id=?", (concept_id,)).fetchone()
    conn.close()
    return row


def get_all_weak_concepts():
    """回傳所有需要注意的 concept(needs_review 或 recovering),依到期日排序。"""
    conn = get_conn()
    rows = conn.execute(
        """SELECT * FROM concept_weakness
           WHERE status IN ('needs_review', 'recovering')
           ORDER BY (next_review_due IS NULL), next_review_due ASC"""
    ).fetchall()
    conn.close()
    return rows


def get_due_reviews():
    """回傳已到複習時間(或從未複習過的 needs_review)的項目。"""
    now = now_iso()
    all_weak = get_all_weak_concepts()
    due = [r for r in all_weak if r["next_review_due"] is None or r["next_review_due"] <= now]
    upcoming = [r for r in all_weak if r not in due]
    return due, upcoming


def unit_has_unresolved_weakness(unit_id: str) -> bool:
    conn = get_conn()
    row = conn.execute(
        "SELECT COUNT(*) c FROM concept_weakness WHERE unit_id=? AND status IN ('needs_review','recovering')",
        (unit_id,),
    ).fetchone()
    conn.close()
    return row["c"] > 0
