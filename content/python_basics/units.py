# -*- coding: utf-8 -*-
"""Stage 1: Python 基礎。只涵蓋未來學 NumPy/Pandas 真正需要的子集。"""
from core.models import Unit, Concept, Example, Exercise, Question

UNITS = [
    Unit(
        id="py_variables",
        stage="python",
        order=1,
        title="變數與基本資料型態",
        summary="int、float、str、bool 是後面所有資料分析的最小單位——DataFrame 裡的每一格,本質上都是這幾種型態之一。",
        concepts=[
            Concept(
                id="c_variables",
                title="變數與型態",
                what="變數是一個名字,指向記憶體中的一個值。Python 的基本型態有整數 int、浮點數 float、字串 str、布林值 bool。",
                why="資料分析時,一個欄位裡的值一定是某種型態,型態判斷錯誤會導致計算錯誤或程式報錯(例如把字串當數字相加)。",
                problem="讓程式可以命名、記住、重複使用一個值,而不用每次都寫死。",
                syntax="name = value  # 例如 age = 25, price = 19.9, city = \"Taipei\", is_valid = True\n用 type(x) 可以查看型態。",
                usage="Pandas 讀入 CSV 後,每個欄位(Series)的 dtype 就是由裡面的值的型態決定的;分不清 int 和 str 是初學者最常見的資料清理地雷。",
                common_errors="把數字字串當數字運算,例如 \"5\" + 3 會報錯(TypeError),因為字串不能直接跟整數相加。",
                confusions="int 和 float 相除在 Python 3 一定得到 float(例如 7 / 2 == 3.5);想要整數除法要用 //。",
            )
        ],
        examples=[
            Example(
                code='age = 25\nprice = 19.9\ncity = "Taipei"\nis_valid = True\nprint(type(age), type(price), type(city), type(is_valid))',
                explain="分別建立四種基本型態的變數,並用 type() 確認型態。",
            ),
            Example(
                code='count_text = "5"\ncount_number = int(count_text)\nprint(count_number + 3)',
                explain="用 int() 把字串轉成整數,這是讀取 CSV 後常見的型態轉換動作。",
            ),
        ],
        exercises=[
            Exercise(
                id="ex_variables_1",
                prompt="請建立一個變數 quantity,把字串 \"12\" 轉成整數後存進去,再建立變數 unit_price = 8.5,最後把 total = quantity * unit_price 印出來。",
                starter_code='quantity_text = "12"\n# 在這裡完成\n',
                checker_code=(
                    "import json\n"
                    "ok = 'quantity' in dir() and 'unit_price' in dir() and 'total' in dir()\n"
                    "ok = ok and quantity == 12 and unit_price == 8.5 and abs(total - 102.0) < 1e-6\n"
                    "print('RESULT_JSON:' + json.dumps({'passed': bool(ok), 'message': '正確!total 應為 102.0' if ok else '請確認 quantity 已轉成整數 12,且 total = quantity * unit_price'}))"
                ),
                hint="quantity = int(quantity_text)\nunit_price = 8.5\ntotal = quantity * unit_price",
            )
        ],
        questions=[
            Question(
                id="q_py_var_1", concept_id="c_variables", qtype="predict",
                prompt="這段程式碼會印出什麼?", code='print(type(7 / 2))',
                answer="<class 'float'>", explanation="Python 3 的 / 一律回傳 float,即使可以整除。",
            ),
            Question(
                id="q_py_var_2", concept_id="c_variables", qtype="bugfix",
                prompt="這段程式碼會報錯,錯誤原因是什麼?", code='x = "3"\ny = x + 2',
                options=[("a", "字串不能跟整數直接相加,要先用 int(x) 轉型"), ("b", "變數名稱 x 不能用"), ("c", "數字不能放進字串"), ("d", "Python 不支援加法")],
                answer="a", explanation="\"3\" 是字串,+ 2 前需要先轉型:int(x) + 2。",
            ),
            Question(
                id="q_py_var_3", concept_id="c_variables", qtype="tf",
                prompt="判斷對錯:type(10) 和 type(10.0) 是一樣的。",
                answer="false", explanation="10 是 int,10.0 是 float,是不同型態。",
            ),
        ],
    ),
    Unit(
        id="py_operators",
        stage="python",
        order=2,
        title="數值運算與運算子",
        summary="+ - * / // % ** 以及比較運算子,是之後寫篩選條件、算統計量的基礎。",
        concepts=[
            Concept(
                id="c_operators",
                title="運算子",
                what="算術運算子:+ - * / // % **;比較運算子:== != > < >= <=;邏輯運算子:and or not。",
                why="篩選資料(例如「薪水大於 5 萬」)、計算衍生欄位,全部都要靠運算子組合條件與算式。",
                problem="讓程式能做數學計算與邏輯判斷。",
                syntax="a // b 取整除,a % b 取餘數,a ** b 次方。比較會回傳 True/False。",
                usage="df[df[\"salary\"] > 50000] 這種 Pandas 篩選語法,骨子裡就是比較運算子回傳的布林值。",
                common_errors="把 = (賦值) 和 == (比較) 搞混,例如 if x = 5 是語法錯誤,應為 if x == 5。",
                confusions="and/or 是關鍵字,不是 &&/||;-7 // 2 的結果是 -4(向下取整),不是直覺的 -3。",
            )
        ],
        examples=[
            Example(code='print(17 // 5, 17 % 5, 2 ** 10)', explain="整除、取餘數、次方運算。"),
            Example(code='age = 20\nprint(age >= 18 and age < 65)', explain="用 and 組合兩個條件,結果是 True/False。"),
        ],
        exercises=[
            Exercise(
                id="ex_operators_1",
                prompt="有 37 顆蘋果,每箱裝 5 顆。請計算可以裝滿幾箱(存成 full_boxes),還剩幾顆(存成 remainder)。",
                starter_code="apples = 37\nbox_size = 5\n# 在這裡完成\n",
                checker_code=(
                    "import json\n"
                    "ok = 'full_boxes' in dir() and 'remainder' in dir() and full_boxes == 7 and remainder == 2\n"
                    "print('RESULT_JSON:' + json.dumps({'passed': bool(ok), 'message': '正確!7 箱又剩 2 顆' if ok else '用 // 取箱數、% 取餘數'}))"
                ),
                hint="full_boxes = apples // box_size\nremainder = apples % box_size",
            )
        ],
        questions=[
            Question(id="q_py_op_1", concept_id="c_operators", qtype="predict", prompt="這段會印出什麼?", code="print(-7 // 2)", answer="-4", explanation="// 是向下取整,不是直接捨去小數。"),
            Question(id="q_py_op_2", concept_id="c_operators", qtype="mc", prompt="想判斷 x 是否「介於 10 和 20 之間(含)」,正確寫法是?",
                      options=[("a", "10 <= x <= 20"), ("b", "10 < x < 20 = True"), ("c", "x = 10 to 20"), ("d", "x >< (10, 20)")],
                      answer="a", explanation="Python 支援串接比較 10 <= x <= 20。"),
            Question(id="q_py_op_3", concept_id="c_operators", qtype="bugfix", prompt="這段程式碼哪裡錯了?", code="if age = 18:\n    print('adult')",
                      options=[("a", "= 應改成 =="), ("b", "if 拼錯"), ("c", "缺少 else"), ("d", "18 要加引號")],
                      answer="a", explanation="判斷相等要用 ==,= 是賦值。"),
        ],
    ),
    Unit(
        id="py_strings",
        stage="python",
        order=3,
        title="字串基礎",
        summary="字串是資料清理中最常打交道的型態:欄位名稱不一致、多餘空白、大小寫問題都靠字串方法處理。",
        concepts=[
            Concept(
                id="c_strings",
                title="字串與常用方法",
                what="字串是用 \"\" 或 '' 包起來的文字。常用方法:.strip() 去除頭尾空白、.lower()/.upper() 轉大小寫、.split() 切割、.replace() 取代、f-string 格式化。",
                why="真實資料常有「 Taipei 」「TAIPEI」「taipei」這種同義不同形式的字串,分析前需要先統一格式。",
                problem="處理、清理、組合文字資料。",
                syntax='name = "  Alice  "\nname.strip()  # "Alice"\nf"Hello {name}"  # 格式化字串',
                usage="Pandas 的 str accessor(如 df['city'].str.strip().str.lower())本質上就是把這些字串方法套用到整欄。",
                common_errors="忘記字串方法不會修改原字串,而是回傳新字串,例如只寫 name.strip() 而沒有 name = name.strip()。",
                confusions="len(\"123\") 是 3(字數),不是數值 123 本身;字串索引從 0 開始。",
            )
        ],
        examples=[
            Example(code='s = "  Taipei City  "\nprint(s.strip().lower())', explain="去除頭尾空白後轉小寫,得到 'taipei city'。"),
            Example(code='name = "Alice"\nscore = 90\nprint(f"{name} got {score} points")', explain="f-string 是最常用的字串格式化方式。"),
        ],
        exercises=[
            Exercise(
                id="ex_strings_1",
                prompt="給定 raw = \"  New York \",請建立 cleaned,內容是去除頭尾空白並轉成全小寫的結果(應為 'new york')。",
                starter_code='raw = "  New York "\n# 在這裡完成\n',
                checker_code=(
                    "import json\n"
                    "ok = 'cleaned' in dir() and cleaned == 'new york'\n"
                    "print('RESULT_JSON:' + json.dumps({'passed': bool(ok), 'message': '正確!' if ok else \"cleaned 應為 'new york'\"}))"
                ),
                hint="cleaned = raw.strip().lower()",
            )
        ],
        questions=[
            Question(id="q_py_str_1", concept_id="c_strings", qtype="predict", prompt="這段會印出什麼?", code='print("Data,Analysis,Python".split(","))',
                      answer="['Data', 'Analysis', 'Python']", explanation="split(',') 依逗號切成 list。"),
            Question(id="q_py_str_2", concept_id="c_strings", qtype="tf", prompt="判斷對錯:執行 name.strip() 後,原本的 name 變數本身也會被改變。",
                      answer="false", explanation="字串是不可變的,方法回傳新字串,不會修改原變數,除非重新賦值。"),
            Question(id="q_py_str_3", concept_id="c_strings", qtype="fill", prompt="請填空,讓程式印出 'ALICE': name = 'alice'\nprint(name.____())",
                      answer="upper", explanation="upper() 轉成大寫。"),
        ],
    ),
    Unit(
        id="py_list",
        stage="python",
        order=4,
        title="List(串列)",
        summary="list 是一整排可變動的值,概念上就是「一欄資料」的雛形,是理解 NumPy 陣列與 Pandas Series 的第一步。",
        concepts=[
            Concept(
                id="c_list",
                title="list 基本操作",
                what="list 用 [] 表示,可以放多個值,可修改、新增、刪除,用索引([0]、[-1])或切片([1:3])取值。",
                why="很多資料一開始就是以 list 形式出現(例如一次讀入多筆數字),之後轉成 NumPy array / Pandas Series 都是以 list 為起點。",
                problem="儲存與操作一組有順序的資料。",
                syntax="nums = [3, 1, 4, 1, 5]\nnums.append(9)\nnums[0]  # 3\nnums[-1]  # 最後一個\nnums[1:3]  # 切片,索引1到2",
                usage="pd.Series([1,2,3]) 或 np.array([1,2,3]) 都是直接把 list 包裝成分析用的資料結構。",
                common_errors="索引超出範圍(IndexError);以為切片 [1:3] 會包含索引3,其實不包含(左閉右開)。",
                confusions="list 是可變的(mutable),跟之後會學到的 tuple(不可變)不同;+ 用在 list 上是接起來而不是相加。",
            )
        ],
        examples=[
            Example(code='scores = [88, 92, 75, 100]\nscores.append(60)\nprint(scores[0], scores[-1], scores[1:3])', explain="新增元素、取第一個/最後一個、切片取一段。"),
            Example(code='a = [1, 2]\nb = [3, 4]\nprint(a + b)', explain="list 的 + 是串接,得到 [1, 2, 3, 4],不是元素相加(這正是 NumPy 陣列存在的原因之一)。"),
        ],
        exercises=[
            Exercise(
                id="ex_list_1",
                prompt="給定 prices = [12, 45, 7, 23, 9],請計算 total(總和)和 highest(最大值),並建立 top_two,內容是排序後(由大到小)的前兩個價格。",
                starter_code="prices = [12, 45, 7, 23, 9]\n# 在這裡完成\n",
                checker_code=(
                    "import json\n"
                    "ok = 'total' in dir() and 'highest' in dir() and 'top_two' in dir()\n"
                    "ok = ok and total == 96 and highest == 45 and top_two == [45, 23]\n"
                    "print('RESULT_JSON:' + json.dumps({'passed': bool(ok), 'message': '正確!' if ok else '提示:sum()、max()、sorted(prices, reverse=True)[:2]'}))"
                ),
                hint="total = sum(prices)\nhighest = max(prices)\ntop_two = sorted(prices, reverse=True)[:2]",
            )
        ],
        questions=[
            Question(id="q_py_list_1", concept_id="c_list", qtype="predict", prompt="這段會印出什麼?", code="nums = [10, 20, 30, 40]\nprint(nums[1:3])",
                      answer="[20, 30]", explanation="切片左閉右開,[1:3] 取索引1、2。"),
            Question(id="q_py_list_2", concept_id="c_list", qtype="bugfix", prompt="這段程式碼想取得最後一個元素,但寫錯了,問題出在哪?", code="nums = [1, 2, 3]\nprint(nums[3])",
                      options=[("a", "索引超出範圍,最後一個應該是 nums[2] 或 nums[-1]"), ("b", "list 不能用中括號取值"), ("c", "應該用 nums(3)"), ("d", "沒有問題")],
                      answer="a", explanation="長度為3的 list,合法索引是 0,1,2 或 -1,-2,-3。"),
            Question(id="q_py_list_3", concept_id="c_list", qtype="tf", prompt="判斷對錯:[1,2] + [3,4] 會得到 [4,6]。",
                      answer="false", explanation="list 相加是串接,結果是 [1,2,3,4],不是逐項相加——這正是為什麼分析數值資料要改用 NumPy 陣列。"),
        ],
    ),
    Unit(
        id="py_tuple_set",
        stage="python",
        order=5,
        title="Tuple 與 Set",
        summary="tuple 是不可變的序列,set 是不重複的集合——兩者在資料分析中常用於「固定不變的設定值」與「去重複」。",
        concepts=[
            Concept(
                id="c_tuple_set",
                title="tuple 與 set",
                what="tuple 用 () 表示,建立後不能修改;set 用 {} 或 set() 表示,元素不重複、沒有順序。",
                why="tuple 適合表示「固定組合」(如座標、shape);set 適合快速判斷「有沒有出現過」或「去除重複值」。",
                problem="tuple 保障資料不被意外修改;set 解決「有哪些不重複的類別」這類問題。",
                syntax="point = (3, 4)\ncities = {\"Taipei\", \"Tainan\", \"Taipei\"}  # 自動變成只有兩個元素",
                usage="NumPy 陣列的 .shape 回傳的就是 tuple,例如 (3, 4) 代表 3 列 4 欄;set 常用來快速找出一欄裡有哪些不重複的類別值。",
                common_errors="嘗試修改 tuple 的元素(如 point[0] = 5)會報 TypeError,因為 tuple 不可變。",
                confusions="{} 單獨使用建立的是空 dict 而不是空 set,空 set 要寫 set()。",
            )
        ],
        examples=[
            Example(code='shape = (3, 4)\nprint(shape[0], shape[1])', explain="用索引讀取 tuple 內容,跟 list 讀法一樣,但不能修改。"),
            Example(code='cities = ["Taipei", "Tainan", "Taipei", "Taichung"]\nunique_cities = set(cities)\nprint(unique_cities)', explain="用 set() 把 list 轉成集合,自動去除重複值。"),
        ],
        exercises=[
            Exercise(
                id="ex_tuple_set_1",
                prompt="給定 tags = ['a','b','a','c','b','d'],請建立 unique_count,內容是不重複標籤的數量(應為 4)。",
                starter_code="tags = ['a','b','a','c','b','d']\n# 在這裡完成\n",
                checker_code=(
                    "import json\n"
                    "ok = 'unique_count' in dir() and unique_count == 4\n"
                    "print('RESULT_JSON:' + json.dumps({'passed': bool(ok), 'message': '正確!' if ok else '提示:len(set(tags))'}))"
                ),
                hint="unique_count = len(set(tags))",
            )
        ],
        questions=[
            Question(id="q_py_ts_1", concept_id="c_tuple_set", qtype="bugfix", prompt="這段為什麼會報錯?", code="point = (1, 2)\npoint[0] = 5",
                      options=[("a", "tuple 建立後不能修改元素"), ("b", "point 命名不合法"), ("c", "括號用錯"), ("d", "缺少 import")],
                      answer="a", explanation="tuple 是不可變型態。"),
            Question(id="q_py_ts_2", concept_id="c_tuple_set", qtype="predict", prompt="這段會印出什麼(元素順序不重要)?", code="print(len({1, 2, 2, 3, 3, 3}))",
                      answer="3", explanation="set 自動去重,{1,2,2,3,3,3} 只剩 {1,2,3}。"),
            Question(id="q_py_ts_3", concept_id="c_tuple_set", qtype="tf", prompt="判斷對錯:NumPy 陣列的 .shape 屬性回傳的是 list。",
                      answer="false", explanation="shape 回傳的是 tuple,例如 (3, 4)。"),
        ],
    ),
    Unit(
        id="py_dict",
        stage="python",
        order=6,
        title="Dict(字典)",
        summary="dict 用 key 對應 value,概念上就是「欄位名稱對應一整欄資料」——DataFrame 本質上就是一個欄名對應 Series 的 dict。",
        concepts=[
            Concept(
                id="c_dict",
                title="dict 基本操作",
                what="dict 用 {key: value, ...} 表示,用 key 存取對應的 value,可新增/修改/刪除。",
                why="dict 是「有名字的資料」最自然的表示法,例如 {'name': 'Alice', 'age': 25} 代表一筆記錄。",
                problem="用有意義的名字(而不是數字索引)來組織與查找資料。",
                syntax="person = {\"name\": \"Alice\", \"age\": 25}\nperson[\"age\"]  # 25\nperson[\"city\"] = \"Taipei\"  # 新增\nperson.get(\"job\", \"未知\")  # 安全取值,不存在時給預設值",
                usage="pd.DataFrame({'name': ['Alice','Bob'], 'age': [25,30]}) 就是用 dict(欄名對應一整欄的值)來建立表格,這是最常見的 DataFrame 建立方式之一。",
                common_errors="用 [] 存取不存在的 key 會報 KeyError,應該用 .get(key, 預設值) 來避免。",
                confusions="dict 從 Python 3.7 起會保留插入順序,但邏輯上不該依賴順序來查資料,應該用 key。",
            )
        ],
        examples=[
            Example(code='student = {"name": "Bob", "score": 88}\nprint(student["name"], student.get("grade", "未評分"))', explain="用 [] 取一定存在的 key,用 .get() 安全取可能不存在的 key。"),
            Example(code='data = {"name": ["Alice", "Bob"], "age": [25, 30]}\nprint(data["age"])', explain="這種「欄名對應一整欄 list」的結構,正是 pd.DataFrame() 最常見的輸入格式。"),
        ],
        exercises=[
            Exercise(
                id="ex_dict_1",
                prompt="給定 record = {'name': 'Alice', 'age': 25},請新增一個 key 'city',值為 'Taipei',並建立 age_next_year,內容是 record['age'] + 1。",
                starter_code="record = {'name': 'Alice', 'age': 25}\n# 在這裡完成\n",
                checker_code=(
                    "import json\n"
                    "ok = record.get('city') == 'Taipei' and 'age_next_year' in dir() and age_next_year == 26\n"
                    "print('RESULT_JSON:' + json.dumps({'passed': bool(ok), 'message': '正確!' if ok else \"提示:record['city'] = 'Taipei'\"}))"
                ),
                hint="record['city'] = 'Taipei'\nage_next_year = record['age'] + 1",
            )
        ],
        questions=[
            Question(id="q_py_dict_1", concept_id="c_dict", qtype="bugfix", prompt="這段程式碼可能會報 KeyError,該怎麼改比較安全?", code="student = {'name': 'Bob'}\nprint(student['score'])",
                      options=[("a", "改用 student.get('score', 0) 給預設值"), ("b", "改用 student['score'] = 0 才能讀取"), ("c", "dict 不能用中括號讀取"), ("d", "沒有問題"),],
                      answer="a", explanation="key 不存在時 [] 會報錯,.get() 可以給預設值避免程式中斷。"),
            Question(id="q_py_dict_2", concept_id="c_dict", qtype="predict", prompt="這段會印出什麼?", code="d = {'a': 1, 'b': 2}\nd['c'] = 3\nprint(len(d))",
                      answer="3", explanation="新增一個 key 後,dict 有 3 組 key-value。"),
            Question(id="q_py_dict_3", concept_id="c_dict", qtype="short", prompt="用一句話說明,為什麼 dict 很適合用來建立 Pandas DataFrame?",
                      keywords=["欄", "對應", "key"], explanation="因為 dict 的 key 可以對應「欄名」,value(一個 list)對應「該欄所有的值」,結構剛好符合表格。"),
        ],
    ),
    Unit(
        id="py_conditionals",
        stage="python",
        order=7,
        title="if / elif / else 條件判斷",
        summary="條件判斷是所有「篩選資料」邏輯的基礎,不管是寫在迴圈裡,還是之後理解 df[condition] 的原理都要靠它。",
        concepts=[
            Concept(
                id="c_conditionals",
                title="條件判斷",
                what="if 條件成立時執行一個區塊;elif 是「否則如果」;else 是「以上皆非時」執行。",
                why="資料分析常需要依條件分類或篩選,例如「薪水 > 5萬 標記為高薪」。",
                problem="讓程式依不同情況執行不同邏輯。",
                syntax="if score >= 90:\n    grade = \"A\"\nelif score >= 60:\n    grade = \"B\"\nelse:\n    grade = \"C\"",
                usage="Pandas 的 df['salary'] > 50000 會對整欄每個值做這種判斷,回傳一整欄 True/False,再用來篩選資料列。",
                common_errors="縮排錯誤(Python 用縮排決定區塊範圍,不是用 {});忘記 elif 要接在 if 之後,不能單獨使用。",
                confusions="多個 elif 由上而下比對,一旦符合就不會再往下比對其他條件。",
            )
        ],
        examples=[
            Example(code='score = 75\nif score >= 90:\n    grade = "A"\nelif score >= 60:\n    grade = "B"\nelse:\n    grade = "C"\nprint(grade)', explain="依分數落點決定等第,只會進入第一個成立的分支。"),
        ],
        exercises=[
            Exercise(
                id="ex_cond_1",
                prompt="給定 temperature = 32,請建立 comment:溫度 >= 30 時為 '炎熱',介於 20(含)到 30(不含)為 '舒適',否則為 '寒冷'。",
                starter_code="temperature = 32\n# 在這裡完成\n",
                checker_code=(
                    "import json\n"
                    "ok = 'comment' in dir() and comment == '炎熱'\n"
                    "print('RESULT_JSON:' + json.dumps({'passed': bool(ok), 'message': '正確!' if ok else '提示:先判斷 >= 30 的情況'}))"
                ),
                hint="if temperature >= 30:\n    comment = '炎熱'\nelif temperature >= 20:\n    comment = '舒適'\nelse:\n    comment = '寒冷'",
            )
        ],
        questions=[
            Question(id="q_py_cond_1", concept_id="c_conditionals", qtype="predict", prompt="這段會印出什麼?", code="x = 5\nif x > 10:\n    print('A')\nelif x > 3:\n    print('B')\nelse:\n    print('C')",
                      answer="B", explanation="x=5 不大於10,但大於3,進入第二個分支。"),
            Question(id="q_py_cond_2", concept_id="c_conditionals", qtype="tf", prompt="判斷對錯:一個 if/elif/elif/else 結構中,可能同時執行兩個分支的內容。",
                      answer="false", explanation="由上而下比對,只會執行第一個成立的分支。"),
        ],
    ),
    Unit(
        id="py_loops",
        stage="python",
        order=8,
        title="for、range、while",
        summary="迴圈讓程式重複處理資料——理解 for 迴圈,是理解 NumPy「向量化為什麼比迴圈快」的重要對照組。",
        concepts=[
            Concept(
                id="c_loops",
                title="for 迴圈與 while 迴圈",
                what="for 用來走訪一個序列(list、字串、range 等)中的每個元素;while 在條件成立時持續重複執行;range(n) 產生 0 到 n-1 的數字序列。",
                why="要對一堆資料逐筆處理(加總、篩選、轉換),迴圈是最直接的做法。",
                problem="重複執行一段邏輯,直到走完資料或條件不成立。",
                syntax="for x in [1, 2, 3]:\n    print(x)\nfor i in range(5):\n    print(i)\ni = 0\nwhile i < 3:\n    i += 1",
                usage="用 for 迴圈逐一加總 list 裡的數字,對比 NumPy 用 array.sum() 不寫迴圈就完成同樣的事、而且快很多——這是後面學 vectorization 時最重要的對照。",
                common_errors="while 迴圈忘記更新條件變數,會造成無窮迴圈,程式永遠不會結束。",
                confusions="range(5) 產生的是 0,1,2,3,4,不包含 5;range(1, 5) 才是從 1 開始。",
            )
        ],
        examples=[
            Example(code='total = 0\nfor x in [3, 5, 7]:\n    total += x\nprint(total)', explain="用 for 迴圈手動加總,結果是 15——這是 NumPy sum() 內部概念上在做的事。"),
            Example(code='for i in range(3):\n    print(f"第 {i} 輪")', explain="range(3) 依序給出 0、1、2。"),
        ],
        exercises=[
            Exercise(
                id="ex_loops_1",
                prompt="給定 nums = [4, 8, 15, 16, 23, 42],請用 for 迴圈計算 even_sum:所有偶數的總和(應為 4+8+16+42=70)。",
                starter_code="nums = [4, 8, 15, 16, 23, 42]\neven_sum = 0\n# 在這裡完成\n",
                checker_code=(
                    "import json\n"
                    "ok = 'even_sum' in dir() and even_sum == 70\n"
                    "print('RESULT_JSON:' + json.dumps({'passed': bool(ok), 'message': '正確!' if ok else '提示:if x % 2 == 0'}))"
                ),
                hint="for x in nums:\n    if x % 2 == 0:\n        even_sum += x",
            )
        ],
        questions=[
            Question(id="q_py_loop_1", concept_id="c_loops", qtype="predict", prompt="這段會印出什麼?", code="total = 0\nfor i in range(1, 4):\n    total += i\nprint(total)",
                      answer="6", explanation="range(1,4) 是 1,2,3,總和為 6。"),
            Question(id="q_py_loop_2", concept_id="c_loops", qtype="bugfix", prompt="這段程式碼會無窮迴圈,問題在哪?", code="i = 0\nwhile i < 5:\n    print(i)",
                      options=[("a", "迴圈裡沒有更新 i,條件永遠成立"), ("b", "while 語法錯誤"), ("c", "print 不能放在 while 裡"), ("d", "i 應該從 1 開始")],
                      answer="a", explanation="缺少 i += 1,i 永遠是 0,條件 i<5 永遠成立。"),
            Question(id="q_py_loop_3", concept_id="c_loops", qtype="short", prompt="簡述:為什麼之後學 NumPy 會說『向量化運算比 for 迴圈快』?",
                      keywords=["迴圈", "整"], explanation="向量化運算把整個陣列一次交給底層(C語言)批次處理,不用 Python 逐一迴圈,速度快很多。"),
        ],
    ),
    Unit(
        id="py_functions",
        stage="python",
        order=9,
        title="Function(函式)",
        summary="把一段邏輯包成可重複呼叫的函式,是寫資料清理/轉換流程時避免重複貼上程式碼的關鍵能力。",
        concepts=[
            Concept(
                id="c_functions",
                title="函式定義與呼叫",
                what="用 def 定義函式,可以接收參數(輸入)、用 return 回傳結果(輸出)。",
                why="同一段邏輯(例如清理一個字串欄位)常常要套用很多次,寫成函式可以重複使用、方便測試與除錯。",
                problem="把邏輯封裝、命名、重複使用,避免同樣的程式碼複製貼上很多份。",
                syntax="def clean_name(name):\n    return name.strip().lower()\n\nresult = clean_name(\"  Alice \")",
                usage="Pandas 的 df['col'].apply(my_function) 就是把你自訂的函式套用到整欄的每一個值上。",
                common_errors="忘記寫 return,函式執行完會回傳 None,呼叫端拿到的值就會是 None 而不是預期結果。",
                confusions="函式內部定義的變數(區域變數)在函式外部無法直接存取,跟函式外面的同名變數是不同的東西。",
            )
        ],
        examples=[
            Example(code='def celsius_to_fahrenheit(c):\n    return c * 9 / 5 + 32\n\nprint(celsius_to_fahrenheit(30))', explain="定義一個轉換攝氏到華氏的函式,並呼叫它。"),
        ],
        exercises=[
            Exercise(
                id="ex_func_1",
                prompt="請定義函式 discount_price(price, rate),回傳打折後的價格(price * (1 - rate)),再呼叫 discount_price(100, 0.2) 存入變數 result(應為 80.0)。",
                starter_code="# 在這裡完成\n",
                checker_code=(
                    "import json\n"
                    "ok = 'discount_price' in dir() and 'result' in dir() and abs(result - 80.0) < 1e-6\n"
                    "print('RESULT_JSON:' + json.dumps({'passed': bool(ok), 'message': '正確!' if ok else '記得要 return,並呼叫函式存入 result'}))"
                ),
                hint="def discount_price(price, rate):\n    return price * (1 - rate)\n\nresult = discount_price(100, 0.2)",
            )
        ],
        questions=[
            Question(id="q_py_func_1", concept_id="c_functions", qtype="bugfix", prompt="這個函式呼叫後,result 會是什麼?", code="def add(a, b):\n    c = a + b\nresult = add(2, 3)\nprint(result)",
                      options=[("a", "None,因為函式沒有 return"), ("b", "5"), ("c", "報錯"), ("d", "0")],
                      answer="a", explanation="函式內只計算了 c,沒有 return,所以呼叫端拿到 None。"),
            Question(id="q_py_func_2", concept_id="c_functions", qtype="predict", prompt="這段會印出什麼?", code="def square(x):\n    return x * x\nprint(square(4) + square(2))",
                      answer="20", explanation="16 + 4 = 20。"),
        ],
    ),
    Unit(
        id="py_comprehension",
        stage="python",
        order=10,
        title="List Comprehension",
        summary="一行寫完「對每個元素做某件事」的迴圈寫法,是閱讀他人資料處理程式碼時常見的簡潔語法。",
        concepts=[
            Concept(
                id="c_comprehension",
                title="List Comprehension",
                what="用一行語法建立新 list:[運算式 for 變數 in 可疊代物件 (if 條件)],等同於一個簡化的 for 迴圈 + append。",
                why="比寫多行 for 迴圈更精簡,在資料處理程式碼中非常常見,看得懂是閱讀他人程式碼的基本能力。",
                problem="用更精簡的語法,從一個既有序列快速產生一個新序列。",
                syntax="squares = [x**2 for x in range(5)]\nevens = [x for x in range(10) if x % 2 == 0]",
                usage="等同於 NumPy 向量化運算的『手動版』,例如 [x*2 for x in nums] 對比 np.array(nums) * 2——理解這行程式碼有助於理解向量化為何更快、更簡潔。",
                common_errors="把 for 和 if 的順序寫反,或忘記中括號 [],comprehension 的中括號決定了結果是 list。",
                confusions="comprehension 讀起來像英文『取 x 的平方,對每個 x,從 range(5) 裡』——熟悉這個閱讀順序有助於快速理解。",
            )
        ],
        examples=[
            Example(code='nums = [1, 2, 3, 4, 5]\nsquares = [x ** 2 for x in nums]\nprint(squares)', explain="對每個元素平方,結果 [1, 4, 9, 16, 25]。"),
            Example(code='nums = range(10)\nevens = [x for x in nums if x % 2 == 0]\nprint(evens)', explain="只保留偶數,結果 [0, 2, 4, 6, 8]。"),
        ],
        exercises=[
            Exercise(
                id="ex_comp_1",
                prompt="給定 words = ['data', 'python', 'ai'],請用一行 list comprehension 建立 lengths,內容是每個字串的長度(應為 [4, 6, 2])。",
                starter_code="words = ['data', 'python', 'ai']\n# 在這裡完成\n",
                checker_code=(
                    "import json\n"
                    "ok = 'lengths' in dir() and lengths == [4, 6, 2]\n"
                    "print('RESULT_JSON:' + json.dumps({'passed': bool(ok), 'message': '正確!' if ok else '提示:[len(w) for w in words]'}))"
                ),
                hint="lengths = [len(w) for w in words]",
            )
        ],
        questions=[
            Question(id="q_py_comp_1", concept_id="c_comprehension", qtype="predict", prompt="這段會印出什麼?", code="print([x for x in range(6) if x % 3 == 0])",
                      answer="[0, 3]", explanation="range(6) 是 0~5,其中 3 的倍數是 0 和 3。"),
            Question(id="q_py_comp_2", concept_id="c_comprehension", qtype="explain", prompt="用一句話解釋 [x*2 for x in range(3)] 在做什麼。",
                      keywords=["每個", "2"], explanation="對 range(3) 裡的每個數字乘以2,產生新 list [0, 2, 4]。"),
        ],
    ),
    Unit(
        id="py_exceptions",
        stage="python",
        order=11,
        title="Exception 基礎",
        summary="真實資料常有意外狀況(格式錯誤、缺值),try/except 讓程式在遇到錯誤時不會直接崩潰。",
        concepts=[
            Concept(
                id="c_exceptions",
                title="try / except",
                what="try 區塊放可能出錯的程式碼,except 區塊放出錯時要執行的處理邏輯。",
                why="資料清理時常遇到「這一格轉型失敗」這種情況,用 try/except 可以攔截錯誤、決定如何處理,而不是讓整個程式當掉。",
                problem="讓程式在遇到預期內的錯誤時能優雅地處理,而不是直接中斷。",
                syntax='try:\n    value = int("abc")\nexcept ValueError:\n    value = None\n    print("轉型失敗")',
                usage="讀取外部資料轉型時(例如把字串欄位轉成數字),用 try/except 包住轉型邏輯,轉型失敗時填入 NaN 或預設值,是資料清理常見寫法。",
                common_errors="except 沒有指定錯誤類型(裸露的 except:)會連不該攔截的錯誤都吃掉,不利於除錯;建議明確寫出錯誤類型如 except ValueError。",
                confusions="try/except 不是用來『避免』錯誤發生,而是『發生後如何應對』;有 finally 區塊時,不論成功失敗都會執行。",
            )
        ],
        examples=[
            Example(code='values = ["10", "abc", "30"]\nresult = []\nfor v in values:\n    try:\n        result.append(int(v))\n    except ValueError:\n        result.append(None)\nprint(result)', explain="把無法轉型的資料標成 None,而不是讓程式中斷。"),
        ],
        exercises=[
            Exercise(
                id="ex_exc_1",
                prompt="給定 raw_values = ['5', '9x', '12', 'abc', '3'],請用 try/except 把每個能轉成整數的值放進 clean_values,轉型失敗的直接跳過(不加入)。clean_values 應為 [5, 12, 3]。",
                starter_code="raw_values = ['5', '9x', '12', 'abc', '3']\nclean_values = []\n# 在這裡完成\n",
                checker_code=(
                    "import json\n"
                    "ok = 'clean_values' in dir() and clean_values == [5, 12, 3]\n"
                    "print('RESULT_JSON:' + json.dumps({'passed': bool(ok), 'message': '正確!' if ok else '提示:for 迴圈搭配 try/except ValueError,失敗就不 append'}))"
                ),
                hint="for v in raw_values:\n    try:\n        clean_values.append(int(v))\n    except ValueError:\n        pass",
            )
        ],
        questions=[
            Question(id="q_py_exc_1", concept_id="c_exceptions", qtype="predict", prompt="這段會印出什麼?", code='try:\n    x = int("abc")\nexcept ValueError:\n    x = -1\nprint(x)',
                      answer="-1", explanation="int(\"abc\") 轉型失敗,進入 except,x 被設為 -1。"),
            Question(id="q_py_exc_2", concept_id="c_exceptions", qtype="tf", prompt="判斷對錯:如果 try 區塊沒有發生錯誤,except 區塊的程式碼也會被執行。",
                      answer="false", explanation="except 只有在 try 區塊發生錯誤時才會執行。"),
        ],
    ),
    Unit(
        id="py_imports",
        stage="python",
        order=12,
        title="Import 與模組/套件概念",
        summary="NumPy、Pandas 本身就是「套件」——理解 import 是使用它們的第一步。",
        concepts=[
            Concept(
                id="c_imports",
                title="import 模組與套件",
                what="模組(module)是一個 .py 檔案;套件(package)是一堆模組的集合。用 import 把別人寫好的功能載入到自己的程式裡使用。",
                why="不用自己從零實作所有功能——NumPy、Pandas 都是已經寫好、高度最佳化的套件,直接 import 就能用。",
                problem="重複使用別人(或自己)寫好的程式碼,不用每個專案都重寫一次。",
                syntax="import numpy as np\nimport pandas as pd\nfrom collections import Counter\n\nnp.array([1,2,3])",
                usage="幾乎所有數據分析程式碼開頭都會看到 import numpy as np 和 import pandas as pd——as 是幫套件取一個慣用的簡短別名。",
                common_errors="套件沒有安裝就 import 會報 ModuleNotFoundError;import 的別名打錯(例如忘記用 np. 前綴直接呼叫 array())。",
                confusions="import pandas 和 import pandas as pd 效果相同,只是後者呼叫時可以用簡短的 pd. 而不是打完整的 pandas.。",
            )
        ],
        examples=[
            Example(code='import math\nprint(math.sqrt(16))', explain="import 標準函式庫的 math 模組,呼叫其中的 sqrt 函式。"),
            Example(code='import numpy as np\narr = np.array([1, 2, 3])\nprint(arr.sum())', explain="這是之後 NumPy 單元會大量出現的標準寫法:import numpy as np。"),
        ],
        exercises=[
            Exercise(
                id="ex_import_1",
                prompt="請 import math 模組,並建立 result,內容是 math.sqrt(81) 的結果(應為 9.0)。",
                starter_code="# 在這裡完成\n",
                checker_code=(
                    "import json\n"
                    "ok = 'result' in dir() and abs(result - 9.0) < 1e-6\n"
                    "print('RESULT_JSON:' + json.dumps({'passed': bool(ok), 'message': '正確!' if ok else '記得先 import math'}))"
                ),
                hint="import math\nresult = math.sqrt(81)",
            )
        ],
        questions=[
            Question(id="q_py_imp_1", concept_id="c_imports", qtype="mc", prompt="import numpy as np 中的 as np 是在做什麼?",
                      options=[("a", "幫 numpy 取一個簡短別名 np,之後可以用 np. 呼叫功能"), ("b", "只載入 numpy 的一部分功能"), ("c", "把 numpy 重新命名成永久名稱"), ("d", "np 是必要語法,不能改成別的名字")],
                      answer="a", explanation="as 只是取別名方便呼叫,理論上可以取任何名字,但 np/pd 是業界慣例。"),
            Question(id="q_py_imp_2", concept_id="c_imports", qtype="tf", prompt="判斷對錯:如果沒有先安裝 pandas,即使寫了 import pandas as pd 也會報錯。",
                      answer="true", explanation="import 只能載入已安裝的套件,未安裝會 ModuleNotFoundError。"),
        ],
    ),
]
