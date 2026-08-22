# -*- coding: utf-8 -*-
"""Stage 1 綜合實作:用 customers_messy.csv 走一遍『讀取→檢查→清理→篩選→排序→GroupBy→結論』。

每個步驟的 starter_code 都重新從讀檔開始(獨立子行程執行,彼此不共用記憶體狀態),
之後的步驟會在 prompt 中提示延續前一步的清理邏輯,checker 則各自重新計算一份參考答案來比對,
避免因為手動寫死數字而跟資料集內容脫鉤。
"""
from core.models import CapstoneStep

CAPSTONE_META = {
    "title": "Stage 1 綜合實作:顧客資料分析",
    "dataset": "customers_messy",
    "description": (
        "這份顧客資料(customers_messy.csv)有缺失值、重複紀錄、城市名稱大小寫不一致、"
        "以及不合理的年齡異常值。請依序完成六個步驟,實際走一遍完整的資料分析流程。"
    ),
}

STEPS = [
    CapstoneStep(
        id="cs_step1_load",
        title="Step 1:讀取與初步檢查",
        prompt="讀取 content/datasets/customers_messy.csv 存成 df。建立 n_rows(總列數)與 n_missing_age、n_missing_spent(分別是 age、total_spent 欄位的缺失值數量)。",
        starter_code="import pandas as pd\n# 在這裡完成\n",
        checker_code=(
            "import json, pandas as pd\n"
            "ref = pd.read_csv('content/datasets/customers_messy.csv')\n"
            "ok = ('n_rows' in dir() and 'n_missing_age' in dir() and 'n_missing_spent' in dir()\n"
            "      and n_rows == len(ref) and n_missing_age == ref['age'].isna().sum() and n_missing_spent == ref['total_spent'].isna().sum())\n"
            "print('RESULT_JSON:' + json.dumps({'passed': bool(ok), 'message': '正確!' if ok else '提示:isna().sum() 分別統計 age 與 total_spent 欄'}))"
        ),
        hint="df = pd.read_csv('content/datasets/customers_messy.csv')\nn_rows = len(df)\nn_missing_age = df['age'].isna().sum()\nn_missing_spent = df['total_spent'].isna().sum()",
    ),
    CapstoneStep(
        id="cs_step2_clean_city",
        title="Step 2:清理城市欄位",
        prompt="重新讀取資料,清理 city 欄位(去除頭尾空白、統一大小寫,建議用 .str.strip().str.title()),存回 df['city']。建立 unique_cities,內容是清理後不重複城市名稱的 set(應該有4個城市)。",
        starter_code="import pandas as pd\ndf = pd.read_csv('content/datasets/customers_messy.csv')\n# 在這裡完成\n",
        checker_code=(
            "import json, pandas as pd\n"
            "ref = pd.read_csv('content/datasets/customers_messy.csv')\n"
            "ref['city'] = ref['city'].str.strip().str.title()\n"
            "expected = set(ref['city'].unique())\n"
            "ok = 'unique_cities' in dir() and set(unique_cities) == expected and len(expected) == 4\n"
            "print('RESULT_JSON:' + json.dumps({'passed': bool(ok), 'message': '正確!' if ok else '提示:df[\"city\"].str.strip().str.title()'}))"
        ),
        hint="df['city'] = df['city'].str.strip().str.title()\nunique_cities = set(df['city'].unique())",
    ),
    CapstoneStep(
        id="cs_step3_missing_outliers",
        title="Step 3:處理離群值與缺失值",
        prompt=(
            "延續 Step 2 的城市清理,接著:(1) 移除 age 不合理的離群值(age < 0 或 age > 120 的列) "
            "(2) 用剩餘資料 age 欄的中位數(median)填補 age 的缺失值 "
            "(3) 用 total_spent 欄的平均值(mean)填補 total_spent 的缺失值。"
            "最後建立 df_clean 為完成上述清理的 DataFrame,並建立 remaining_rows,內容為 df_clean 的列數。"
        ),
        starter_code=(
            "import pandas as pd\n"
            "df = pd.read_csv('content/datasets/customers_messy.csv')\n"
            "df['city'] = df['city'].str.strip().str.title()\n"
            "# 在這裡完成:離群值處理、缺失值填補,結果存成 df_clean\n"
        ),
        checker_code=(
            "import json, pandas as pd\n"
            "ref = pd.read_csv('content/datasets/customers_messy.csv')\n"
            "ref['city'] = ref['city'].str.strip().str.title()\n"
            "ref = ref[(ref['age'].isna()) | ((ref['age'] >= 0) & (ref['age'] <= 120))].copy()\n"
            "ref['age'] = ref['age'].fillna(ref['age'].median())\n"
            "ref['total_spent'] = ref['total_spent'].fillna(ref['total_spent'].mean())\n"
            "ok = ('df_clean' in dir() and 'remaining_rows' in dir()\n"
            "      and remaining_rows == len(ref) and df_clean['age'].isna().sum() == 0 and df_clean['total_spent'].isna().sum() == 0\n"
            "      and df_clean['age'].max() <= 120 and df_clean['age'].min() >= 0)\n"
            "print('RESULT_JSON:' + json.dumps({'passed': bool(ok), 'message': '正確!' if ok else '提示:先篩掉 age<0 或 age>120 的列,再分別用 median/mean 填補'}))"
        ),
        hint=(
            "df = df[(df['age'].isna()) | ((df['age'] >= 0) & (df['age'] <= 120))].copy()\n"
            "df['age'] = df['age'].fillna(df['age'].median())\n"
            "df['total_spent'] = df['total_spent'].fillna(df['total_spent'].mean())\n"
            "df_clean = df\nremaining_rows = len(df_clean)"
        ),
    ),
    CapstoneStep(
        id="cs_step4_filter_sort",
        title="Step 4:篩選與排序",
        prompt="在完成 Step 3 清理的 df_clean 基礎上,篩選出 total_spent > 3000 的顧客存成 high_value,並依 total_spent 由高到低排序後,建立 top5,內容是消費前5名顧客(只保留 name、total_spent 兩欄)。",
        starter_code=(
            "import pandas as pd\n"
            "df = pd.read_csv('content/datasets/customers_messy.csv')\n"
            "df['city'] = df['city'].str.strip().str.title()\n"
            "df = df[(df['age'].isna()) | ((df['age'] >= 0) & (df['age'] <= 120))].copy()\n"
            "df['age'] = df['age'].fillna(df['age'].median())\n"
            "df['total_spent'] = df['total_spent'].fillna(df['total_spent'].mean())\n"
            "df_clean = df\n"
            "# 在這裡完成:high_value 與 top5\n"
        ),
        checker_code=(
            "import json, pandas as pd\n"
            "ref = pd.read_csv('content/datasets/customers_messy.csv')\n"
            "ref['city'] = ref['city'].str.strip().str.title()\n"
            "ref = ref[(ref['age'].isna()) | ((ref['age'] >= 0) & (ref['age'] <= 120))].copy()\n"
            "ref['age'] = ref['age'].fillna(ref['age'].median())\n"
            "ref['total_spent'] = ref['total_spent'].fillna(ref['total_spent'].mean())\n"
            "expected_high = ref[ref['total_spent'] > 3000]\n"
            "expected_top5_names = list(ref.sort_values('total_spent', ascending=False).head(5)['name'])\n"
            "ok = ('high_value' in dir() and 'top5' in dir()\n"
            "      and len(high_value) == len(expected_high) and list(top5['name']) == expected_top5_names)\n"
            "print('RESULT_JSON:' + json.dumps({'passed': bool(ok), 'message': '正確!' if ok else '提示:df_clean[df_clean[\"total_spent\"]>3000],再 sort_values 排序取前5'}))"
        ),
        hint="high_value = df_clean[df_clean['total_spent'] > 3000]\ntop5 = df_clean.sort_values('total_spent', ascending=False).head(5)[['name','total_spent']]",
    ),
    CapstoneStep(
        id="cs_step5_groupby",
        title="Step 5:分組統計",
        prompt="在 df_clean 基礎上,建立 city_avg_spent(各城市平均消費,Series)與 city_counts(各城市顧客數,Series)。",
        starter_code=(
            "import pandas as pd\n"
            "df = pd.read_csv('content/datasets/customers_messy.csv')\n"
            "df['city'] = df['city'].str.strip().str.title()\n"
            "df = df[(df['age'].isna()) | ((df['age'] >= 0) & (df['age'] <= 120))].copy()\n"
            "df['age'] = df['age'].fillna(df['age'].median())\n"
            "df['total_spent'] = df['total_spent'].fillna(df['total_spent'].mean())\n"
            "df_clean = df\n"
            "# 在這裡完成:city_avg_spent 與 city_counts\n"
        ),
        checker_code=(
            "import json, pandas as pd\n"
            "ref = pd.read_csv('content/datasets/customers_messy.csv')\n"
            "ref['city'] = ref['city'].str.strip().str.title()\n"
            "ref = ref[(ref['age'].isna()) | ((ref['age'] >= 0) & (ref['age'] <= 120))].copy()\n"
            "ref['age'] = ref['age'].fillna(ref['age'].median())\n"
            "ref['total_spent'] = ref['total_spent'].fillna(ref['total_spent'].mean())\n"
            "expected_avg = ref.groupby('city')['total_spent'].mean()\n"
            "expected_counts = ref.groupby('city').size()\n"
            "ok = ('city_avg_spent' in dir() and 'city_counts' in dir()\n"
            "      and city_avg_spent.round(2).equals(expected_avg.round(2)) and city_counts.equals(expected_counts))\n"
            "print('RESULT_JSON:' + json.dumps({'passed': bool(ok), 'message': '正確!' if ok else '提示:df_clean.groupby(\"city\")[\"total_spent\"].mean() 與 .size()'}))"
        ),
        hint="city_avg_spent = df_clean.groupby('city')['total_spent'].mean()\ncity_counts = df_clean.groupby('city').size()",
    ),
    CapstoneStep(
        id="cs_step6_conclusion",
        title="Step 6:分析結論",
        prompt="根據前面的分析,寫下你的結論(存入字串變數 conclusion,至少兩句話):(1) 哪個城市的平均消費最高?(2) 你在清理這份資料時,遇到了哪些主要的資料品質問題?",
        starter_code="conclusion = \"\"\"\n請在這裡寫下你的結論\n\"\"\"\n",
        checker_code=(
            "import json\n"
            "text = conclusion if 'conclusion' in dir() else ''\n"
            "ok = len(text.strip()) >= 20\n"
            "print('RESULT_JSON:' + json.dumps({'passed': bool(ok), 'message': '已記錄你的結論。' if ok else '請至少寫兩句話,說明你的發現與清理過程中遇到的問題。'}))"
        ),
        hint="至少提到一個城市名稱,以及你處理過的資料問題(缺失值/重複值/異常值/格式不一致)。",
    ),
]
