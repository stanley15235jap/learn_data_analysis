"""用子行程實際執行使用者寫的 Python 程式碼。

單人本機使用,子行程本身就是隔離邊界;Windows 沒有 resource 模組可做記憶體限制,
v1 用「執行逾時 + 獨立行程」防止無窮迴圈卡死主程式,README 有註明這個已知限制。
"""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

TIMEOUT_SECONDS = 8
PROJECT_ROOT = Path(__file__).resolve().parent.parent


def run_code(code: str, timeout: int = TIMEOUT_SECONDS) -> dict:
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding="utf-8") as f:
        f.write(code)
        path = f.name
    try:
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        result = subprocess.run(
            [sys.executable, path],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            cwd=str(PROJECT_ROOT),
            env=env,
        )
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "timed_out": False,
            "returncode": result.returncode,
        }
    except subprocess.TimeoutExpired as e:
        stdout = e.stdout.decode("utf-8", "replace") if isinstance(e.stdout, bytes) else (e.stdout or "")
        return {
            "stdout": stdout,
            "stderr": "執行逾時(超過 {}秒),請檢查是否有無窮迴圈。".format(timeout),
            "timed_out": True,
            "returncode": None,
        }
    finally:
        try:
            os.unlink(path)
        except OSError:
            pass


def run_exercise(student_code: str, checker_code: str, timeout: int = TIMEOUT_SECONDS) -> dict:
    """學生程式碼 + 隱藏 checker 一起執行。checker 需印出一行 RESULT_JSON:{...}。"""
    full_code = student_code + "\n\n# ---- 自動檢查(不會顯示給學生) ----\n" + checker_code
    result = run_code(full_code, timeout=timeout)

    passed = False
    message = ""
    for line in result["stdout"].splitlines():
        if line.startswith("RESULT_JSON:"):
            try:
                payload = json.loads(line[len("RESULT_JSON:"):])
                passed = bool(payload.get("passed", False))
                message = payload.get("message", "")
            except json.JSONDecodeError:
                pass

    visible_stdout = "\n".join(
        line for line in result["stdout"].splitlines() if not line.startswith("RESULT_JSON:")
    )

    if not passed and not message:
        if result["timed_out"]:
            message = "執行逾時。"
        elif result["stderr"]:
            message = "程式執行發生錯誤:\n" + result["stderr"].strip().splitlines()[-1]
        else:
            message = "尚未通過檢查,再試試看。"

    return {
        "passed": passed,
        "message": message,
        "stdout": visible_stdout,
        "stderr": result["stderr"],
        "timed_out": result["timed_out"],
    }
