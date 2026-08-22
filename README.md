# 數據分析 × 機器學習學習工作台(第一版:Python → NumPy → Pandas）

一個可實際操作的 Streamlit 學習工作台:學習 → 實作 → 執行 → 練習 → 測驗 → 弱點追蹤 → 複習 → 進度,完整循環。

## 啟動方式

```bash
pip install -r requirements.txt
streamlit run app.py
```

啟動後瀏覽器會自動開啟 `http://localhost:8501`。

## 資料保存

所有學習進度、練習紀錄、測驗結果、弱點追蹤、綜合實作進度都保存在 `data/workbench.db`(單一 SQLite 檔案)。關閉工作台後再重新啟動,這些紀錄都會保留。若想重新開始,刪除這個檔案即可(會遺失所有紀錄)。

## 程式碼執行的安全性說明

「實作區」「練習區」「綜合實作」裡你寫的程式碼,會在**子行程(subprocess)** 中於你自己的電腦上真實執行,並有 8 秒逾時保護,避免無窮迴圈卡住工作台。因為是單人本機使用、不對外開放,這個防護等級是合理且足夠的。

已知限制:Windows 平台沒有 `resource` 模組可做記憶體用量限制,所以目前只有時間逾時保護,沒有記憶體用量限制。

## 部署到 Streamlit Community Cloud

之後若要部署上線:
1. 把這個專案推上 GitHub。
2. 到 [share.streamlit.io](https://share.streamlit.io) 連接 repo,指定 `app.py` 為進入點。
3. 注意:Streamlit Community Cloud 的檔案系統不保證重啟後保留,`data/workbench.db` 在雲端環境可能不是永久保存——雲端部署時的資料持久化方案需要另外規劃(例如外部資料庫),本機使用不受影響。

## 專案結構

- `app.py`、`pages/`:Streamlit 頁面
- `core/`:資料庫存取、程式碼執行、批改、進度與弱點邏輯
- `content/`:課程內容(Python 基礎、NumPy、Pandas)、關卡題組、Capstone 規格、練習資料集

## 範圍

第一版僅涵蓋 Python 基礎 → NumPy → Pandas,不包含 Scikit-learn / 機器學習 / 深度學習內容。
