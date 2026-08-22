# -*- coding: utf-8 -*-
"""每份練習資料集的說明:代表什麼、每欄含意、資料型態、已知問題、可以回答的問題。"""

DATASETS = {
    "employees": {
        "file": "content/datasets/employees.csv",
        "title": "員工基本資料(乾淨版)",
        "description": "一間小公司 10 位員工的基本資料,用於練習最基礎的 DataFrame 操作,資料本身乾淨、沒有缺失或錯誤。",
        "rows_mean": "一列代表一位員工",
        "columns": [
            ("employee_id", "int", "員工編號"),
            ("name", "str", "姓名"),
            ("department", "str", "部門(Engineering / Sales / Marketing)"),
            ("salary", "int", "月薪(新台幣)"),
            ("years_experience", "int", "年資(年)"),
        ],
        "known_issues": "無(乾淨資料,適合初次練習)。",
        "sample_questions": ["各部門平均薪資是多少?", "年資最高的員工是誰?", "哪個部門的人數最多?"],
    },
    "sales_messy": {
        "file": "content/datasets/sales_messy.csv",
        "title": "銷售訂單資料(含缺失與重複)",
        "description": "某小型網路商店的訂單紀錄,用於練習缺失值與重複值的資料清理。",
        "rows_mean": "一列代表一筆訂單",
        "columns": [
            ("order_id", "int", "訂單編號"),
            ("product", "str", "商品名稱"),
            ("category", "str", "商品類別(注意:大小寫不一致,如 Electronics / electronics / ELECTRONICS)"),
            ("price", "float", "單價(部分缺失)"),
            ("quantity", "int", "數量(部分缺失)"),
            ("sale_date", "str", "銷售日期(部分缺失)"),
        ],
        "known_issues": "price、quantity、sale_date 有缺失值;category 大小寫不一致(需要統一);有一筆訂單(order_id 1001)被重複記錄了兩次。",
        "sample_questions": ["各類別的總銷售額是多少?", "去除重複訂單後,實際訂單數是多少?", "哪個商品賣得最多?"],
    },
    "customers_messy": {
        "file": "content/datasets/customers_messy.csv",
        "title": "顧客資料(Capstone 用,問題較多)",
        "description": "某會員系統匯出的顧客資料,用於 Stage 1 綜合實作,問題比前兩份資料集更真實、更多元。",
        "rows_mean": "一列代表一位顧客",
        "columns": [
            ("customer_id", "str", "顧客編號"),
            ("name", "str", "姓名"),
            ("age", "float", "年齡(有缺失,也有不合理的異常值,例如 -5 或 150)"),
            ("city", "str", "所在城市(大小寫不一致、有多餘空白,如 'Taipei '、'taipei'、'TAIPEI')"),
            ("signup_date", "str", "註冊日期"),
            ("total_spent", "float", "累計消費金額(部分缺失)"),
        ],
        "known_issues": "age 有缺失值與不合理異常值;city 同一個城市有多種寫法;total_spent 有缺失值;有完全重複的顧客紀錄(如 C001 與 C010、C018)。",
        "sample_questions": ["清理後,各城市顧客的平均消費是多少?", "有多少筆重複紀錄需要移除?", "年齡欄位中哪些值明顯不合理,該怎麼處理?"],
    },
}
