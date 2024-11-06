# 開發學習專案說明文件

## 概述

本專案目前僅供個人使用與學習，首次創建於 **2024/11/01**。由於 Windows 與 Linux 的環境變數存在差異，暫時使用 Windows 進行開發與測試。目前透過 [![ngrok](https://img.shields.io/badge/ngrok-Online-brightgreen)](https://ngrok.com/) 測試將服務開放至網際網路，未來計劃實現無需透過 ngrok 即可公開。

## 功能概覽

### 已實現功能

| 功能             | 進度     | 更新日期     | 備註                                                       |
| ---------------- | -------- | ------------ | ---------------------------------------------------------- |
| **颱風假查詢**   | ✅ 已完成 | 2024/11/01  | 爬取[行政院人事行政總處颱風訊息](https://www.dgpa.gov.tw/typh/daily/nds.html) |
| **查詢功能**     | ✅ 已完成 | 2024/11/02  | 各縣市天氣預報、空氣品質查詢                                |
| **用戶管理**     | ✅ 已完成 | 2024/11/04  | 登入功能、註冊功能                                                 |
| **檔案管理**     | ✅ 已完成 | 2024/11/01  | 使用 Flask 的 **Blueprints** 進行模組化管理                |

### 待實現功能

| 功能               | 進度       | 預計完成時間 | 備註                                  |
| ------------------ | ---------- | ------------ | ------------------------------------- |
| 更多查詢功能       | ⏳ 開發中   | 待定         | 敬請期待                              |
| **日誌記錄**       | ⏳ 開發中   | 待定         | 實現 **Log 日誌** 功能                |
| **服務公開**       | ⏳ 開發中   | 待定         | 無需透過 **ngrok** 將服務公開至網際網路 |
| **用戶管理**       | ⏳ 開發中   | 待定         | 忘記密碼、刪除帳號功能 |
| **使用Permission** | ⏳ 開發中  | 待定          | 可以使用權限進行一些使用 |

## 技術細節

- **資料庫**
  - 預計使用 **SQLite** 進行用戶資訊管理 | ✅ 已完成 2024/11/05

- **開發環境**
  - 由於環境變數差異，目前在 Windows 平台上開發測試

## 圖片展示

![我就爛](https://megapx-assets.dcard.tw/images/7e898349-582c-481d-88bd-7a98370be5cd/full.jpeg)

## 徽章

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-development-orange)

## 備註

- 本專案仍在持續開發中，未來將陸續增加新功能並優化現有功能
- 歡迎提出建議與意見，以提升專案品質

---

**更新日期：2024/11/05**
