# -*- coding: utf-8 -*-
"""Stage 2: NumPy。重點放在 shape/axis/broadcasting/boolean indexing 這些容易『會照抄但沒真懂』的觀念。"""
from core.models import Unit, Concept, Example, Exercise, Question, CodeWalkthrough, WalkthroughStep

UNITS = [
    Unit(
        id="np_intro",
        stage="numpy",
        order=1,
        title="NumPy 是什麼、為什麼要用它",
        summary="NumPy 提供 ndarray——一種比 Python list 快得多、也更適合數值運算的陣列結構,是 Pandas 的底層基礎。",
        concepts=[
            Concept(
                id="c_np_intro",
                title="NumPy 與 ndarray",
                what="NumPy 是 Python 的數值運算套件,核心是 ndarray(N-dimensional array,多維陣列)。",
                why="Python list 每個元素可以是不同型態,彈性但慢;ndarray 要求所有元素同型態,換來大幅提升的運算速度與整欄/整批運算能力。",
                problem="解決 Python 原生 list 在大量數值運算時效能差、寫法繁瑣(要用迴圈)的問題。",
                syntax="import numpy as np\narr = np.array([1, 2, 3, 4])\nprint(arr, type(arr))",
                usage="幾乎所有數值計算函式庫(包含 Pandas)底層都是用 NumPy 陣列存資料;Pandas 的一個欄位(Series)本質上就是一個帶標籤的 NumPy 陣列。",
                common_errors="把 np.array 跟 list 混用做數學運算,忘記兩者相加行為完全不同(list 是接起來,array 是逐元素相加)。",
                confusions="array([1,2,3]) 印出來長得跟 list 很像,容易誤以為它們是同一種東西。",
            )
        ],
        examples=[
            Example(code='import numpy as np\nnums_list = [1, 2, 3]\nnums_array = np.array([1, 2, 3])\nprint(nums_list * 2)\nprint(nums_array * 2)', explain="list * 2 是複製接兩次;array * 2 是每個元素乘以2——這就是為什麼分析數值資料要用 NumPy。"),
        ],
        exercises=[
            Exercise(
                id="ex_npintro_1",
                prompt="請 import numpy as np,把 [10, 20, 30] 轉成 NumPy 陣列存成 arr,並建立 doubled,內容是 arr 每個元素乘以2的結果。",
                starter_code="# 在這裡完成\n",
                checker_code=(
                    "import json\n"
                    "import numpy as np\n"
                    "ok = 'arr' in dir() and 'doubled' in dir() and list(doubled) == [20, 40, 60]\n"
                    "print('RESULT_JSON:' + json.dumps({'passed': bool(ok), 'message': '正確!' if ok else '提示:doubled = arr * 2'}))"
                ),
                hint="import numpy as np\narr = np.array([10, 20, 30])\ndoubled = arr * 2",
            )
        ],
        questions=[
            Question(id="q_np_intro_1", concept_id="c_np_intro", qtype="predict", prompt="這段會印出什麼?", code="import numpy as np\nprint(np.array([1, 2]) + np.array([3, 4]))",
                      answer="[4 6]", explanation="NumPy 陣列相加是逐元素相加,得到 [4, 6]。"),
            Question(id="q_np_intro_2", concept_id="c_np_intro", qtype="tf", prompt="判斷對錯:[1,2,3] + [4,5,6](兩個 Python list 相加)會得到 [5,7,9]。",
                      answer="false", explanation="Python list 相加是串接,得到 [1,2,3,4,5,6],不是逐元素相加——這正是需要 NumPy 的原因。"),
        ],
    ),
    Unit(
        id="np_shape_dtype",
        stage="numpy",
        order=2,
        title="shape、ndim、dtype",
        summary="這三個屬性回答『這個陣列長什麼樣子、幾維、裡面是什麼型態』——看懂它們是讀懂任何 NumPy/Pandas 錯誤訊息的前提。",
        concepts=[
            Concept(
                id="c_np_shape",
                title="shape / ndim / dtype",
                what=".shape 回傳一個 tuple,表示陣列每個維度的大小,例如 (3, 4) 代表 3 列 4 欄;.ndim 是維度數;.dtype 是陣列內元素的型態。",
                why="幾乎所有 NumPy/Pandas 的錯誤(形狀不符、型態不對)都跟這三個屬性有關,能看懂它們才能除錯。",
                problem="讓你隨時知道手上這個陣列的『形狀』與『內容型態』,避免用錯誤的方式操作它。",
                syntax="arr = np.array([[1,2,3],[4,5,6]])\narr.shape   # (2, 3) → 2列3欄\narr.ndim    # 2\narr.dtype   # int64(依平台可能不同)",
                usage="DataFrame 的 .shape 回傳 (列數, 欄數),概念完全相同;檢查資料筆數與欄位數時第一件事通常就是看 .shape。",
                common_errors="把 shape 的 (列, 欄) 順序搞反,誤以為 (3, 4) 是『3欄4列』,正確是『3列4欄』。",
                confusions="一維陣列的 shape 是 (n,) 這種只有一個數字的 tuple,不是 (n, 1) 也不是單純的 n——很多人第一次看到 (5,) 會困惑。",
            )
        ],
        examples=[
            Example(code='import numpy as np\narr = np.array([[1, 2, 3], [4, 5, 6]])\nprint(arr.shape, arr.ndim, arr.dtype)', explain="2x3 的二維陣列,shape 是 (2, 3),ndim 是 2。"),
            Example(code='import numpy as np\narr1d = np.array([1, 2, 3])\nprint(arr1d.shape)', explain="一維陣列的 shape 是 (3,)——注意逗號,這代表『一個元素的 tuple』,不是數字 3。"),
        ],
        exercises=[
            Exercise(
                id="ex_shape_1",
                prompt="建立一個 3x2 的二維陣列 arr(內容任意),並建立 rows、cols 分別存 arr.shape[0] 和 arr.shape[1]。",
                starter_code="import numpy as np\n# 在這裡完成\n",
                checker_code=(
                    "import json\n"
                    "ok = 'arr' in dir() and 'rows' in dir() and 'cols' in dir() and rows == 3 and cols == 2 and arr.shape == (3, 2)\n"
                    "print('RESULT_JSON:' + json.dumps({'passed': bool(ok), 'message': '正確!' if ok else '提示:arr = np.array([[1,2],[3,4],[5,6]])'}))"
                ),
                hint="arr = np.array([[1,2],[3,4],[5,6]])\nrows, cols = arr.shape",
            )
        ],
        questions=[
            Question(id="q_np_shape_1", concept_id="c_np_shape", qtype="predict", prompt="這段會印出什麼?", code="import numpy as np\narr = np.array([[1,2,3,4],[5,6,7,8]])\nprint(arr.shape)",
                      answer="(2, 4)", explanation="2 列 4 欄,shape 是 (2, 4)。"),
            Question(id="q_np_shape_2", concept_id="c_np_shape", qtype="mc", prompt="np.array([1,2,3,4,5]).shape 的結果是?",
                      options=[("a", "(5,)"), ("b", "(5, 1)"), ("c", "5"), ("d", "(1, 5)")],
                      answer="a", explanation="一維陣列 shape 是 (5,) 這種單元素 tuple。"),
        ],
    ),
    Unit(
        id="np_indexing_slicing",
        stage="numpy",
        order=3,
        title="Indexing 與 Slicing",
        summary="用位置或範圍取出陣列中的一部分,是之後理解 Pandas iloc 的基礎。",
        concepts=[
            Concept(
                id="c_np_indexing",
                title="indexing 與 slicing",
                what="用 [] 搭配索引取出單一元素,或用 [start:stop] 切片取出一段;二維陣列可以用逗號同時指定列與欄,如 arr[1, 2] 或 arr[0:2, 1:3]。",
                why="需要精確存取陣列中某個位置或某個區塊的資料時使用。",
                problem="從陣列中取出你需要的部分,而不是整個陣列。",
                syntax="arr[0]      # 第一列\narr[-1]     # 最後一列\narr[1, 2]   # 第2列第3欄(索引從0開始)\narr[:, 0]   # 所有列的第1欄\narr[0:2, :] # 前兩列,所有欄",
                usage="df.iloc[0:3, 1:4] 完全沿用這套『逗號分列與欄、切片左閉右開』的邏輯,只是換成 Pandas 的 iloc。",
                common_errors="切片 [1:3] 不包含索引3;二維陣列忘記用逗號分開列與欄的索引,寫成 arr[1][2] 雖然也能用但不是慣用寫法。",
                confusions="arr[:, 0] 的冒號代表『這個維度全選』,常有人誤以為冒號是『跳過』的意思。",
            )
        ],
        examples=[
            Example(code='import numpy as np\narr = np.array([[1,2,3],[4,5,6],[7,8,9]])\nprint(arr[1, 2])\nprint(arr[:, 0])\nprint(arr[0:2, 0:2])', explain="分別取單一元素、整欄、與一個子區塊。"),
        ],
        exercises=[
            Exercise(
                id="ex_idx_1",
                prompt="給定 arr = np.array([[10,20,30],[40,50,60],[70,80,90]]),請建立 middle_col,內容是所有列的第2欄(索引1),應為 [20, 50, 80]。",
                starter_code="import numpy as np\narr = np.array([[10,20,30],[40,50,60],[70,80,90]])\n# 在這裡完成\n",
                checker_code=(
                    "import json\n"
                    "ok = 'middle_col' in dir() and list(middle_col) == [20, 50, 80]\n"
                    "print('RESULT_JSON:' + json.dumps({'passed': bool(ok), 'message': '正確!' if ok else '提示:arr[:, 1]'}))"
                ),
                hint="middle_col = arr[:, 1]",
            )
        ],
        questions=[
            Question(id="q_np_idx_1", concept_id="c_np_indexing", qtype="predict", prompt="這段會印出什麼?", code="import numpy as np\narr = np.array([[1,2],[3,4],[5,6]])\nprint(arr[1, 0])",
                      answer="3", explanation="第2列(索引1)第1欄(索引0)是 3。"),
            Question(id="q_np_idx_2", concept_id="c_np_indexing", qtype="bugfix", prompt="想取得所有列的第一欄,這樣寫對嗎? arr[0, :]",
                      options=[("a", "錯,這是取第一列所有欄,要取第一欄應寫 arr[:, 0]"), ("b", "對"), ("c", "兩者完全一樣"), ("d", "語法錯誤")],
                      answer="a", explanation="逗號前是列、逗號後是欄,arr[0,:] 是第一列,arr[:,0] 才是第一欄。"),
        ],
    ),
    Unit(
        id="np_boolean_indexing",
        stage="numpy",
        order=4,
        title="Boolean Indexing(布林索引)",
        summary="用條件式產生一整排 True/False,再用它來篩選資料——這是 df[condition] 篩選語法的底層原理。",
        concepts=[
            Concept(
                id="c_np_boolean",
                title="布林索引",
                what="對陣列做比較運算(如 arr > 5)會得到一個同樣大小、內容是 True/False 的陣列;把這個布林陣列放進 [] 裡,就會只留下 True 對應的元素。",
                why="這是從資料中『篩選符合條件的部分』最核心的機制,比寫迴圈判斷快得多也更簡潔。",
                problem="不用寫 for 迴圈加 if 判斷,就能一次篩出符合條件的資料。",
                syntax="arr = np.array([1, 5, 3, 8, 2])\nmask = arr > 3        # [False True False True False]\narr[mask]             # array([5, 8])\narr[arr > 3]          # 等同上面,常見寫法",
                usage="df[df['salary'] > 50000] 的原理完全相同:df['salary'] > 50000 先產生一整排 True/False,再拿去篩選 DataFrame 的列。",
                common_errors="想組合多個條件時用 Python 的 and/or 會報錯,陣列布林運算要用 & 和 |,並且每個條件要用括號包起來,如 (arr>3) & (arr<8)。",
                confusions="mask = arr > 3 本身還不是篩選結果,它只是一個布林陣列;要再用 arr[mask] 才真正取出資料。",
            )
        ],
        examples=[
            Example(code='import numpy as np\narr = np.array([1, 5, 3, 8, 2, 9])\nprint(arr > 4)\nprint(arr[arr > 4])', explain="先產生布林陣列,再用它篩選出真正符合條件的元素。"),
            Example(code='import numpy as np\narr = np.array([1, 5, 3, 8, 2, 9])\nprint(arr[(arr > 2) & (arr < 9)])', explain="組合兩個條件要用 & 並各自加括號,不能用 Python 的 and。"),
        ],
        exercises=[
            Exercise(
                id="ex_bool_1",
                prompt="給定 arr = np.array([12, 45, 7, 23, 9, 68]),請建立 filtered,內容是所有大於等於 20 的元素(應為 [45, 23, 68])。",
                starter_code="import numpy as np\narr = np.array([12, 45, 7, 23, 9, 68])\n# 在這裡完成\n",
                checker_code=(
                    "import json\n"
                    "ok = 'filtered' in dir() and list(filtered) == [45, 23, 68]\n"
                    "print('RESULT_JSON:' + json.dumps({'passed': bool(ok), 'message': '正確!' if ok else '提示:arr[arr >= 20]'}))"
                ),
                hint="filtered = arr[arr >= 20]",
            )
        ],
        questions=[
            Question(id="q_np_bool_1", concept_id="c_np_boolean", qtype="bugfix", prompt="這段程式碼會報錯,問題在哪?", code="import numpy as np\narr = np.array([1,2,3,4,5])\nresult = arr[arr > 1 and arr < 4]",
                      options=[("a", "陣列的布林組合要用 & 不能用 and,且各條件要加括號:(arr>1) & (arr<4)"), ("b", "arr > 1 語法錯誤"), ("c", "陣列不能比較大小"), ("d", "沒有問題")],
                      answer="a", explanation="Python 的 and/or 用於單一布林值,陣列逐元素布林運算要用 & / |。"),
            Question(id="q_np_bool_2", concept_id="c_np_boolean", qtype="predict", prompt="這段會印出什麼?", code="import numpy as np\narr = np.array([10, 20, 30])\nprint(arr > 15)",
                      answer="[False  True  True]", explanation="逐元素比較,10>15為False,20、30>15為True。"),
        ],
    ),
    Unit(
        id="np_vectorization",
        stage="numpy",
        order=5,
        title="Vectorization(向量化運算)",
        summary="直接對整個陣列做運算,取代寫迴圈逐一處理——這是 NumPy/Pandas 又快又好寫的核心原因。",
        concepts=[
            Concept(
                id="c_np_vectorization",
                title="向量化運算",
                what="對整個陣列直接做加減乘除等運算,NumPy 會自動對每個元素套用,不需要自己寫 for 迴圈。",
                why="向量化運算由 NumPy 底層用 C 語言批次執行,比 Python for 迴圈快非常多,寫法也更簡潔。",
                problem="避免用慢且冗長的 Python for 迴圈處理大量數值資料。",
                syntax="arr = np.array([1, 2, 3, 4])\narr * 2          # 不用迴圈,直接得到 [2, 4, 6, 8]\narr + arr        # 逐元素相加\nnp.sqrt(arr)     # 對每個元素開根號",
                usage="Pandas 的 df['total'] = df['price'] * df['quantity'] 就是向量化運算,一行完成『整欄相乘』,不用寫 for 迴圈逐列計算。",
                common_errors="明明可以向量化,卻還是寫 for 迴圈手動處理陣列——這在資料量大時會顯著變慢,也是初學者常見的『沒用到 NumPy 精髓』的寫法。",
                confusions="向量化運算的『向量』不是指方向的向量,而是指『整批資料一起處理』的意思。",
            )
        ],
        examples=[
            Example(code='import numpy as np\nprices = np.array([100, 200, 300])\nqty = np.array([2, 1, 3])\ntotal = prices * qty\nprint(total)', explain="兩個陣列逐元素相乘,一次算出所有商品的小計,不用迴圈。"),
        ],
        exercises=[
            Exercise(
                id="ex_vec_1",
                prompt="給定 celsius = np.array([0, 20, 37, 100]),請用向量化運算(不要用迴圈)建立 fahrenheit = celsius * 9/5 + 32。",
                starter_code="import numpy as np\ncelsius = np.array([0, 20, 37, 100])\n# 在這裡完成\n",
                checker_code=(
                    "import json\n"
                    "import numpy as np\n"
                    "expected = celsius * 9/5 + 32\n"
                    "ok = 'fahrenheit' in dir() and np.allclose(fahrenheit, expected)\n"
                    "print('RESULT_JSON:' + json.dumps({'passed': bool(ok), 'message': '正確!' if ok else '提示:直接對整個陣列做四則運算'}))"
                ),
                hint="fahrenheit = celsius * 9 / 5 + 32",
            )
        ],
        questions=[
            Question(id="q_np_vec_1", concept_id="c_np_vectorization", qtype="explain", prompt="用一句話說明,為什麼 arr * 2 比 [x*2 for x in list_version] 更適合用在大量數值資料上?",
                      keywords=["快", "底層"], explanation="向量化運算交給 NumPy 底層(C語言)批次執行,比 Python 逐一迭代快很多。"),
            Question(id="q_np_vec_2", concept_id="c_np_vectorization", qtype="predict", prompt="這段會印出什麼?", code="import numpy as np\na = np.array([1,2,3])\nb = np.array([10,20,30])\nprint(a + b)",
                      answer="[11 22 33]", explanation="逐元素相加。"),
        ],
    ),
    Unit(
        id="np_broadcasting",
        stage="numpy",
        order=6,
        title="Broadcasting(廣播)",
        summary="不同形狀的陣列也能直接運算的規則——是初學者最容易『照抄但不理解』的觀念之一。",
        concepts=[
            Concept(
                id="c_np_broadcasting",
                title="Broadcasting",
                what="當兩個陣列形狀不同時,NumPy 會嘗試依規則『擴張』較小的陣列,讓它們形狀相容後再逐元素運算,例如陣列與純量相乘、二維陣列加一維陣列。",
                why="不用手動把純量或一列資料『複製』成跟大陣列一樣的形狀,NumPy 自動處理,程式更簡潔。",
                problem="讓不同形狀但邏輯上『對得起來』的陣列可以直接運算,不用手動對齊形狀。",
                syntax="arr = np.array([[1,2,3],[4,5,6]])  # shape (2,3)\narr + 10                              # 純量廣播成 (2,3),每個元素+10\narr + np.array([1,0,1])              # shape (3,) 廣播到每一列",
                usage="df['price'] * 1.05(整欄乘以一個數字調漲5%)就是最常見的廣播應用——一個純量『廣播』成跟整欄一樣長。",
                common_errors="形狀不相容時會報 ValueError: operands could not be broadcast together——常發生在誤以為兩個陣列形狀『看起來差不多』就能直接運算。",
                confusions="廣播不是『複製資料佔用更多記憶體』,NumPy 內部是用聰明的方式模擬擴張,不會真的複製出巨大陣列。",
            )
        ],
        examples=[
            Example(code='import numpy as np\narr = np.array([[1,2,3],[4,5,6]])\nprint(arr + 10)', explain="純量 10 被廣播到陣列的每個元素。"),
            Example(code='import numpy as np\narr = np.array([[1,2,3],[4,5,6]])\nrow = np.array([10, 20, 30])\nprint(arr + row)', explain="shape (3,) 的一維陣列被廣播到 (2,3) 的每一列上,分別對應相加。"),
        ],
        exercises=[
            Exercise(
                id="ex_broadcast_1",
                prompt="給定 prices = np.array([[100, 200], [150, 250]]),請用廣播建立 adjusted,內容是每個價格都乘以 1.1(漲價10%)。",
                starter_code="import numpy as np\nprices = np.array([[100, 200], [150, 250]])\n# 在這裡完成\n",
                checker_code=(
                    "import json\n"
                    "import numpy as np\n"
                    "expected = prices * 1.1\n"
                    "ok = 'adjusted' in dir() and np.allclose(adjusted, expected)\n"
                    "print('RESULT_JSON:' + json.dumps({'passed': bool(ok), 'message': '正確!' if ok else '提示:adjusted = prices * 1.1'}))"
                ),
                hint="adjusted = prices * 1.1",
            )
        ],
        questions=[
            Question(id="q_np_bc_1", concept_id="c_np_broadcasting", qtype="bugfix", prompt="這段為什麼會報錯(ValueError)?", code="import numpy as np\na = np.array([[1,2,3],[4,5,6]])  # shape (2,3)\nb = np.array([1,2])              # shape (2,)\nprint(a + b)",
                      options=[("a", "b 的長度(2)跟 a 的欄數(3)對不上,形狀不相容,無法廣播"), ("b", "NumPy 不支援陣列相加"), ("c", "a 的形狀寫錯"), ("d", "應該用乘法不能用加法")],
                      answer="a", explanation="廣播要求維度長度相等或其中一個為1;這裡 b 長度2對不上 a 的欄數3。"),
            Question(id="q_np_bc_2", concept_id="c_np_broadcasting", qtype="tf", prompt="判斷對錯:陣列 arr(shape 為 (3,4))可以直接跟一個純量(例如 5)做運算。",
                      answer="true", explanation="純量會廣播到跟陣列相同形狀,逐元素運算。"),
        ],
    ),
    Unit(
        id="np_aggregation_axis",
        stage="numpy",
        order=7,
        title="Aggregation 與 Axis",
        summary="sum、mean、max 等統計運算,搭配 axis 參數決定『沿著哪個方向』計算——這是 groupby/欄位統計的基礎觀念。",
        concepts=[
            Concept(
                id="c_np_axis",
                title="聚合運算與 axis",
                what="常用聚合函式:.sum()、.mean()、.max()、.min()、.std()。二維陣列可以指定 axis 參數:axis=0 沿著『列的方向』計算(結果是每一欄的統計量),axis=1 沿著『欄的方向』計算(結果是每一列的統計量)。",
                why="資料通常是二維表格,常需要『每一欄的平均』或『每一列的總和』這類彙總,axis 就是用來指定方向的。",
                problem="把一堆數字彙總成一個或一組代表性的統計量。",
                syntax="arr = np.array([[1,2,3],[4,5,6]])\narr.sum()          # 全部加總,21\narr.sum(axis=0)    # 每欄加總,[5,7,9]\narr.sum(axis=1)    # 每列加總,[6,15]",
                usage="df.mean() 預設是算每一欄的平均(axis=0);df.mean(axis=1) 才是算每一列的平均——初學者非常容易搞混這兩個方向。",
                common_errors="以為 axis=0 是『橫著算』,axis=1 是『豎著算』,方向記反——正確理解是 axis=0 表示『沿著 axis 0(列的方向)壓縮』,結果保留欄。",
                confusions="記憶技巧:axis=0 消去的是第0個維度(列數),所以結果變成『每一欄一個值』;axis=1 消去第1個維度(欄數),結果變成『每一列一個值』。",
            )
        ],
        examples=[
            Example(code='import numpy as np\narr = np.array([[1,2,3],[4,5,6]])\nprint(arr.sum())\nprint(arr.sum(axis=0))\nprint(arr.sum(axis=1))', explain="全部加總、每欄加總、每列加總三種聚合方向。"),
        ],
        exercises=[
            Exercise(
                id="ex_axis_1",
                prompt="給定 scores = np.array([[80, 90], [70, 85], [95, 60]])(3位學生、2科成績),請建立 subject_avg:每一科的平均(axis=0),應約為 [81.67, 78.33]。",
                starter_code="import numpy as np\nscores = np.array([[80, 90], [70, 85], [95, 60]])\n# 在這裡完成\n",
                checker_code=(
                    "import json\n"
                    "import numpy as np\n"
                    "expected = scores.mean(axis=0)\n"
                    "ok = 'subject_avg' in dir() and np.allclose(subject_avg, expected)\n"
                    "print('RESULT_JSON:' + json.dumps({'passed': bool(ok), 'message': '正確!' if ok else '提示:scores.mean(axis=0)'}))"
                ),
                hint="subject_avg = scores.mean(axis=0)",
            )
        ],
        questions=[
            Question(id="q_np_axis_1", concept_id="c_np_axis", qtype="predict", prompt="這段會印出什麼?", code="import numpy as np\narr = np.array([[1,2],[3,4],[5,6]])\nprint(arr.sum(axis=1))",
                      answer="[ 3  7 11]", explanation="axis=1 是每列加總:1+2=3, 3+4=7, 5+6=11(NumPy 印出時會依最大數字寬度對齊,所以有多餘空白)。"),
            Question(id="q_np_axis_2", concept_id="c_np_axis", qtype="mc", prompt="想計算一個 DataFrame『每一欄』的平均值,應該用?",
                      options=[("a", "df.mean() 或 df.mean(axis=0)"), ("b", "df.mean(axis=1)"), ("c", "df.sum(axis=1)"), ("d", "df.mean(axis=2)")],
                      answer="a", explanation="axis=0(預設)是沿列方向壓縮,結果是每欄一個值。"),
        ],
    ),
    Unit(
        id="np_reshape",
        stage="numpy",
        order=8,
        title="Reshape",
        summary="改變陣列的形狀但不改變資料內容與總數量,常用在調整資料排列方式以配合特定運算或函式需求。",
        concepts=[
            Concept(
                id="c_np_reshape",
                title="reshape",
                what=".reshape(new_shape) 在不改變元素數量與順序的前提下,把陣列排成新的形狀。新形狀的元素總數必須跟原本相同。",
                why="有些函式或運算要求特定形狀的輸入(例如把一維資料轉成二維的『一欄』),reshape 用來調整成需要的樣子。",
                problem="讓資料符合特定函式或運算所需要的形狀,而不需要重新輸入資料。",
                syntax="arr = np.arange(6)          # [0,1,2,3,4,5]\narr.reshape(2, 3)            # 變成 2列3欄\narr.reshape(3, -1)           # -1 表示『自動計算這個維度』,結果是 3列2欄",
                usage="常見情境是把一維的預測結果 reshape 成二維的『一欄』(n, 1)以符合某些函式的輸入格式要求。",
                common_errors="要求的形狀元素總數對不上原陣列,例如把 6 個元素 reshape(2,4) 會報 ValueError,因為 2*4=8 ≠ 6。",
                confusions="reshape 不會『複製』資料變出新的數值,只是重新安排既有元素的排列方式。",
            )
        ],
        examples=[
            Example(code='import numpy as np\narr = np.arange(6)\nprint(arr)\nprint(arr.reshape(2, 3))\nprint(arr.reshape(3, -1))', explain="同樣 6 個元素,分別排成 2x3 和 3x2(用 -1 讓 NumPy 自動算)。"),
        ],
        exercises=[
            Exercise(
                id="ex_reshape_1",
                prompt="給定 arr = np.arange(12),請建立 grid,把它 reshape 成 3 列 4 欄。",
                starter_code="import numpy as np\narr = np.arange(12)\n# 在這裡完成\n",
                checker_code=(
                    "import json\n"
                    "ok = 'grid' in dir() and grid.shape == (3, 4)\n"
                    "print('RESULT_JSON:' + json.dumps({'passed': bool(ok), 'message': '正確!' if ok else '提示:arr.reshape(3, 4)'}))"
                ),
                hint="grid = arr.reshape(3, 4)",
            )
        ],
        questions=[
            Question(id="q_np_reshape_1", concept_id="c_np_reshape", qtype="bugfix", prompt="這段為什麼會報錯?", code="import numpy as np\narr = np.arange(7)\ngrid = arr.reshape(2, 4)",
                      options=[("a", "7 個元素無法排成 2x4=8 個位置,總數對不上"), ("b", "arange 用法錯誤"), ("c", "reshape 參數順序寫反"), ("d", "沒有問題")],
                      answer="a", explanation="reshape 前後元素總數必須相等。"),
            Question(id="q_np_reshape_2", concept_id="c_np_reshape", qtype="predict", prompt="這段會印出什麼 shape?", code="import numpy as np\narr = np.arange(10)\nprint(arr.reshape(5, -1).shape)",
                      answer="(5, 2)", explanation="10個元素分5列,每列自動算出2欄。"),
        ],
    ),
    Unit(
        id="np_nan",
        stage="numpy",
        order=9,
        title="NaN 基本處理",
        summary="真實資料常有缺失值,NumPy 用 np.nan 表示『缺失的數字』,理解它的特殊行為是資料清理的重要前置知識。",
        concepts=[
            Concept(
                id="c_np_nan",
                title="NaN(Not a Number)",
                what="np.nan 是 NumPy 用來表示『缺失/未知數值』的特殊浮點數值。任何跟 NaN 的數學運算或比較(包括 NaN == NaN)結果都是 False 或 NaN。",
                why="真實資料常有缺漏(例如問卷未填、感測器故障),需要有一個標準方式表示『這裡沒有值』,而不是用 0 或空字串魚目混珠。",
                problem="標示並處理資料中『缺失』的部分,避免缺失值被誤當成真實的 0 參與計算。",
                syntax="arr = np.array([1, 2, np.nan, 4])\nnp.isnan(arr)          # 找出哪裡是 NaN:[False False True False]\nnp.nanmean(arr)        # 忽略 NaN 計算平均\narr.sum()              # 一般 sum 遇到 NaN 結果整個變 NaN",
                usage="Pandas 讀取 CSV 時,空白儲存格預設會被讀成 NaN;df.isna()、df.dropna()、df.fillna() 都是建立在這套 NaN 機制上。",
                common_errors="用 arr == np.nan 判斷是否為 NaN 永遠是 False(NaN 不等於任何值,包括自己),必須用 np.isnan() 或 pd.isna()。",
                confusions="一般的 .sum()/.mean() 只要陣列中有一個 NaN,結果就會是 NaN;要用 np.nansum()/np.nanmean() 才會自動忽略 NaN 計算。",
            )
        ],
        examples=[
            Example(code='import numpy as np\narr = np.array([1, 2, np.nan, 4])\nprint(arr.sum())\nprint(np.nansum(arr))\nprint(np.isnan(arr))', explain="一般 sum 遇到 NaN 會整個變 NaN;nansum 會自動忽略它。"),
        ],
        exercises=[
            Exercise(
                id="ex_nan_1",
                prompt="給定 arr = np.array([10.0, np.nan, 30.0, np.nan, 50.0]),請建立 valid_mean,內容是忽略 NaN 後的平均值(應為 30.0)。",
                starter_code="import numpy as np\narr = np.array([10.0, np.nan, 30.0, np.nan, 50.0])\n# 在這裡完成\n",
                checker_code=(
                    "import json\n"
                    "ok = 'valid_mean' in dir() and abs(valid_mean - 30.0) < 1e-6\n"
                    "print('RESULT_JSON:' + json.dumps({'passed': bool(ok), 'message': '正確!' if ok else '提示:np.nanmean(arr)'}))"
                ),
                hint="valid_mean = np.nanmean(arr)",
            )
        ],
        questions=[
            Question(id="q_np_nan_1", concept_id="c_np_nan", qtype="tf", prompt="判斷對錯:np.nan == np.nan 的結果是 True。",
                      answer="false", explanation="NaN 不等於任何值,包括它自己,這是 NaN 定義上的特性。"),
            Question(id="q_np_nan_2", concept_id="c_np_nan", qtype="bugfix", prompt="這段程式碼想判斷 arr 裡哪些是缺失值,但寫錯了,該怎麼改?", code="import numpy as np\narr = np.array([1, np.nan, 3])\nmissing = arr == np.nan",
                      options=[("a", "應改用 missing = np.isnan(arr)"), ("b", "np.nan 拼錯了"), ("c", "== 應該改成 is"), ("d", "沒有問題")],
                      answer="a", explanation="判斷是否為 NaN 必須用 np.isnan(),不能用 ==。"),
        ],
    ),
    Unit(
        id="np_relation_pandas",
        stage="numpy",
        order=10,
        title="NumPy 與 list、Pandas 的關係",
        summary="收斂前面所有概念:list 是通用容器、ndarray 是數值運算的高速容器、Pandas 在 ndarray 之上加了欄名與列索引,變成表格。",
        concepts=[
            Concept(
                id="c_np_pandas_relation",
                title="list → ndarray → DataFrame 的關係",
                what="Python list 是通用、彈性但慢的容器;NumPy ndarray 要求同型態、換來高速的向量化運算;Pandas Series/DataFrame 是在 ndarray 外面加上『標籤』(索引與欄名),讓資料有了『名字』。",
                why="理解這條演進關係,能幫助你知道『為什麼 Pandas 這麼多操作看起來很像 NumPy』——因為它們背後常常就是同一套機制,只是多了標籤與表格結構。",
                problem="建立正確的心智模型,理解三種資料結構彼此的定位與差異,而不是死背個別的語法。",
                syntax="import pandas as pd\ns = pd.Series([1, 2, 3])       # 帶索引標籤的一維陣列\nprint(s.values)                # 拿出底層的 NumPy 陣列",
                usage="df['salary'].values 或 df['salary'].to_numpy() 可以直接拿到底層的 NumPy 陣列,代表 Series 本質上就是『ndarray + 索引標籤』。",
                common_errors="把三者的能力混為一談,例如以為 Python list 也能像 ndarray 一樣直接逐元素相乘。",
                confusions="Series 是一維的(像一欄),DataFrame 是二維的(像整張表);DataFrame 可以想成『很多個共用同一個列索引的 Series 並排在一起』。",
            )
        ],
        examples=[
            Example(code='import pandas as pd\ns = pd.Series([10, 20, 30])\nprint(s.values, type(s.values))', explain="Series 的 .values 拿出來就是一個 NumPy 陣列,證明 Series 底層就是 ndarray 加上索引。"),
        ],
        exercises=[
            Exercise(
                id="ex_relation_1",
                prompt="請建立 pd.Series([5, 10, 15]) 存成 s,並建立 as_array,內容是 s.values(應是一個 NumPy 陣列,值為 [5,10,15])。",
                starter_code="import pandas as pd\nimport numpy as np\n# 在這裡完成\n",
                checker_code=(
                    "import json\n"
                    "import numpy as np\n"
                    "ok = 's' in dir() and 'as_array' in dir() and isinstance(as_array, np.ndarray) and list(as_array) == [5, 10, 15]\n"
                    "print('RESULT_JSON:' + json.dumps({'passed': bool(ok), 'message': '正確!' if ok else '提示:as_array = s.values'}))"
                ),
                hint="s = pd.Series([5, 10, 15])\nas_array = s.values",
            )
        ],
        questions=[
            Question(id="q_np_rel_1", concept_id="c_np_pandas_relation", qtype="mc", prompt="下列敘述何者正確?",
                      options=[("a", "Pandas 的 Series 本質上是 NumPy 陣列加上索引標籤"), ("b", "NumPy 陣列可以像 list 一樣放不同型態的元素而不影響效能"), ("c", "Pandas 完全不依賴 NumPy"), ("d", "Series 是二維的,DataFrame 是一維的")],
                      answer="a", explanation="Series = 帶標籤的一維陣列,底層就是 ndarray。"),
            Question(id="q_np_rel_2", concept_id="c_np_pandas_relation", qtype="short", prompt="用一句話說明 DataFrame 和 Series 的維度關係。",
                      keywords=["二維", "一維"], explanation="Series 是一維(像一欄),DataFrame 是二維(像整張表,多個 Series 並排)。"),
        ],
    ),
]
