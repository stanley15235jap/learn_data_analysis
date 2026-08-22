# -*- coding: utf-8 -*-
"""Stage 3: Pandas。從 Series/DataFrame 一路到 groupby/EDA,聚焦『讀取→檢查→清理→篩選→整理→分析』的完整流程。"""
from core.models import Unit, Concept, Example, Exercise, Question, CodeWalkthrough, WalkthroughStep

UNITS = [
    Unit(
        id="pd_series_dataframe",
        stage="pandas",
        order=1,
        title="Series 與 DataFrame",
        summary="Series 是一欄帶標籤的資料,DataFrame 是多個 Series 並排組成的表格——這是 Pandas 的兩個核心資料結構。",
        concepts=[
            Concept(
                id="c_pd_series_df",
                title="Series 與 DataFrame",
                what="Series 是一維、帶索引標籤的資料(像一欄);DataFrame 是二維的表格,由多個共用同一組列索引的 Series 並排組成(像整張表)。",
                why="真實資料幾乎都是表格形式(欄+列),DataFrame 是處理這種資料最自然的結構,Series 則是操作『單一欄』時的基本單位。",
                problem="用貼近『表格』直覺的方式儲存與操作結構化資料,而不是像 NumPy 那樣只有位置沒有名字。",
                syntax='import pandas as pd\ns = pd.Series([90, 85, 77])\ndf = pd.DataFrame({"name": ["Alice","Bob"], "score": [90, 85]})',
                usage="讀取 CSV 得到的就是 DataFrame;取出其中一欄(如 df[\"score\"])得到的就是 Series。",
                common_errors="把 df[\"col\"](取出一欄,得到 Series)跟 df[[\"col\"]](取出一欄但保持 DataFrame 形狀)搞混,兩者型態不同。",
                confusions="df.columns 是欄名的清單,df.index 是列索引的清單——兩者容易搞混,但分別對應表格的兩個維度。",
            )
        ],
        examples=[
            Example(code='import pandas as pd\ndf = pd.DataFrame({"name": ["Alice", "Bob", "Carol"], "score": [90, 85, 77]})\nprint(df)\nprint(type(df["score"]))\nprint(type(df[["score"]]))', explain="df['score'] 是 Series,df[['score']] 用雙層中括號取出仍是 DataFrame。"),
        ],
        exercises=[
            Exercise(
                id="ex_pd_sd_1",
                prompt="請用 dict 建立一個 DataFrame df,包含欄位 name=['A','B','C'] 與 age=[20,25,30],再建立 age_series,內容是 df['age']。",
                starter_code="import pandas as pd\n# 在這裡完成\n",
                checker_code=(
                    "import json\nimport pandas as pd\n"
                    "ok = 'df' in dir() and 'age_series' in dir() and isinstance(age_series, pd.Series) and list(age_series) == [20,25,30]\n"
                    "print('RESULT_JSON:' + json.dumps({'passed': bool(ok), 'message': '正確!' if ok else \"提示:df = pd.DataFrame({'name':['A','B','C'],'age':[20,25,30]})\"}))"
                ),
                hint="df = pd.DataFrame({'name': ['A','B','C'], 'age': [20,25,30]})\nage_series = df['age']",
            )
        ],
        questions=[
            Question(id="q_pd_sd_1", concept_id="c_pd_series_df", qtype="mc", prompt="df['score'] 和 df[['score']] 的差別是?",
                      options=[("a", "前者回傳 Series,後者回傳只有一欄的 DataFrame"), ("b", "兩者完全相同"), ("c", "後者語法錯誤"), ("d", "前者回傳 DataFrame,後者回傳 Series")],
                      answer="a", explanation="單層中括號取出 Series,雙層中括號(傳入 list)取出仍為 DataFrame 的子集。"),
            Question(id="q_pd_sd_2", concept_id="c_pd_series_df", qtype="tf", prompt="判斷對錯:DataFrame 可以想成是多個共用列索引的 Series 並排組成的表格。",
                      answer="true", explanation="這正是 DataFrame 的本質。"),
        ],
    ),
    Unit(
        id="pd_create_read",
        stage="pandas",
        order=2,
        title="建立 DataFrame 與 read_csv",
        summary="資料分析的第一步永遠是把資料讀進來——最常見的來源是 CSV 檔案。",
        concepts=[
            Concept(
                id="c_pd_read",
                title="建立 DataFrame / read_csv",
                what="可以用 dict、list of dict、或 pd.read_csv(path) 讀取 CSV 檔案來建立 DataFrame。",
                why="真實世界的資料多半以 CSV、Excel 等檔案形式存在,read_csv 是分析流程的起點。",
                problem="把外部資料載入成程式可以操作的 DataFrame。",
                syntax='import pandas as pd\ndf = pd.read_csv("content/datasets/employees.csv")',
                usage="幾乎所有資料分析專案的第一行『真正的分析程式碼』就是 pd.read_csv(...)。",
                common_errors="檔案路徑寫錯導致 FileNotFoundError;誤以為 read_csv 後資料型態一定正確,實際上常需要事後檢查與轉型。",
                confusions="read_csv 預設會把第一列當成欄名(header),若資料沒有標題列需要加參數 header=None。",
            )
        ],
        examples=[
            Example(code='import pandas as pd\ndf = pd.read_csv("content/datasets/employees.csv")\nprint(df.head())', explain="讀取員工資料 CSV,並用 head() 預覽前幾筆。"),
        ],
        exercises=[
            Exercise(
                id="ex_pd_read_1",
                prompt="請用 pd.read_csv 讀取 content/datasets/employees.csv,存成 df,並建立 n_rows,內容是這份資料的列數(應為 10)。",
                starter_code="import pandas as pd\n# 在這裡完成\n",
                checker_code=(
                    "import json\n"
                    "ok = 'df' in dir() and 'n_rows' in dir() and n_rows == 10 and len(df) == 10\n"
                    "print('RESULT_JSON:' + json.dumps({'passed': bool(ok), 'message': '正確!' if ok else '提示:n_rows = len(df) 或 df.shape[0]'}))"
                ),
                hint='df = pd.read_csv("content/datasets/employees.csv")\nn_rows = len(df)',
            )
        ],
        questions=[
            Question(id="q_pd_read_1", concept_id="c_pd_read", qtype="tf", prompt="判斷對錯:pd.read_csv() 預設會把 CSV 的第一列當成欄名。",
                      answer="true", explanation="header 參數預設為 'infer',通常取第一列作欄名。"),
        ],
    ),
    Unit(
        id="pd_inspect",
        stage="pandas",
        order=3,
        title="初步檢查資料",
        summary="讀進資料後,第一件事永遠是『先看一眼』——head/tail/info/describe/shape/columns/dtypes。",
        concepts=[
            Concept(
                id="c_pd_inspect",
                title="head / tail / info / describe / shape / columns / dtypes",
                what=".head(n)/.tail(n) 看前/後 n 筆;.info() 看欄位型態與缺失概況;.describe() 看數值欄位的統計摘要;.shape 看(列數,欄數);.columns 看欄名;.dtypes 看每欄型態。",
                why="拿到資料後,不先看過就直接分析很容易踩到型態錯誤或缺失值的坑,這些指令是資料分析的『第一眼健檢』。",
                problem="快速掌握資料的規模、結構與品質概況,決定後續清理與分析的方向。",
                syntax="df.head()\ndf.info()\ndf.describe()\ndf.shape\ndf.columns\ndf.dtypes",
                usage="拿到任何新資料集,養成先跑一輪 df.shape → df.info() → df.describe() → df.head() 的習慣,是專業分析師的基本動作。",
                common_errors="把 df.shape 當函式呼叫寫成 df.shape(),shape 是屬性不是方法,不用加括號。",
                confusions="describe() 預設只統計數值欄位,文字欄位不會出現在結果中,除非加上 include='all'。",
            )
        ],
        examples=[
            Example(code='import pandas as pd\ndf = pd.read_csv("content/datasets/employees.csv")\nprint(df.shape)\nprint(df.dtypes)\nprint(df.describe())', explain="依序查看形狀、型態、數值欄位統計摘要。"),
        ],
        exercises=[
            Exercise(
                id="ex_pd_inspect_1",
                prompt="讀取 content/datasets/employees.csv 存成 df,建立 avg_salary,內容是 salary 欄位的平均值(用 df['salary'].mean())。",
                starter_code="import pandas as pd\n# 在這裡完成\n",
                checker_code=(
                    "import json\n"
                    "ok = 'avg_salary' in dir() and abs(avg_salary - 68200.0) < 1.0\n"
                    "print('RESULT_JSON:' + json.dumps({'passed': bool(ok), 'message': '正確!' if ok else '提示:avg_salary = df[\"salary\"].mean()'}))"
                ),
                hint='df = pd.read_csv("content/datasets/employees.csv")\navg_salary = df["salary"].mean()',
            )
        ],
        questions=[
            Question(id="q_pd_insp_1", concept_id="c_pd_inspect", qtype="bugfix", prompt="這段程式碼會報錯,問題在哪?", code="print(df.shape())",
                      options=[("a", "shape 是屬性不是方法,不該加括號,應寫 df.shape"), ("b", "df 沒有定義"), ("c", "print 用法錯誤"), ("d", "沒有問題")],
                      answer="a", explanation="shape 是屬性(property),不用呼叫。"),
            Question(id="q_pd_insp_2", concept_id="c_pd_inspect", qtype="mc", prompt="想快速知道每一欄有沒有缺失值、型態是什麼,最適合用?",
                      options=[("a", "df.info()"), ("b", "df.head()"), ("c", "df.columns"), ("d", "print(df)")],
                      answer="a", explanation="info() 會列出每欄的非缺失值數量與型態。"),
        ],
    ),
    Unit(
        id="pd_select_columns",
        stage="pandas",
        order=4,
        title="欄位選取",
        summary="取出一欄、多欄,是所有後續分析的起手式。",
        concepts=[
            Concept(
                id="c_pd_select",
                title="欄位選取",
                what="df['col'] 取單欄(Series);df[['col1','col2']] 取多欄(DataFrame);可以用 list 動態指定要選哪些欄。",
                why="分析時常常只需要資料的一部分欄位,選取是最基本的資料操作。",
                problem="從表格中取出你需要的欄位子集。",
                syntax="df['salary']\ndf[['name', 'salary']]",
                usage="做部門薪資分析時,可能只需要 df[['department', 'salary']] 這兩欄,不需要整張表。",
                common_errors="df['col1', 'col2'] (少了一層中括號)會報錯,多欄選取必須傳入一個 list:df[['col1','col2']]。",
                confusions="欄位名稱打錯字(大小寫、多餘空白)會直接報 KeyError,這也是為什麼前面要學字串清理。",
            )
        ],
        examples=[
            Example(code='import pandas as pd\ndf = pd.read_csv("content/datasets/employees.csv")\nprint(df["department"].unique())\nprint(df[["name", "salary"]].head(3))', explain="取單欄看有哪些不重複的部門;取多欄預覽前三筆。"),
        ],
        exercises=[
            Exercise(
                id="ex_pd_select_1",
                prompt="讀取 employees.csv,建立 subset,內容只包含 name 和 department 兩欄。",
                starter_code="import pandas as pd\ndf = pd.read_csv('content/datasets/employees.csv')\n# 在這裡完成\n",
                checker_code=(
                    "import json\n"
                    "ok = 'subset' in dir() and list(subset.columns) == ['name', 'department']\n"
                    "print('RESULT_JSON:' + json.dumps({'passed': bool(ok), 'message': '正確!' if ok else \"提示:subset = df[['name', 'department']]\"}))"
                ),
                hint="subset = df[['name', 'department']]",
            )
        ],
        questions=[
            Question(id="q_pd_sel_1", concept_id="c_pd_select", qtype="bugfix", prompt="這段程式碼會報錯,問題在哪?", code="df['name', 'department']",
                      options=[("a", "選取多欄要傳入 list,應寫 df[['name','department']]"), ("b", "欄名打錯"), ("c", "df 未定義"), ("d", "沒有問題")],
                      answer="a", explanation="df[a, b] 會被誤解成用 tuple 當索引,正確要用 list。"),
        ],
    ),
    Unit(
        id="pd_loc_iloc",
        stage="pandas",
        order=5,
        title="loc 與 iloc",
        summary="這是初學者最容易混淆的一組觀念:loc 用『標籤』選取,iloc 用『位置』選取。",
        concepts=[
            Concept(
                id="c_pd_loc_iloc",
                title="loc 與 iloc",
                what=".loc[列標籤, 欄名] 用『標籤/名稱』選取資料;.iloc[列位置, 欄位置] 用『整數位置』選取資料,概念跟 NumPy 的 arr[列,欄] 完全對應。",
                why="DataFrame 的列索引不一定是連續整數(可能是日期、ID 等),需要區分『用名字找』還是『用第幾個找』。",
                problem="精確、明確地指定要用『標籤』還是『位置』來選取資料列與欄,避免選錯。",
                syntax="df.loc[0, 'name']        # 標籤為0的列、'name'欄\ndf.loc[0:2, 'name']       # 用loc時,切片『包含』結尾\ndf.iloc[0, 1]             # 第1列第2欄(位置,從0算)\ndf.iloc[0:2, :]           # 用iloc時,切片跟一般Python一樣『不包含』結尾",
                usage="條件篩選常搭配 loc 使用,例如 df.loc[df['salary']>60000, 'name'];單純想用『第幾筆』取資料時用 iloc。",
                common_errors="搞混兩者的切片行為:df.loc[0:2] 會包含索引2共3列,df.iloc[0:2] 則跟一般切片一樣不包含2、只有2列——這是最常見的錯誤來源。",
                confusions="如果 DataFrame 的索引剛好是 0,1,2...的連續整數,loc 和 iloc 用數字時看起來結果很像,容易誤以為兩者相同,但只要索引不是預設整數(例如篩選過、排序過的資料),兩者結果就會明顯不同。",
            )
        ],
        examples=[
            Example(code='import pandas as pd\ndf = pd.read_csv("content/datasets/employees.csv")\nprint(df.loc[0, "name"])\nprint(df.iloc[0, 1])', explain="loc 用欄名 'name'、iloc 用欄位置 1(第2欄),在這個例子中兩者剛好取到同一個值。"),
            Example(code='import pandas as pd\ndf = pd.read_csv("content/datasets/employees.csv")\nprint(df.loc[0:2].shape)\nprint(df.iloc[0:2].shape)', explain="loc[0:2] 包含索引2,共3列;iloc[0:2] 不包含2,只有2列——這是兩者最關鍵的差異。"),
        ],
        exercises=[
            Exercise(
                id="ex_pd_locilo_1",
                prompt="讀取 employees.csv,用 iloc 建立 first_three,內容是前3列(位置0,1,2);再用 loc 建立 alice_dept,內容是列標籤0、欄位'department'的值。",
                starter_code="import pandas as pd\ndf = pd.read_csv('content/datasets/employees.csv')\n# 在這裡完成\n",
                checker_code=(
                    "import json\n"
                    "ok = 'first_three' in dir() and 'alice_dept' in dir() and len(first_three) == 3 and alice_dept == 'Engineering'\n"
                    "print('RESULT_JSON:' + json.dumps({'passed': bool(ok), 'message': '正確!' if ok else \"提示:first_three = df.iloc[0:3]; alice_dept = df.loc[0, 'department']\"}))"
                ),
                hint="first_three = df.iloc[0:3]\nalice_dept = df.loc[0, 'department']",
            )
        ],
        questions=[
            Question(id="q_pd_li_1", concept_id="c_pd_loc_iloc", qtype="predict", prompt="df 有5列(索引0~4),df.iloc[0:3] 會回傳幾列?", code="", answer="3", explanation="iloc 切片跟一般 Python 一樣不包含結尾,0,1,2共3列。"),
            Question(id="q_pd_li_2", concept_id="c_pd_loc_iloc", qtype="predict", prompt="df 有5列(索引0~4),df.loc[0:3] 會回傳幾列?", code="", answer="4", explanation="loc 切片包含結尾標籤,0,1,2,3共4列。"),
            Question(id="q_pd_li_3", concept_id="c_pd_loc_iloc", qtype="mc", prompt="想用『欄位名稱』選取資料,應該用?",
                      options=[("a", "loc"), ("b", "iloc"), ("c", "兩者皆可,結果必然相同"), ("d", "都不行")],
                      answer="a", explanation="loc 用標籤(名稱),iloc 用整數位置。"),
        ],
    ),
    Unit(
        id="pd_filter",
        stage="pandas",
        order=6,
        title="條件篩選",
        summary="用布林條件篩選資料列,原理跟 NumPy 的 boolean indexing 完全相同。",
        concepts=[
            Concept(
                id="c_pd_filter",
                title="條件篩選",
                what="df[condition] 或 df.loc[condition] 篩選出條件為 True 的列;condition 是像 df['col'] > 5 這種比較運算產生的布林 Series。",
                why="分析時常常只關心符合特定條件的子集,例如『薪水高於平均的員工』。",
                problem="從整份資料中挑出符合特定邏輯的部分。",
                syntax="df[df['salary'] > 60000]\ndf[(df['salary'] > 60000) & (df['department'] == 'Engineering')]",
                usage="幾乎所有『某某條件下的分析』都是先用條件篩選出子集,再對子集做統計。",
                common_errors="多重條件忘記加括號或用錯 and/or(跟 NumPy 布林索引一樣,要用 & | 並各自括號)。",
                confusions="df[condition] 篩出來的是符合條件的『整列』,不是只有那一欄的值。",
            )
        ],
        examples=[
            Example(code='import pandas as pd\ndf = pd.read_csv("content/datasets/employees.csv")\nhigh_earners = df[df["salary"] > 70000]\nprint(high_earners[["name", "salary"]])', explain="篩出薪水高於7萬的員工。"),
        ],
        exercises=[
            Exercise(
                id="ex_pd_filter_1",
                prompt="讀取 employees.csv,建立 eng_senior,內容是 department 為 'Engineering' 且 years_experience >= 5 的列。",
                starter_code="import pandas as pd\ndf = pd.read_csv('content/datasets/employees.csv')\n# 在這裡完成\n",
                checker_code=(
                    "import json\n"
                    "ok = 'eng_senior' in dir() and len(eng_senior) == 2 and set(eng_senior['name']) == {'Carol Wu', 'Frank Liu'}\n"
                    "print('RESULT_JSON:' + json.dumps({'passed': bool(ok), 'message': '正確!' if ok else \"提示:df[(df['department']=='Engineering') & (df['years_experience']>=5)]\"}))"
                ),
                hint="eng_senior = df[(df['department']=='Engineering') & (df['years_experience']>=5)]",
            )
        ],
        questions=[
            Question(id="q_pd_filter_1", concept_id="c_pd_filter", qtype="bugfix", prompt="這段為什麼會報錯?", code="df[df['salary'] > 60000 and df['department'] == 'Sales']",
                      options=[("a", "組合條件要用 & 且各自加括號,不能用 and"), ("b", "salary 欄不存在"), ("c", "應該用 loc 才能篩選"), ("d", "沒有問題")],
                      answer="a", explanation="Pandas 布林運算跟 NumPy 一樣要用 & / |,並用括號包住各條件。"),
        ],
    ),
    Unit(
        id="pd_modify_columns",
        stage="pandas",
        order=7,
        title="新增、修改、刪除欄位",
        summary="資料分析常需要衍生新欄位(如稅後薪資),或移除不需要的欄位。",
        concepts=[
            Concept(
                id="c_pd_modify",
                title="新增/修改/刪除欄位",
                what="df['new_col'] = ... 新增或覆寫一欄;df.drop(columns=['col']) 刪除欄位(預設回傳新 DataFrame,不改原本的,除非加 inplace=True)。",
                why="原始資料常常不是直接可用的格式,需要衍生計算欄位或移除不需要的欄位以利後續分析。",
                problem="調整表格的欄位結構,產生分析所需要的新資訊。",
                syntax="df['bonus'] = df['salary'] * 0.1\ndf = df.drop(columns=['years_experience'])",
                usage="df['total'] = df['price'] * df['quantity'] 是資料分析中最常見的新增衍生欄位寫法,直接用到向量化運算。",
                common_errors="以為 df.drop(columns=['col']) 會直接修改原本的 df,實際上預設回傳新的 DataFrame,需要重新賦值或加 inplace=True。",
                confusions="新增欄位時如果欄名已存在,會直接覆寫該欄,不會報錯也不會另外新增。",
            )
        ],
        examples=[
            Example(code='import pandas as pd\ndf = pd.read_csv("content/datasets/employees.csv")\ndf["bonus"] = df["salary"] * 0.1\nprint(df[["name", "salary", "bonus"]].head(3))', explain="新增衍生欄位 bonus,是薪水的10%。"),
        ],
        exercises=[
            Exercise(
                id="ex_pd_modify_1",
                prompt="讀取 employees.csv,新增欄位 annual_salary,內容是 salary * 12,並建立 max_annual,內容是 annual_salary 的最大值。",
                starter_code="import pandas as pd\ndf = pd.read_csv('content/datasets/employees.csv')\n# 在這裡完成\n",
                checker_code=(
                    "import json\n"
                    "ok = 'annual_salary' in df.columns and 'max_annual' in dir() and max_annual == 95000*12\n"
                    "print('RESULT_JSON:' + json.dumps({'passed': bool(ok), 'message': '正確!' if ok else \"提示:df['annual_salary'] = df['salary']*12\"}))"
                ),
                hint="df['annual_salary'] = df['salary'] * 12\nmax_annual = df['annual_salary'].max()",
            )
        ],
        questions=[
            Question(id="q_pd_mod_1", concept_id="c_pd_modify", qtype="tf", prompt="判斷對錯:df.drop(columns=['a']) 預設會直接修改原本的 df。",
                      answer="false", explanation="預設回傳新 DataFrame,除非加 inplace=True 或重新賦值給 df。"),
        ],
    ),
    Unit(
        id="pd_sort",
        stage="pandas",
        order=8,
        title="sort_values",
        summary="依某一欄的值排序整張表,常用於找出最大/最小、排行榜類分析。",
        concepts=[
            Concept(
                id="c_pd_sort",
                title="sort_values",
                what="df.sort_values('col') 依某欄由小到大排序;加 ascending=False 由大到小;可以傳入多個欄名做多層排序。",
                why="找『前幾名』『最貴的商品』這類分析都需要先排序。",
                problem="依指定欄位重新排列資料列的順序。",
                syntax="df.sort_values('salary', ascending=False)\ndf.sort_values(['department', 'salary'], ascending=[True, False])",
                usage="想找出『薪水最高的前3名員工』:df.sort_values('salary', ascending=False).head(3)。",
                common_errors="排序後忘記重新賦值(df = df.sort_values(...)),或不知道排序不影響原本索引,索引會跟著資料一起移動。",
                confusions="sort_values 預設不會重設索引(index),排序後索引看起來會是亂序的,如果要重設可以加 .reset_index(drop=True)。",
            )
        ],
        examples=[
            Example(code='import pandas as pd\ndf = pd.read_csv("content/datasets/employees.csv")\ntop3 = df.sort_values("salary", ascending=False).head(3)\nprint(top3[["name", "salary"]])', explain="依薪水由高到低排序,取前3名。"),
        ],
        exercises=[
            Exercise(
                id="ex_pd_sort_1",
                prompt="讀取 employees.csv,建立 lowest_two,內容是薪水最低的兩位員工(依 salary 由小到大排序後取前2筆)。",
                starter_code="import pandas as pd\ndf = pd.read_csv('content/datasets/employees.csv')\n# 在這裡完成\n",
                checker_code=(
                    "import json\n"
                    "ok = 'lowest_two' in dir() and set(lowest_two['name']) == {'Henry Chen', 'Bob Lin'}\n"
                    "print('RESULT_JSON:' + json.dumps({'passed': bool(ok), 'message': '正確!' if ok else \"提示:df.sort_values('salary').head(2)\"}))"
                ),
                hint="lowest_two = df.sort_values('salary').head(2)",
            )
        ],
        questions=[
            Question(id="q_pd_sort_1", concept_id="c_pd_sort", qtype="mc", prompt="想依薪水『由高到低』排序,應該加什麼參數?",
                      options=[("a", "ascending=False"), ("b", "ascending=True"), ("c", "descending=True"), ("d", "reverse=True")],
                      answer="a", explanation="ascending=False 表示不是遞增排序,即由大到小。"),
        ],
    ),
    Unit(
        id="pd_missing",
        stage="pandas",
        order=9,
        title="缺失值(Missing Values)",
        summary="真實資料幾乎一定有缺失值,學會辨識、統計、決定如何處理它們是資料清理的核心技能。",
        concepts=[
            Concept(
                id="c_pd_missing",
                title="缺失值處理",
                what="df.isna()(或 isnull())標出哪裡缺失;df.isna().sum() 統計每欄缺了幾筆;df.dropna() 刪除含缺失值的列;df.fillna(value) 用指定值填補缺失。",
                why="缺失值如果不處理,會讓平均數、加總等統計量失真,甚至讓程式報錯。",
                problem="辨識資料中的缺漏,並依情境決定是刪除、填補,還是保留缺失狀態。",
                syntax="df.isna().sum()\ndf.dropna()                      # 刪除任一欄有缺失的列\ndf.dropna(subset=['price'])       # 只看 price 欄是否缺失\ndf.fillna({'price': 0})            # 指定欄位用值填補",
                usage="清理 sales_messy.csv 這類資料時,第一步通常是 df.isna().sum() 先看每欄缺了多少,再決定 dropna 還是 fillna。",
                common_errors="不分青紅皂白直接 dropna() 可能刪掉太多資料;用平均數填補時忘記先排除本身就異常的值。",
                confusions="isna() 判斷的是『這個儲存格是不是 NaN』,不是判斷『這個值是不是等於0或空字串』——0跟空字串都不是缺失值。",
            )
        ],
        examples=[
            Example(code='import pandas as pd\ndf = pd.read_csv("content/datasets/sales_messy.csv")\nprint(df.isna().sum())', explain="統計每欄有多少缺失值。"),
        ],
        exercises=[
            Exercise(
                id="ex_pd_missing_1",
                prompt="讀取 sales_messy.csv,建立 missing_price_count,內容是 price 欄位缺失值的數量。",
                starter_code="import pandas as pd\ndf = pd.read_csv('content/datasets/sales_messy.csv')\n# 在這裡完成\n",
                checker_code=(
                    "import json\n"
                    "ok = 'missing_price_count' in dir() and missing_price_count == 1\n"
                    "print('RESULT_JSON:' + json.dumps({'passed': bool(ok), 'message': '正確!' if ok else \"提示:df['price'].isna().sum()\"}))"
                ),
                hint="missing_price_count = df['price'].isna().sum()",
            )
        ],
        questions=[
            Question(id="q_pd_miss_1", concept_id="c_pd_missing", qtype="tf", prompt="判斷對錯:數值 0 跟 NaN 是一樣的,isna() 也會把 0 判斷成缺失值。",
                      answer="false", explanation="0 是一個有效數值,不是缺失值;isna() 只認 NaN/None 這類真正的缺失標記。"),
            Question(id="q_pd_miss_2", concept_id="c_pd_missing", qtype="mc", prompt="想把 price 欄的缺失值填成 0,應該用?",
                      options=[("a", "df['price'].fillna(0)"), ("b", "df['price'].dropna(0)"), ("c", "df['price'].isna(0)"), ("d", "df['price'] = 0")],
                      answer="a", explanation="fillna(value) 用指定值填補缺失。"),
        ],
    ),
    Unit(
        id="pd_duplicates",
        stage="pandas",
        order=10,
        title="重複資料",
        summary="重複紀錄會讓加總、平均等統計量被『灌水』,需要先辨識並移除。",
        concepts=[
            Concept(
                id="c_pd_duplicates",
                title="重複值處理",
                what="df.duplicated() 標出哪些列是重複的(跟前面出現過的列完全相同);df.drop_duplicates() 移除重複列,只保留第一筆。",
                why="重複資料若未處理,計算總數、平均等統計量會失真,例如同一筆訂單被算了兩次。",
                problem="找出並處理資料中不應該重複出現的紀錄。",
                syntax="df.duplicated().sum()          # 有幾筆重複\ndf.drop_duplicates()             # 移除重複,保留第一筆\ndf.drop_duplicates(subset=['order_id'])  # 只依特定欄位判斷重複",
                usage="清理 sales_messy.csv 前,通常會先確認 df.duplicated().sum() 看有沒有完全重複的訂單列,再決定要不要 drop_duplicates()。",
                common_errors="只憑『看起來像』就認定資料重複,沒有實際用 duplicated() 檢查,可能誤刪合法的相似資料。",
                confusions="duplicated() 預設判斷『整列所有欄位都相同』才算重複,如果只想比對特定欄位,需要用 subset 參數指定。",
            )
        ],
        examples=[
            Example(code='import pandas as pd\ndf = pd.read_csv("content/datasets/sales_messy.csv")\nprint(df.duplicated().sum())\nclean = df.drop_duplicates()\nprint(len(df), len(clean))', explain="先確認重複列數量,再移除重複。"),
        ],
        exercises=[
            Exercise(
                id="ex_pd_dup_1",
                prompt="讀取 sales_messy.csv,建立 deduped,內容是移除完全重複列之後的 DataFrame,並建立 removed_count,內容是被移除的列數。",
                starter_code="import pandas as pd\ndf = pd.read_csv('content/datasets/sales_messy.csv')\n# 在這裡完成\n",
                checker_code=(
                    "import json\n"
                    "ok = 'deduped' in dir() and 'removed_count' in dir() and removed_count == 1 and len(deduped) == len(df) - 1\n"
                    "print('RESULT_JSON:' + json.dumps({'passed': bool(ok), 'message': '正確!' if ok else \"提示:deduped = df.drop_duplicates(); removed_count = len(df) - len(deduped)\"}))"
                ),
                hint="deduped = df.drop_duplicates()\nremoved_count = len(df) - len(deduped)",
            )
        ],
        questions=[
            Question(id="q_pd_dup_1", concept_id="c_pd_duplicates", qtype="predict", prompt="df 有10列,其中2列完全重複(共有1組重複),df.drop_duplicates() 後會剩幾列?", code="", answer="9", explanation="drop_duplicates 保留第一筆,移除多餘的重複列,10-1=9。"),
        ],
    ),
    Unit(
        id="pd_groupby",
        stage="pandas",
        order=11,
        title="GroupBy 與 Aggregation",
        summary="『依某個類別分組,各自算統計量』是數據分析最核心的操作之一,例如各部門平均薪資。",
        concepts=[
            Concept(
                id="c_pd_groupby",
                title="GroupBy 與聚合",
                what="df.groupby('col') 依某欄的值分組;接著選一欄再套用聚合函式(如 .mean()、.sum()、.count()),得到『每個分組』各自的統計量。",
                why="『依類別分組後比較』是數據分析中最常見的問題形式,例如各部門平均薪資、各城市顧客數。",
                problem="把整份資料依類別拆開,分別計算每個類別的統計量,而不用手動篩選每個類別再各自計算一次。",
                syntax="df.groupby('department')['salary'].mean()\ndf.groupby('department').agg({'salary': 'mean', 'name': 'count'})",
                usage="這幾乎是所有『依類別比較』分析題的標準寫法,例如「哪個部門薪水最高」就是 groupby 後排序取第一。",
                common_errors="忘記 groupby 之後要先選欄位或用 .agg() 才能得到聚合結果,單獨 df.groupby('col') 只是建立一個『分組物件』,還沒有算出任何統計量。",
                confusions="df.groupby('col')['other_col'].mean() 讀起來要拆成三段理解:先分組、再選欄、再聚合——這正是本單元下方『程式碼閱讀』要練習的能力。",
            )
        ],
        examples=[
            Example(code='import pandas as pd\ndf = pd.read_csv("content/datasets/employees.csv")\nprint(df.groupby("department")["salary"].mean())', explain="依部門分組,計算各部門的平均薪資。"),
            Example(code='import pandas as pd\ndf = pd.read_csv("content/datasets/employees.csv")\nprint(df.groupby("department").agg({"salary": "mean", "name": "count"}))', explain="一次計算多個聚合結果:平均薪資與人數。"),
        ],
        exercises=[
            Exercise(
                id="ex_pd_groupby_1",
                prompt="讀取 employees.csv,建立 dept_avg,內容是各部門的平均薪資(df.groupby('department')['salary'].mean())。",
                starter_code="import pandas as pd\ndf = pd.read_csv('content/datasets/employees.csv')\n# 在這裡完成\n",
                checker_code=(
                    "import json\n"
                    "ok = 'dept_avg' in dir() and abs(dept_avg['Sales'] - (55000+58000+51000)/3) < 1.0\n"
                    "print('RESULT_JSON:' + json.dumps({'passed': bool(ok), 'message': '正確!' if ok else \"提示:df.groupby('department')['salary'].mean()\"}))"
                ),
                hint="dept_avg = df.groupby('department')['salary'].mean()",
            )
        ],
        questions=[
            Question(id="q_pd_gb_1", concept_id="c_pd_groupby", qtype="mc", prompt="這段大致會印出什麼結構(不用精確數值,選出正確描述)?", code="df.groupby('department')['salary'].mean()",
                      options=[("a", "一個以部門為索引、值為該部門平均薪資的 Series"), ("b", "原本整張 DataFrame,沒有任何改變"), ("c", "一個布林值,表示是否分組成功"), ("d", "報錯,因為 groupby 後不能再用中括號選欄")],
                      answer="a", explanation="groupby+選欄+聚合函式,結果是『每個分組一個值』的 Series,索引是分組依據的欄位。"),
            Question(id="q_pd_gb_2", concept_id="c_pd_groupby", qtype="short", prompt="用一句話解釋 df.groupby('department')['salary'].mean() 這行程式碼在做什麼。",
                      keywords=["部門", "平均"], explanation="依部門分組,對每組的 salary 欄計算平均值。"),
        ],
        code_walkthrough=CodeWalkthrough(
            title="逐段拆解:df.groupby(\"department\")[\"salary\"].mean()",
            full_code='df.groupby("department")["salary"].mean()',
            steps=[
                WalkthroughStep(segment="df", explain="觸發點:一份完整的員工資料表,每列一位員工,包含 department、salary 等欄位。"),
                WalkthroughStep(segment=".groupby(\"department\")", explain="演進脈絡第一步:依 department 欄的值,把所有列分成好幾組(Engineering一組、Sales一組、Marketing一組),此時還沒有任何計算,只是『分組完成』的中繼狀態。"),
                WalkthroughStep(segment="[\"salary\"]", explain="演進脈絡第二步:在每一組裡,只挑出 salary 這一欄準備進行計算,其他欄位(如 name)暫時不理會。"),
                WalkthroughStep(segment=".mean()", explain="最終呈現:對每一組的 salary 值分別計算平均數,結果是一個以「部門名稱」為索引、值為「該部門平均薪資」的 Series。"),
            ],
            final_output_note="最終你會得到類似:Engineering 84333.3 / Marketing 64333.3 / Sales 54666.7 這樣『一個部門對一個數字』的結果。",
        ),
    ),
    Unit(
        id="pd_merge_concat",
        stage="pandas",
        order=12,
        title="Merge 與 Concat",
        summary="把兩份資料表合併在一起——merge 依欄位值對應(像資料庫的 join),concat 單純上下或左右拼接。",
        concepts=[
            Concept(
                id="c_pd_merge_concat",
                title="merge / concat",
                what="pd.merge(df1, df2, on='key') 依共同欄位的值把兩個表『橫向』對應合併,類似資料庫的 join;pd.concat([df1, df2]) 單純把多個表『上下』(或指定 axis=1 左右)接起來。",
                why="真實資料常分散在多個表(例如員工表、部門表),需要合併才能一起分析;或是分批取得的資料需要接在一起。",
                problem="把邏輯上相關但實體上分開的資料組合成一份可以一起分析的表。",
                syntax="pd.merge(orders, customers, on='customer_id', how='left')\npd.concat([df_jan, df_feb], axis=0)  # 上下接,列增加",
                usage="訂單表跟顧客表各自存在時,要分析『哪個城市的顧客消費最高』,得先用 merge 把兩表依 customer_id 合併。",
                common_errors="merge 的 how 參數(inner/left/right/outer)沒設對,導致資料無故消失或出現非預期的空值。",
                confusions="merge 是『依值對應』橫向合併(欄位可能增加、列數依對應關係變化);concat 是單純『接起來』,預設是列數增加,不會依值做任何比對。",
            )
        ],
        examples=[
            Example(code='import pandas as pd\norders = pd.DataFrame({"order_id":[1,2],"customer_id":["C1","C2"],"amount":[100,200]})\ncustomers = pd.DataFrame({"customer_id":["C1","C2"],"city":["Taipei","Tainan"]})\nmerged = pd.merge(orders, customers, on="customer_id")\nprint(merged)', explain="依 customer_id 把訂單表跟顧客表合併,新表同時擁有 amount 和 city。"),
            Example(code='import pandas as pd\ndf1 = pd.DataFrame({"x":[1,2]})\ndf2 = pd.DataFrame({"x":[3,4]})\nprint(pd.concat([df1, df2], ignore_index=True))', explain="單純把兩個表上下接起來,ignore_index=True 讓索引重新從0編號。"),
        ],
        exercises=[
            Exercise(
                id="ex_pd_merge_1",
                prompt="給定 orders = pd.DataFrame({'customer_id':['C1','C2','C1'],'amount':[100,200,50]}) 與 customers = pd.DataFrame({'customer_id':['C1','C2'],'city':['Taipei','Tainan']}),請用 merge 建立 merged,再建立 total_by_city,內容是各城市總消費(merged.groupby('city')['amount'].sum())。",
                starter_code=(
                    "import pandas as pd\n"
                    "orders = pd.DataFrame({'customer_id':['C1','C2','C1'],'amount':[100,200,50]})\n"
                    "customers = pd.DataFrame({'customer_id':['C1','C2'],'city':['Taipei','Tainan']})\n"
                    "# 在這裡完成\n"
                ),
                checker_code=(
                    "import json\n"
                    "ok = 'merged' in dir() and 'total_by_city' in dir() and total_by_city['Taipei'] == 150 and total_by_city['Tainan'] == 200\n"
                    "print('RESULT_JSON:' + json.dumps({'passed': bool(ok), 'message': '正確!' if ok else \"提示:merged = pd.merge(orders, customers, on='customer_id')\"}))"
                ),
                hint="merged = pd.merge(orders, customers, on='customer_id')\ntotal_by_city = merged.groupby('city')['amount'].sum()",
            )
        ],
        questions=[
            Question(id="q_pd_mc_1", concept_id="c_pd_merge_concat", qtype="mc", prompt="想把兩份『欄位相同、內容是不同月份』的資料表接成一份,應該用?",
                      options=[("a", "pd.concat([df1, df2])"), ("b", "pd.merge(df1, df2)"), ("c", "df1 + df2"), ("d", "df1.append(df2, on='key')")],
                      answer="a", explanation="concat 是單純上下接起來,適合合併結構相同的資料;merge 是依值對應合併,用途不同。"),
        ],
    ),
    Unit(
        id="pd_apply_datetime",
        stage="pandas",
        order=13,
        title="apply 與日期時間基礎",
        summary="apply 讓你把自訂函式套用到整欄或整列;日期時間欄位需要先轉型才能做時間相關運算。",
        concepts=[
            Concept(
                id="c_pd_apply_datetime",
                title="apply 與日期時間",
                what="df['col'].apply(func) 把函式 func 套用到該欄每一個值;pd.to_datetime(df['col']) 把字串欄位轉成日期時間型態,轉換後可以用 .dt.year、.dt.month 等取出年月日。",
                why="有些轉換邏輯太特殊,沒有現成的 Pandas 函式可以直接用,這時就自己寫函式配合 apply;日期字串在做時間相關分析前一定要先轉型。",
                problem="apply 解決『套用自訂邏輯到整欄』的問題;to_datetime 解決『日期是字串,無法做日期運算』的問題。",
                syntax="df['level'] = df['score'].apply(lambda x: 'high' if x >= 80 else 'low')\ndf['sale_date'] = pd.to_datetime(df['sale_date'])\ndf['month'] = df['sale_date'].dt.month",
                usage="想從 sale_date 欄位算出『每月銷售額』,得先用 pd.to_datetime 轉型,再用 .dt.month 取出月份,才能搭配 groupby 使用。",
                common_errors="忘記日期欄位讀進來預設是字串(object)型態,直接用 .dt 存取會報錯,需要先 pd.to_datetime() 轉型。",
                confusions="能用內建向量化方法(如 .str、.dt)解決的,效能通常比 apply 好,apply 適合用在真的沒有現成方法、邏輯較特殊的情況。",
            )
        ],
        examples=[
            Example(code='import pandas as pd\ndf = pd.read_csv("content/datasets/employees.csv")\ndf["level"] = df["salary"].apply(lambda x: "high" if x >= 70000 else "normal")\nprint(df[["name","salary","level"]])', explain="用 apply 搭配自訂邏輯,依薪水分級。"),
            Example(code='import pandas as pd\ndf = pd.read_csv("content/datasets/sales_messy.csv")\ndf["sale_date"] = pd.to_datetime(df["sale_date"])\nprint(df["sale_date"].dt.month.head())', explain="轉型成日期後,用 .dt.month 取出月份。"),
        ],
        exercises=[
            Exercise(
                id="ex_pd_apply_1",
                prompt="讀取 employees.csv,用 apply 建立欄位 level:salary >= 70000 為 'high',否則為 'normal'。建立 high_count,內容是 level 為 'high' 的人數。",
                starter_code="import pandas as pd\ndf = pd.read_csv('content/datasets/employees.csv')\n# 在這裡完成\n",
                checker_code=(
                    "import json\n"
                    "ok = 'level' in df.columns and 'high_count' in dir() and high_count == 4\n"
                    "print('RESULT_JSON:' + json.dumps({'passed': bool(ok), 'message': '正確!' if ok else \"提示:df['level'] = df['salary'].apply(lambda x: 'high' if x>=70000 else 'normal')\"}))"
                ),
                hint="df['level'] = df['salary'].apply(lambda x: 'high' if x>=70000 else 'normal')\nhigh_count = (df['level']=='high').sum()",
            )
        ],
        questions=[
            Question(id="q_pd_apply_1", concept_id="c_pd_apply_datetime", qtype="bugfix", prompt="這段程式碼想取出月份,但報錯了,問題在哪?", code="df['sale_date'].dt.month",
                      options=[("a", "sale_date 讀進來是字串,需要先 pd.to_datetime() 轉型才能用 .dt"), ("b", "month 拼錯"), ("c", "dt 應改成 date"), ("d", "沒有問題")],
                      answer="a", explanation="CSV 讀進來的日期欄預設是字串型態,必須先轉型才有 .dt 存取器。"),
        ],
    ),
    Unit(
        id="pd_eda",
        stage="pandas",
        order=14,
        title="資料清理與探索性資料分析(EDA)綜合",
        summary="把前面所有 Pandas 技能串起來:讀取 → 檢查 → 清理 → 篩選 → 整理 → 統計分析,是進入 Capstone 前的最後一站。",
        concepts=[
            Concept(
                id="c_pd_eda",
                title="EDA 的標準流程",
                what="探索性資料分析(EDA)是拿到資料後,系統性地『先了解資料』的過程,標準流程大致是:讀取資料 → 檢查形狀與型態 → 找出缺失值與重複值 → 清理 → 篩選/分組觀察 → 得出初步結論。",
                why="沒有先做 EDA 就直接建模或下結論,很容易被資料中的錯誤或偏差誤導。",
                problem="在深入分析或建模之前,先系統性地認識資料的品質與樣貌。",
                syntax="df.shape → df.info() → df.isna().sum() → df.duplicated().sum() → 清理 → df.groupby(...) → 觀察與結論",
                usage="這正是 Stage 1 綜合實作要練習的完整流程,也是往後任何真實資料分析專案的第一天都會做的事。",
                common_errors="跳過檢查步驟直接分析,事後才發現資料裡有大量缺失值或重複值,導致結論不可靠。",
                confusions="EDA 不是『畫很多圖』,核心是『系統性地檢查資料品質與分佈』,圖表只是輔助工具之一。",
            )
        ],
        examples=[
            Example(
                code=(
                    'import pandas as pd\n'
                    'df = pd.read_csv("content/datasets/sales_messy.csv")\n'
                    'print(df.shape)\n'
                    'print(df.isna().sum())\n'
                    'print(df.duplicated().sum())\n'
                    'df["category"] = df["category"].str.lower()\n'
                    'df = df.drop_duplicates()\n'
                    'df["price"] = df["price"].fillna(df["price"].mean())\n'
                    'print(df.groupby("category")["price"].mean())'
                ),
                explain="一次走完:檢查形狀 → 檢查缺失 → 檢查重複 → 統一類別大小寫 → 移除重複 → 填補缺失 → 分組統計,這就是 EDA 的縮影。",
            ),
        ],
        exercises=[
            Exercise(
                id="ex_pd_eda_1",
                prompt="讀取 sales_messy.csv:(1) 把 category 欄統一轉小寫 (2) 移除完全重複列 (3) 把缺失的 price 用該欄平均值填補。最後建立 clean_shape,內容是清理後的 df.shape。",
                starter_code="import pandas as pd\ndf = pd.read_csv('content/datasets/sales_messy.csv')\n# 在這裡完成\n",
                checker_code=(
                    "import json\n"
                    "ok = 'clean_shape' in dir() and clean_shape[0] == 14 and df['category'].str.islower().all() and df['price'].isna().sum() == 0\n"
                    "print('RESULT_JSON:' + json.dumps({'passed': bool(ok), 'message': '正確!' if ok else '提示:依序 str.lower()、drop_duplicates()、fillna(mean)'}))"
                ),
                hint=(
                    "df['category'] = df['category'].str.lower()\n"
                    "df = df.drop_duplicates()\n"
                    "df['price'] = df['price'].fillna(df['price'].mean())\n"
                    "clean_shape = df.shape"
                ),
            )
        ],
        questions=[
            Question(id="q_pd_eda_1", concept_id="c_pd_eda", qtype="explain", prompt="用1-2句話說明,為什麼 EDA 要在清理資料『之前』先做,而不是等分析出結論後才檢查資料品質?",
                      keywords=["品質", "結論"], explanation="如果不先確認資料品質,分析出的結論可能建立在錯誤或有偏差的資料上,之後才發現會需要重做整個分析。"),
        ],
    ),
]
