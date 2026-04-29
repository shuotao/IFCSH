# CORENET X IFC-SG 專案執行步驟與應用策略指南 (Instruction.md)

> [!IMPORTANT]
> **環境配置絕對路徑紀錄 (本機環境：C:\Users\Use\Desktop\IFCSH)**
> 為了確保團隊成員在不同電腦上能快速找到資源，以下為第一階段前置作業檔案的絕對路徑：
> 
> **A. 安裝程式 (軟體端)：**
> 1. **Revit 2025 Patch**: 透過 Autodesk Access 線上更新 (狀態：已安裝)
> 2. **Interoperability Tools**: `C:\Users\Use\Desktop\IFCSH\InteroperabilityTools_10_0_9_4966_2025.exe` (狀態：已備妥)
> 3. **Revit-IFC Exporter (v25.4.40)**: `C:\Users\Use\Desktop\IFCSH\IFC.for.Revit.2025.4.40.0.msi` (狀態：已安裝)
> 
> **B. 官方 Toolkit 資源 (數據端 - COP Edition 3)：**
> 4. **Shared Parameters (Step 1)**: `C:\Users\Use\Desktop\IFCSH\IFC+SG_SharedParameters_R2024.txt`
> 5. **Classification for Subtypes (Step 2)**: `C:\Users\Use\Desktop\IFCSH\IFC+SG Classification for Subtypes.xlsx`
> 6. **Property Set Mapping (Step 5)**: `C:\Users\Use\Desktop\IFCSH\IFC+SG Property Sets.txt`
> 7. **Model Checker Config (Step 4)**: `C:\Users\Use\Desktop\IFCSH\IFC+SG_ModelCheckerConfiguration_R2024.xml`
> 8. **SPT Configuration**: `C:\Users\Use\Desktop\IFCSH\IFC+SG_SPTConfiguration_R2024.xml`
> 9. **Dynamo Scripts (Step 3 參數填寫輔助)**:
>    - `C:\Users\Use\Desktop\IFCSH\1-Create a schedule to collect IFC parameters.dyn`
>    - `C:\Users\Use\Desktop\IFCSH\2-Export schedule into excel.dyn`
>    - `C:\Users\Use\Desktop\IFCSH\3-Import excel data to Revit elements.dyn`

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

在 Revit 模型製作過程中，請嚴格遵守以下線性工作流。建議**先理解手動流程，再執行自動化工具**。

### Step 1: 匯入 IFC-SG 參數 (Add IFC-SG Parameters)

#### 【初學者手動導引】
1. **連結共享參數**: `Manage > Shared Parameters` > 瀏覽並選擇 `IFC+SG_SharedParameters_R2024.txt`。
2. **注入參數**: `Manage > Project Parameters` > `Add` > 選擇 `Shared Parameter` > 挑選關鍵參數（如 `SystemName`）。
3. **對齊品類**: 針對 Plumbing 專業，務必勾選 `Pipes`, `Pumps`, `Plumbing Fixtures` 等品類。

#### 【專業者自動化回填 (推薦)】
使用 **Shared Parameters Tool (SPT)** 載入 `IFC+SG_SPTConfiguration_R2024.xml` 進行一鍵注入。
> [!CAUTION]
> **自動化執行但書 (關鍵提醒)：**
> 針對 2025 增加或需手動確認的欄位，請依照以下邏輯設定，確保 Model Checker 通過：
> - **必須勾選 (Essential)**: `IfcObjectType` (這是 SDT 運作的核心，務必確保最左側勾選框已勾，並設為 **Instance**)。
> - **Type (類型屬性)**: `BeamFaçade`, `DoubleBayFaçade`, `NumberOfRiser`, `PrefabricatedReinforcementCage`, `PrefinishedFaçade`, `SeatingCapacity`, `Watertight`。
> - **Instance (實體屬性)**: `ExternalReference`, `SiteName`, `IfcObjectType`。
> - **設定理由**: SDT 工具需要 `IfcObjectType` 參數存在於模型中才能寫入分類資料。若漏勾此項，SDT 將會噴出 "Parameter not found" 錯誤。

---

### Step 2: 定義 IFC 類別 (Populate IFC Classes)
- **嚴禁使用「Generic Models (常規模型)」**。所有的設備、管線都必須對應到正確的 Family Category。
- **操作建議**: 使用 **Standardized Data Tool (SDT)** 載入 `IFC+SG Classification for Subtypes.xlsx`，透過選單選取分類。

#### 【常見元件查詢路徑範例】
若在 SDT 中找不到特定組件（如 Tank），請嘗試以下官方路徑：
- **水箱 (Tank)**: `MEP > Plumbing > Tank > WATERSTORAGE` (或是 `IfcTank`)。
- **泵浦 (Pump)**: `MEP > Plumbing > Pump > CIRCULATINGPUMP / SUMPPUMP`。
- **閥門 (Valve)**: `MEP > Plumbing > Valve > CHECKVALVE / ISOLATINGVALVE`。
- **小撇步**: 若階層太深找不到，直接在 SDT 視窗的 **Search 框** 輸入英文單字（如 `Tank`），工具會自動過濾出所有相關的 IFC 分類。

---

### Step 3: 填寫專案特定數值 (Populate IFC-SG Values)

#### 【給排水/泵浦專業填寫規範】
- **參考依據**: `CORENET X COP 3.1 Edition 2025-12.pdf` **第 423 頁** (PDF 標註頁碼)。
- **關鍵參數填寫建議**:
  - **`SystemType`**: 必須符合官方預定義值（如 `Potable Water`, `Sanitary`, `Drainage`）。**大小寫必須完全一致**。
  - **`SystemName`**: 專案唯一編號（如 `L1-PW-01`）。
  - **`IsPotable`**: 飲用水系統務必勾選 `Yes`。
  - **`Watertight`**: 泵浦室與特定閥門務必依設計需求勾選。

#### 【自動化輔助】
- 使用資料夾內的 Dynamo 腳本（`1-Create a schedule...dyn`）自動抓取參數至明細表，建議在 Excel 中統一編輯後再回傳 Revit，以避開人為打字錯誤。

---

### Step 4: 參數合規性驗證 (Validate Parameters)
- 載入 `IFC+SG_ModelCheckerConfiguration_R2024.xml` 進行自動化掃描。

---

## 陸、 實戰故障排除 (Troubleshooting)

### 1. SPT 工具出現紅框或 Choose...
- **現象**: 載入 XML 後，部分參數（如 `SiteName`）顯示紅框且無法點擊 Run。
- **解決**: 必須手動在下拉選單指定 **Group** 為 `IFC Parameters`。若未完成此動作，模型將不會出現該欄位。

### 2. SDT 分類清單是空的 (找不到 Tank 等)
- **現象**: 點選 Assign Picklist 後視窗沒有內容，或找不到對應元件。
- **解決**: 
  1. 檢查是否已執行 `SDT > Setup` 並載入 `IFC+SG Classification for Subtypes.xlsx`。
  2. 確保 **Step 1 已點擊 Run**，若模型中沒有 `IfcObjectType` 參數，SDT 將無法寫入資料。

### 3. PDF 頁碼對照提醒
- 官方文件的 PDF 閱讀器顯示頁碼與右下角標註頁碼可能不符。
- **請統一以頁面右下角標註為準**（例如：給排水系統規範在 **第 423 頁**）。

### Step 5: 匯出 IFC 模型 (Export to IFC)
- **必須選擇 IFC 4x3** 版本的設定配置。
- 載入 `IFC+SG Property Sets.txt` 確保匯出時包含所有新加坡專用屬性。

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
