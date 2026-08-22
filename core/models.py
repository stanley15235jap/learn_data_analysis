"""資料模型定義：課程內容的結構（不是資料庫 schema，資料庫 schema 在 db.py）。"""
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Concept:
    """一個知識點。七問結構對應課程學習區的固定講解框架。"""
    id: str
    title: str
    what: str            # 這是什麼？
    why: str              # 為什麼需要它？
    problem: str           # 它解決什麼問題？
    syntax: str              # 語法怎麼寫？
    usage: str                 # 數據分析時可能怎麼使用？
    common_errors: str          # 常見錯誤有哪些？
    confusions: str               # 初學者容易混淆什麼？


@dataclass
class Example:
    code: str
    explain: str


@dataclass
class WalkthroughStep:
    segment: str      # 程式碼片段，例如 .groupby("department")
    explain: str      # 這段在做什麼


@dataclass
class CodeWalkthrough:
    """逐段程式碼拆解，方法論借用 python-onboarding 的 觸發點→演進脈絡→最終呈現。"""
    title: str
    full_code: str
    steps: list  # list[WalkthroughStep]
    final_output_note: str


@dataclass
class Exercise:
    id: str
    prompt: str
    starter_code: str
    checker_code: str   # 接在學生程式碼後執行，需印出一行 RESULT_JSON:{...}
    hint: str = ""


@dataclass
class Question:
    """qtype: mc | tf | predict | bugfix | fill | short | explain"""
    id: str
    concept_id: str
    qtype: str
    prompt: str
    code: str = ""
    options: list = field(default_factory=list)   # [(key, label), ...] for mc
    answer: str = ""
    explanation: str = ""
    keywords: list = field(default_factory=list)   # short/explain 用：需包含的關鍵字


@dataclass
class CapstoneStep:
    id: str
    title: str
    prompt: str
    starter_code: str
    checker_code: str
    hint: str = ""


@dataclass
class Unit:
    id: str
    stage: str        # python | numpy | pandas
    order: int
    title: str
    summary: str
    concepts: list         # list[Concept]
    examples: list           # list[Example]
    exercises: list            # list[Exercise]
    questions: list               # list[Question]
    code_walkthrough: Optional[CodeWalkthrough] = None

    def concept_ids(self):
        return [c.id for c in self.concepts]
