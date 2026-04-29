# CORENET X IFC-SG 專案執行步驟與應用策略指南 (Instruction.md)

基於「C2D_IFC-SG Demonstration Meeting」的簡報與會議逐字稿內容，本指南詳細梳理了新加坡政府 CORENET X 專案中針對 IFC-SG (Industry Foundation Classes - Singapore) 模型的提交策略、執行步驟與應用細節。

## 壹、 IFC-SG 核心策略概述

新加坡政府推動 CORENET X 的核心目標在於**統一 BIM 模型的提交標準**，以自動化或半自動化的方式進行法規審查（Regulatory Approvals）。
- **單一標準格式**：強制要求所有專案提交 **IFC 4x3** 格式的模型，並配合官方提供的 IFC-SG Toolkit。
- **跨專業協同送審**：建築 (Arch)、結構 (C&S) 與機電 (MEP) 雖然各自建立模型並可分拆檔案，但最終必須完美對齊（Shared Coordinates SVY21），並由各專業的 QP (Qualified Persons) 共同聯合送審 (Joint Submission)。
- **自動化合規性檢測**：官方系統會透過機器自動讀取 IFC 參數與欄位，若參數未填或設錯類別，會直接遭到退件。

---

## 貳、 專案執行前置作業 (Pre-Requisites)

為了確保專案在不同設備上均能完整執行，**本專案已定案統一使用 Revit 2025 版本**。在進入建模或產出模型之前，必須完成以下環境與軟體的配置：

### 1. 更新 BIM 軟體與外掛
- **Revit 2025 最新修補程式 (Patches/Updates)**：
  - **官方連結**：[Autodesk Account (manage.autodesk.com)](https://manage.autodesk.com/)
  - **說明**：請登入您的 Autodesk 帳戶，進入「所有產品與服務」 > 「Revit」 > 「檢視詳細資料」 > 「更新」，下載並安裝對應 2025 版本的最新補丁（例如 Revit 2025.1）。
  - **快捷方式**：您也可以直接從電腦安裝的 **Autodesk Access** (原 Autodesk Desktop App) 進行一鍵更新。
- **Revit Interoperability Tool (BIM 互操作性工具)**：
  - **官方連結**：[Autodesk Interoperability Tools 官方網站](https://www.interoperabilitytools.com/)
  - **下載路徑**：同樣可在 Autodesk Account 的「擴展程式 (Extensions)」中找到。
  - **包含內容**：此工具包包含 Shared Parameters Tool、Model Checker 等關鍵組件，是符合 IFC-SG 標準的核心工具。
- **Revit-IFC App 及 Revit-IFC Exporter**：
  - **官方連結 (GitHub - 最快更新)**：[Autodesk/revit-ifc Releases](https://github.com/Autodesk/revit-ifc/releases)
  - **官方連結 (App Store)**：[Autodesk App Store](https://apps.autodesk.com/)
  - **重要說明**：為了支援 **IFC 4x3 Schema**，強烈建議從 GitHub 下載最新釋出的 MSI 安裝檔。GitHub 是 Autodesk 官方維護此開源外掛的地方，版本通常比內建版本更新，能解決許多匯出錯誤。

### 2. 下載並套用 CORENET X 官方工具包 (IFC-SG Toolkit)
新加坡政府將所有的 IFC-SG 規範文件與工具集中在 CORENET X 資源中心。

- **官方資源入口**：
  - 官方連結：[CORENET X Official Portal](https://www.corenet.gov.sg/)
  - 資源中心：[CORENET X Resources & Guides](https://www.corenet.gov.sg/general/corenet-x-onboarding.aspx)
- **IFC-SG Toolkit (包含 Shared Parameters、Validation 及 Mapping files)**：
  - 下載頁面：[BCA CORENET X - IFC-SG Resource Toolkit](https://www1.bca.gov.sg/regulatory-info/building-control/corenet-x/ifc-sg-resource-toolkit)
  - **具體包含文件**：
    - **Shared Parameters File (.txt)**：用於將新加坡規定的參數導入 Revit。
    - **Excel Mapping files**：用於設定 Revit 類別與 IFC 類別的對應。
    - **Model Checker Configuration (.xml)**：用於 Revit Interoperability Tool，驗證模型是否符合 IFC-SG 標準。
    - **IFC-SG How-To Guide (Revit)**：官方的操作手冊（PDF）。

### 安裝檢查表總結：
- [ ] 檢查 Revit 2025 版本是否為最新 (經由 Autodesk Access)。
- [ ] 安裝 Autodesk Interoperability Tools (2025 版本)。
- [ ] 至 GitHub 下載並覆蓋安裝最新版 Revit-IFC Exporter。
- [ ] 從 CORENET X 官網 下載最新的 IFC-SG Industry Mapping Excel 與 Shared Parameters 檔案。

> [!CAUTION]
> 由於 CORENET X 標準會定期更新（例如從 v1.0 更新至 v1.1），請務必在下載時確認文件上的 "Last Updated" 日期，以確保符合目前的審查標準。

---

## 參、 5 步標準執行工作流 (5 Steps to Prepare IFC-SG Model)

在 Revit 模型製作過程中，請嚴格遵守以下線性工作流：

### Step 1: 匯入 IFC-SG 參數 (Add IFC-SG Parameters)
- 使用 IFC-SG Toolkit 將官方要求的必要欄位 (Fields) 注入至 Revit 模型中。

### Step 2: 定義 IFC 類別 (Populate IFC Classes)
- **嚴禁使用「Generic Models (常規模型)」**。所有的設備、管線都必須對應到正確的 Family Category，以確保轉換時能精準對應至 IFC Entities（例如：`IfcWall`, `IfcBeam`, 或是特定的 MEP 設備）。
- 使用官方提供的 Mapping Table（Excel 或 CSV 表格）確保 Revit 分類與 IFC 類別一致。

### Step 3: 填寫專案特定數值 (Populate IFC-SG Values)
- 填寫各元件在 IFC-SG 中被要求標示的數值。
- **策略重點**：善用下拉選單與工具包自動帶入功能，減少手動輸入（Manual Typing）以避免人為拼寫錯誤。

### Step 4: 參數合規性驗證 (Validate Parameters)
- 匯出前，利用 Revit Schedules (明細表) 自行稽核，確保所有必要參數 (Mandatory Parameters) 沒有空白。
- 也可以使用 IFC-SG Toolkit 內建的 Model Checker，讓系統自動掃描模型中是否有缺失或錯誤的參數格式。

### Step 5: 匯出 IFC 模型 (Export to IFC)
- 在 Revit 中選擇「Export to IFC」，並且**必須選擇 IFC 4x3** 版本的設定配置 (Schema)。

---

## 肆、 專案應用策略與實務細節 (Submission Good Practices)

### 1. 檔案大小與拆分策略 (800MB 限制)
- **單一 IFC 檔案大小絕對不可超過 800 MB**。
- **拆分策略**：若 MEP 模型過大，必須依據系統 (如：MVAC 空調、Plumbing 給排水、Fire Protection 消防) 或 區域 (Zone/Building) 進行模型拆解。
- 專案實務上，像 F10E、C10 等多棟建築的專案，可依據 IDA 需求拆分為不同的 IFC 檔案個別提交，但基準座標必須一致。

### 2. 空間與座標對齊 (Geospatial & Level Alignment)
- **共用座標 (Shared Coordinates)**：所有模型必須使用 **SVY21** 座標系統，確保 Arch、C&S、MEP 在 CORENET X 平台上能完美重疊。
- **樓層高程一致性**：MEP 的樓層設定 (Levels) 必須與建築模型 (Arch) 「完全一致」。強烈建議使用「複製/監視 (Copy/Monitor)」功能直接連結建築模型的高程，避免任何微小誤差。

### 3. 專業分工與邊界釐清 (Scope of Works)
- **外部環境與景觀 (External/Site/Landscape)**：應由**建築 (Architect)** 負責包含在其模型範圍內。
- **MEP 特定設備**：發電機 (Diesel Generator) 的排煙管 (Exhaust) 位置等，需由建築端在模型中配合預留或置入；而外部的衛生下水道 (External Sanitary / IC) 則由 MEP (如 CDCI/C2D) 負責建立並確保連接。

### 4. 品質保證與第三方軟體覆核 (QA & Review)
- 不能只信任 Revit 匯出的結果。模型匯出後，**強烈建議使用第三方軟體驗證**。
- **推薦工具**：
  - **BIMcollab ZOOM** (免費軟體)：非常適合用來整合與檢查所有專業 (Federated Models) 的 IFC 模型，並確認 IFC 屬性是否正確寫入。
  - **BIM Vision**：適合單純的模型觀看。
  - **Navisworks Manage (NWD)**：可用於提交給內部統包或業主 (如 C2D/CDCI) 進行最終的 Clash Detection (碰撞檢查) 與統整。

## 伍、 階段送審注意事項 (Gateway Submissions)
- 目前的重點在於 **Design Gateway**，主要針對關鍵系統（如消防、空調、給排水）。
- 在 Design Gateway 通過後，若發生設計變更（例如排水量大幅增加導致管線重拉），必須注意重新定義並確保 IFC 資訊同步更新。
- 所有的修改與整合，最終都會匯聚至 C2D / CDCI 進行總體檢查，並由各專業 QP 同時向當局提交。
