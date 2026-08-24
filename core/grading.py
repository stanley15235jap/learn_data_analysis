"""測驗批改與練習提交的協調層:呼叫 executor/db/weakness,不重複定義判斷細節。"""
from core.db import get_conn, insert_quiz_attempt, insert_exercise_submission
from core.weakness import update_weakness
from core.executor import run_exercise


def grade_answer(question, user_answer) -> bool:
    qtype = question.qtype
    if qtype in ("mc", "tf", "predict", "bugfix", "fill"):
        return str(user_answer).strip() == str(question.answer).strip()
    if qtype in ("short", "explain"):
        text = str(user_answer or "").lower()
        if not question.keywords:
            return len(text.strip()) > 0
        return all(k.lower() in text for k in question.keywords)
    return False


def submit_quiz_answer(user_id: int, unit_id: str, question, user_answer) -> bool:
    """批改一題、寫入 quiz_attempts、同步更新該 concept 的弱點狀態。回傳是否答對。"""
    is_correct = grade_answer(question, user_answer)
    conn = get_conn()
    insert_quiz_attempt(conn, user_id, unit_id, question.id, question.concept_id, is_correct, user_answer)
    update_weakness(conn, user_id, question.concept_id, unit_id, is_correct)
    conn.commit()
    conn.close()
    return is_correct


def submit_exercise(user_id: int, unit_id: str, exercise, student_code: str) -> dict:
    """執行學生程式碼、批改、寫入 exercise_submissions。回傳執行結果 dict。"""
    result = run_exercise(student_code, exercise.checker_code)
    insert_exercise_submission(user_id, unit_id, exercise.id, student_code, result["passed"], result["message"])
    return result
