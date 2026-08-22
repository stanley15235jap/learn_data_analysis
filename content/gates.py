# -*- coding: utf-8 -*-
"""Stage Gate 題組:不是看完最後一頁就解鎖下一階段,而是要通過關卡測驗。"""
from core.models import Question

PASS_THRESHOLD = 0.75

GATES = {
    "python_to_numpy": {
        "stage": "python_to_numpy",
        "unlocks": "numpy",
        "title": "關卡一:Python 基礎 → NumPy",
        "description": "確認你已經具備學習 NumPy 所需要的 Python 能力:list 操作、迴圈、函式、條件判斷。",
        "questions": [
            Question(id="gate_pn_1", concept_id="c_list", qtype="predict", prompt="這段會印出什麼?", code="nums = [5, 2, 8, 1]\nprint(sorted(nums, reverse=True)[0])",
                      answer="8", explanation="由大到小排序後取第一個,是最大值。"),
            Question(id="gate_pn_2", concept_id="c_loops", qtype="predict", prompt="這段會印出什麼?", code="total = 0\nfor i in range(1, 5):\n    total += i\nprint(total)",
                      answer="10", explanation="1+2+3+4=10。"),
            Question(id="gate_pn_3", concept_id="c_conditionals", qtype="bugfix", prompt="這段程式碼哪裡有問題?", code="x = 10\nif x = 10:\n    print('yes')",
                      options=[("a", "應該用 == 而不是 ="), ("b", "x 命名不合法"), ("c", "print 用法錯誤"), ("d", "沒有問題")],
                      answer="a", explanation="判斷相等要用 ==。"),
            Question(id="gate_pn_4", concept_id="c_functions", qtype="predict", prompt="這段會印出什麼?", code="def square(x):\n    return x * x\nprint(square(3) + square(4))",
                      answer="25", explanation="9 + 16 = 25。"),
            Question(id="gate_pn_5", concept_id="c_dict", qtype="mc", prompt="想安全地取 dict 中可能不存在的 key,避免報錯,應該用?",
                      options=[("a", "d.get(key, 預設值)"), ("b", "d[key]"), ("c", "d.key"), ("d", "d.find(key)")],
                      answer="a", explanation="get() 可以指定 key 不存在時的預設值。"),
            Question(id="gate_pn_6", concept_id="c_comprehension", qtype="predict", prompt="這段會印出什麼?", code="print([x for x in range(5) if x % 2 == 1])",
                      answer="[1, 3]", explanation="range(5) 是0~4,其中奇數是1和3。"),
            Question(id="gate_pn_7", concept_id="c_list", qtype="tf", prompt="判斷對錯:[1,2,3] + [4,5,6] 會逐項相加得到 [5,7,9]。",
                      answer="false", explanation="list 相加是串接,不是逐項相加,這正是要學 NumPy 陣列的原因。"),
            Question(id="gate_pn_8", concept_id="c_functions", qtype="bugfix", prompt="這段程式呼叫後 result 會是什麼?", code="def add(a, b):\n    c = a + b\nresult = add(2, 3)",
                      options=[("a", "None,因為函式沒有 return"), ("b", "5"), ("c", "報錯"), ("d", "0")],
                      answer="a", explanation="函式沒有 return,呼叫端拿到 None。"),
        ],
    },
    "numpy_to_pandas": {
        "stage": "numpy_to_pandas",
        "unlocks": "pandas",
        "title": "關卡二:NumPy → Pandas",
        "description": "確認你理解 ndarray、indexing/slicing、boolean indexing、shape、axis、broadcasting、aggregation 這些核心觀念。",
        "questions": [
            Question(id="gate_np_1", concept_id="c_np_shape", qtype="predict", prompt="這段會印出什麼?", code="import numpy as np\narr = np.array([[1,2,3],[4,5,6]])\nprint(arr.shape)",
                      answer="(2, 3)", explanation="2列3欄。"),
            Question(id="gate_np_2", concept_id="c_np_indexing", qtype="bugfix", prompt="想取得所有列的第一欄,這樣寫對嗎? arr[0, :]",
                      options=[("a", "錯,應該用 arr[:, 0]"), ("b", "對"), ("c", "兩者相同"), ("d", "語法錯誤")],
                      answer="a", explanation="arr[0,:] 是第一列,arr[:,0] 才是第一欄。"),
            Question(id="gate_np_3", concept_id="c_np_boolean", qtype="bugfix", prompt="這段為什麼會報錯?", code="arr[arr > 1 and arr < 4]",
                      options=[("a", "應改用 & 並各自加括號:(arr>1) & (arr<4)"), ("b", "陣列不能比較"), ("c", "and 拼錯"), ("d", "沒有問題")],
                      answer="a", explanation="陣列布林組合要用 & / |。"),
            Question(id="gate_np_4", concept_id="c_np_axis", qtype="predict", prompt="這段會印出什麼?", code="import numpy as np\narr = np.array([[1,2],[3,4],[5,6]])\nprint(arr.sum(axis=1))",
                      answer="[ 3  7 11]", explanation="axis=1 是每列加總(NumPy 印出時會依最大數字寬度對齊)。"),
            Question(id="gate_np_5", concept_id="c_np_broadcasting", qtype="tf", prompt="判斷對錯:一個 shape (3,4) 的陣列可以直接跟純量5相加。",
                      answer="true", explanation="純量會廣播到相同形狀。"),
            Question(id="gate_np_6", concept_id="c_np_vectorization", qtype="explain", prompt="用一句話解釋為什麼向量化運算比 for 迴圈快。",
                      keywords=["底層", "快"], explanation="向量化運算交給底層批次處理,不用 Python 逐一迭代。"),
        ],
    },
}
