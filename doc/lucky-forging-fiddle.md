# 數據分析 × 機器學習學習工作台 — 第一版（Python → NumPy → Pandas）

## Context

使用者要的不是課程網站或題庫，而是一個可實際操作的 Streamlit 學習工作台，涵蓋「學習 → 實作 → 執行 → 練習 → 測驗 → 弱點追蹤 → 複習 → 進度」完整循環，第一版範圍鎖定 Python 基礎 → NumPy → Pandas。經 `grill-me` 訪談確認關鍵決策：

- **技術棧**：Streamlit（本機開發，未來部署到 Streamlit Community Cloud；不用 Vercel/GitHub Pages，因為它們無法跑有狀態的 Python 伺服器）
- **程式碼執行**：本機真實執行，用子行程（subprocess）跑，加逾時保護
- **資料保存**：SQLite（單一 .db 檔）
- **AI/LLM**：第一版不做，全部用規則式/固定內容判斷正確性與弱點

`impeccable` 用於這個工作台的 UI/UX 規劃（介面屬於 **Operate** 模式：使用者要完成任務，重點是資訊層級清楚、狀態一致、可掃描，不是視覺表演）。`python-onboarding` 的「觸發點→演進脈絡→最終呈現」拆解方法論，直接借來設計「程式碼閱讀」教學元件（例如逐段拆解 `df.groupby(...)["salary"].mean()`）。

專案目錄目前是空的（`D:\files\learn_data_analysis`），屬於全新專案，無需相容既有程式碼。

---

## 專案結構

```
learn_data_analysis/
├── app.py                          # 入口：Dashboard / 學習路線總覽
├── pages/
│   ├── 1_📖_課程學習.py
│   ├── 2_💻_實作區.py
│   ├── 3_✍️_練習區.py
│   ├── 4_🧠_測驗.py
│   ├── 5_🚪_關卡.py                 # Stage Gate
│   ├── 6_🎯_弱點複習.py
│   ├── 7_🏆_綜合實作.py             # Stage 1 Capstone
│   └── 8_📊_學習進度.py
├── core/
│   ├── db.py                       # SQLite schema + CRUD
│   ├── models.py                   # Unit / Exercise / Question / dataclasses
│   ├── executor.py                 # subprocess 執行使用者程式碼（逾時保護）
│   ├── grading.py                  # 測驗自動評分、練習 checker 執行
│   ├── progress.py                 # 狀態機：未開始/學習中/已練習/需複習/已掌握
│   ├── weakness.py                 # 弱點記錄 + 簡易間隔複習排程
│   └── content_loader.py           # 讀取 content/ 底下的單元定義
├── content/
│   ├── python_basics/units.py
│   ├── numpy_basics/units.py
│   ├── pandas_basics/units.py
│   ├── gates.py                    # 兩個 Stage Gate 的題組
│   ├── capstone.py                 # 綜合實作規格與評分規則
│   └── datasets/                   # 練習用小型 CSV + 資料集說明
├── data/
│   └── workbench.db                # 執行時建立，.gitignore
├── .streamlit/config.toml
├── requirements.txt
└── README.md                       # 如何啟動、資料保存位置說明
```

## 資料模型（SQLite，`core/db.py`）

- `unit_progress(unit_id, status, opened_at, last_updated)` — 狀態：not_started / in_progress / practiced / mastered
- `exercise_submissions(id, unit_id, exercise_id, code, passed, message, submitted_at)`
- `quiz_attempts(id, unit_id, question_id, concept_id, is_correct, answer, attempted_at)`
- `concept_weakness(concept_id, unit_id, wrong_count, correct_streak, status, next_review_due, last_seen_at)` — status: needs_review / recovering / resolved
- `gate_results(stage, passed, score, attempted_at)`
- `capstone_progress(step_id, status, submitted_code, passed, notes, updated_at)`

單一使用者、無登入，DB 只存一份紀錄，不需 user_id。

## 核心邏輯

**`executor.py`**：把使用者程式碼寫到暫存 `.py`，用 `subprocess.run([sys.executable, tmp_path], timeout=8, capture_output=True)` 執行，回傳 stdout/stderr/是否逾時/是否 exception。Windows 沒有 `resource` 模組可用做記憶體限制，v1 用「timeout + 獨立子行程崩潰不影響主程式」作為防護，README 會註明此限制。

**練習題自動批改**：學生程式碼 + 隱藏測試片段一起組成暫存檔（測試片段 import 學生定義的函式/變數，assert 預期結果，最後印出 `RESULT_JSON:{...}` 一行），executor 執行後解析該行取得 pass/fail 與訊息。

**測驗批改（`grading.py`）**：依題型（選擇/判斷/看程式猜結果/找 Bug/補程式/簡答比對關鍵字/小型分析題）分別比對，每題綁定 1 個以上 `concept_id`。

**弱點追蹤（`weakness.py`）**：答錯 → `wrong_count+1`、`status=needs_review`、`next_review_due=now+1day`；再次答對 → `correct_streak+1`，streak 達 2 才轉 `resolved`，否則維持 `recovering` 並延後下次複習間隔（1d→3d→7d，簡化版間隔重複）。單元的「已掌握」判定 = 測驗通過 **且** 該單元底下所有 concept 都不是 needs_review。

**Stage Gate（`pages/5_🚪_關卡.py` + `content/gates.py`）**：獨立題組，未達 75% 或關鍵 concept 未過，顯示需要補強的具體項目與連結，不解鎖下一 Stage；允許重考。

## 內容範圍（依使用者清單，聚焦數據分析所需子集）

- **Python 基礎**（約 12 個單元）：變數與型態、數值運算、字串、list、tuple、dict、set、條件判斷、for/range、while、function、comprehension、exception 基礎、import 與模組概念
- **NumPy**（約 10 個單元）：ndarray 與建立、shape/ndim/dtype、indexing/slicing、boolean indexing、vectorization、broadcasting、aggregation、reshape/axis、NaN 處理、與 list/Pandas 的關係
- **Pandas**（約 14 個單元）：Series/DataFrame、建立與 read_csv、head/tail/info/describe、欄位選取、loc/iloc、條件篩選、增刪改欄位、sort_values、缺失值、重複值、groupby/aggregation、merge/concat、apply、日期時間、資料清理與 EDA 綜合

每單元內容結構固定七問（是什麼/為什麼/解決什麼問題/語法/數據分析情境/常見錯誤/易混淆點），1-2 個範例、1-2 題練習（含 checker）、3-5 題測驗（混合題型）。

**程式碼閱讀元件**：借用 `python-onboarding` 的拆解邏輯，做成一個可重用的 UI 元件（`core/models.py` 內的 `CodeWalkthrough` 結構 + 對應顯示元件），對鏈式呼叫（如 `df.groupby(...)["salary"].mean()`）逐段標出：這段是什麼、輸入輸出、常見誤解，用在 Pandas 單元。

**資料集**：`content/datasets/` 準備 3 份，難度遞增：(1) 乾淨的小型員工資料 (2) 帶缺失值/重複值的銷售資料 (3) Capstone 用、格式不一致 + 異常值的顧客資料，並附中文欄位說明 metadata。

## Stage 1 綜合實作（Capstone）

`content/capstone.py` 定義多步驟任務（讀取 → 檢查 → 清理缺失值 → 條件篩選 → 排序 → groupby 聚合 → 統計結論），`pages/7_🏆_綜合實作.py` 讓使用者分段提交程式碼、逐步驗證，最後依 `capstone_progress` + 全站 `concept_weakness` 產出報告：已掌握 / 需加強 / 主要弱點 / 下一階段準備度（僅呈現，不開發 ML 內容）。

## UI/UX 設計（Operate 模式，依 impeccable 原則）

- 側邊欄常駐學習路線樹（Stage > Unit），狀態圖示（灰/藍/琥珀/綠）+ 弱點數量徽章
- `app.py` 首頁：今天可學什麼（下一個建議單元）+ 待複習數量 + 簡要進度
- 課程頁固定七段式結構、實作/練習頁編輯器 + 執行按鈕 + 結果區三段式版面，測驗頁單題聚焦
- 進度頁：Stage 進度條 + 單元狀態表，弱點複習頁：依到期日排序的複習佇列
- 用 `.streamlit/config.toml` 設定主題色，少量必要 CSS（狀態徽章顏色），不做多餘裝飾

## 依賴套件（`requirements.txt`）

`streamlit`, `pandas`, `numpy`, `streamlit-ace`（程式碼編輯器語法高亮，比 text_area 更接近真實 IDE 體感）

## 實作階段

1. 專案骨架：目錄、requirements.txt、db.py schema、`.streamlit/config.toml`、app.py 導覽骨架
2. 核心模組：executor / grading / progress / weakness / content_loader，並用簡單腳本自測 executor
3. Python 基礎內容 + 對應頁面串接（學習/實作/練習/測驗）
4. NumPy 內容 + Python→NumPy 關卡
5. Pandas 內容（含資料集）+ NumPy→Pandas 關卡
6. 進度頁、弱點複習頁
7. Stage 1 綜合實作
8. impeccable 風格 UI 打磨一輪（首頁、側邊欄、狀態視覺化、程式碼閱讀元件）
9. 本機啟動並實際走一遍完整流程驗證（含關閉重開確認資料保存）

## 驗證方式

用 `preview_start` 啟動 `streamlit run app.py`，在瀏覽器中實際：開啟首頁 → 進入一個 Python 單元學習 → 寫程式碼執行 → 完成練習 → 做測驗並故意答錯以確認弱點被記錄 → 查看弱點複習頁出現該項目 → 查看進度頁狀態變化 → 重新整理/重啟伺服器確認 SQLite 資料仍在。過程中檢查 console/network 是否有錯誤。
