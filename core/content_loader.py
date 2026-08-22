"""彙整 content/ 底下所有課程單元、關卡、Capstone 定義,提供給頁面查詢。"""
from content.python_basics.units import UNITS as PYTHON_UNITS
from content.numpy_basics.units import UNITS as NUMPY_UNITS
from content.pandas_basics.units import UNITS as PANDAS_UNITS
from content.gates import GATES
from content.capstone import STEPS as CAPSTONE_STEPS, CAPSTONE_META

STAGE_ORDER = ["python", "numpy", "pandas"]
STAGE_LABELS = {"python": "Python 基礎", "numpy": "NumPy", "pandas": "Pandas"}

ALL_UNITS = PYTHON_UNITS + NUMPY_UNITS + PANDAS_UNITS
UNITS_BY_ID = {u.id: u for u in ALL_UNITS}


def units_for_stage(stage: str):
    return sorted([u for u in ALL_UNITS if u.stage == stage], key=lambda u: u.order)


def all_units_in_order():
    result = []
    for stage in STAGE_ORDER:
        result.extend(units_for_stage(stage))
    return result


def get_unit(unit_id: str):
    return UNITS_BY_ID.get(unit_id)


def get_gate(stage: str):
    return GATES.get(stage)


def all_concepts():
    concepts = {}
    for u in ALL_UNITS:
        for c in u.concepts:
            concepts[c.id] = (c, u)
    return concepts
