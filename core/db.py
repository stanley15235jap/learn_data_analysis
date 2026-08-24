"""SQLite 資料存取層。只負責讀寫,不含判斷邏輯(判斷邏輯在 progress.py / weakness.py)。

所有進度相關的表都以 user_id 區分帳號,查詢時一律要帶入目前登入者的 user_id。
"""
import sqlite3
from pathlib import Path
from datetime import datetime, timezone

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "workbench.db"


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def get_conn():
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user',
            status TEXT NOT NULL DEFAULT 'active',
            created_at TEXT
        );

        CREATE TABLE IF NOT EXISTS unit_progress (
            user_id INTEGER NOT NULL,
            unit_id TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'in_progress',
            opened_at TEXT,
            last_updated TEXT,
            PRIMARY KEY (user_id, unit_id)
        );

        CREATE TABLE IF NOT EXISTS exercise_submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            unit_id TEXT NOT NULL,
            exercise_id TEXT NOT NULL,
            code TEXT,
            passed INTEGER,
            message TEXT,
            submitted_at TEXT
        );

        CREATE TABLE IF NOT EXISTS quiz_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            unit_id TEXT NOT NULL,
            question_id TEXT NOT NULL,
            concept_id TEXT,
            is_correct INTEGER,
            answer TEXT,
            attempted_at TEXT
        );

        CREATE TABLE IF NOT EXISTS concept_weakness (
            user_id INTEGER NOT NULL,
            concept_id TEXT NOT NULL,
            unit_id TEXT,
            wrong_count INTEGER DEFAULT 0,
            correct_streak INTEGER DEFAULT 0,
            status TEXT DEFAULT 'resolved',
            next_review_due TEXT,
            last_seen_at TEXT,
            PRIMARY KEY (user_id, concept_id)
        );

        CREATE TABLE IF NOT EXISTS gate_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            stage TEXT,
            passed INTEGER,
            score REAL,
            attempted_at TEXT
        );

        CREATE TABLE IF NOT EXISTS capstone_progress (
            user_id INTEGER NOT NULL,
            step_id TEXT NOT NULL,
            status TEXT DEFAULT 'not_started',
            submitted_code TEXT,
            passed INTEGER,
            notes TEXT,
            updated_at TEXT,
            PRIMARY KEY (user_id, step_id)
        );
        """
    )
    conn.commit()
    conn.close()


# ---------- unit_progress ----------

def mark_unit_opened(user_id: int, unit_id: str):
    conn = get_conn()
    row = conn.execute(
        "SELECT unit_id FROM unit_progress WHERE user_id=? AND unit_id=?", (user_id, unit_id)
    ).fetchone()
    ts = now_iso()
    if row is None:
        conn.execute(
            "INSERT INTO unit_progress (user_id, unit_id, status, opened_at, last_updated) VALUES (?,?,?,?,?)",
            (user_id, unit_id, "in_progress", ts, ts),
        )
    else:
        conn.execute(
            "UPDATE unit_progress SET last_updated=? WHERE user_id=? AND unit_id=?", (ts, user_id, unit_id)
        )
    conn.commit()
    conn.close()


def get_unit_progress_row(user_id: int, unit_id: str):
    conn = get_conn()
    row = conn.execute(
        "SELECT * FROM unit_progress WHERE user_id=? AND unit_id=?", (user_id, unit_id)
    ).fetchone()
    conn.close()
    return row


def get_all_unit_progress(user_id: int):
    conn = get_conn()
    rows = conn.execute("SELECT * FROM unit_progress WHERE user_id=?", (user_id,)).fetchall()
    conn.close()
    return {r["unit_id"]: r for r in rows}


# ---------- exercises ----------

def insert_exercise_submission(user_id, unit_id, exercise_id, code, passed, message):
    conn = get_conn()
    conn.execute(
        "INSERT INTO exercise_submissions (user_id, unit_id, exercise_id, code, passed, message, submitted_at) VALUES (?,?,?,?,?,?,?)",
        (user_id, unit_id, exercise_id, code, int(passed), message, now_iso()),
    )
    conn.commit()
    conn.close()


def get_passed_exercise_ids(user_id: int, unit_id: str):
    conn = get_conn()
    rows = conn.execute(
        "SELECT DISTINCT exercise_id FROM exercise_submissions WHERE user_id=? AND unit_id=? AND passed=1",
        (user_id, unit_id),
    ).fetchall()
    conn.close()
    return {r["exercise_id"] for r in rows}


def get_exercise_attempts(user_id: int, unit_id: str, exercise_id: str):
    conn = get_conn()
    rows = conn.execute(
        "SELECT * FROM exercise_submissions WHERE user_id=? AND unit_id=? AND exercise_id=? ORDER BY id DESC",
        (user_id, unit_id, exercise_id),
    ).fetchall()
    conn.close()
    return rows


# ---------- quiz ----------

def insert_quiz_attempt(conn, user_id, unit_id, question_id, concept_id, is_correct, answer):
    conn.execute(
        "INSERT INTO quiz_attempts (user_id, unit_id, question_id, concept_id, is_correct, answer, attempted_at) VALUES (?,?,?,?,?,?,?)",
        (user_id, unit_id, question_id, concept_id, int(is_correct), str(answer), now_iso()),
    )


def get_last_attempt(conn, user_id, unit_id, question_id):
    return conn.execute(
        "SELECT * FROM quiz_attempts WHERE user_id=? AND unit_id=? AND question_id=? ORDER BY id DESC LIMIT 1",
        (user_id, unit_id, question_id),
    ).fetchone()


def get_quiz_history(user_id: int, unit_id: str):
    conn = get_conn()
    rows = conn.execute(
        "SELECT * FROM quiz_attempts WHERE user_id=? AND unit_id=? ORDER BY id DESC", (user_id, unit_id)
    ).fetchall()
    conn.close()
    return rows


# ---------- gates ----------

def upsert_gate_result(user_id, stage, passed, score):
    conn = get_conn()
    conn.execute(
        "INSERT INTO gate_results (user_id, stage, passed, score, attempted_at) VALUES (?,?,?,?,?)",
        (user_id, stage, int(passed), score, now_iso()),
    )
    conn.commit()
    conn.close()


def get_latest_gate_result(user_id, stage):
    conn = get_conn()
    row = conn.execute(
        "SELECT * FROM gate_results WHERE user_id=? AND stage=? ORDER BY id DESC LIMIT 1", (user_id, stage)
    ).fetchone()
    conn.close()
    return row


# ---------- capstone ----------

def upsert_capstone_step(user_id, step_id, status, submitted_code, passed, notes):
    conn = get_conn()
    row = conn.execute(
        "SELECT step_id FROM capstone_progress WHERE user_id=? AND step_id=?", (user_id, step_id)
    ).fetchone()
    ts = now_iso()
    if row is None:
        conn.execute(
            "INSERT INTO capstone_progress (user_id, step_id, status, submitted_code, passed, notes, updated_at) VALUES (?,?,?,?,?,?,?)",
            (user_id, step_id, status, submitted_code, int(passed), notes, ts),
        )
    else:
        conn.execute(
            "UPDATE capstone_progress SET status=?, submitted_code=?, passed=?, notes=?, updated_at=? WHERE user_id=? AND step_id=?",
            (status, submitted_code, int(passed), notes, ts, user_id, step_id),
        )
    conn.commit()
    conn.close()


def get_all_capstone_steps(user_id: int):
    conn = get_conn()
    rows = conn.execute("SELECT * FROM capstone_progress WHERE user_id=?", (user_id,)).fetchall()
    conn.close()
    return {r["step_id"]: r for r in rows}
