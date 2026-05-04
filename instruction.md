# CORENET X IFC-SG 專案執行 SOP (Standard Operating Procedure)

> [!IMPORTANT]
> **本文件為「零經驗無腦標準作業程序」**
> 本指南基於實際操作測試，逐步記錄了每一個動作、每一個可能踩到的地雷、以及每一個防呆機制。
> 即使沒有 BIM 工程背景的操作人員，只要嚴格按照本文件的步驟與順序執行，即可完成 IFC-SG 合規送審作業。
>
> **最高指導原則：**
> 1. **白名單原則**：只處理清單上列出的項目，不在清單上的一律跳過。
> 2. **不多做、不擔責**：官方工具沒有要求的，我們絕對不自行補充。
> 3. **不改寫官方腳本**：所有官方提供的 Dynamo 腳本保持原汁原味，僅透過調整 Revit 側的操作流程來適配。

---

## 壹、環境配置與檔案路徑

> **本機環境：`C:\Users\Use\Desktop\IFCSH`**

### A. 安裝程式 (軟體端)

| # | 項目 | 路徑 / 來源 | 狀態 |
|---|------|-------------|------|
| 1 | Revit 2025 Patch | 透過 Autodesk Access 線上更新 | 已安裝 |
| 2 | Interoperability Tools | `IFCSH\InteroperabilityTools_10_0_9_4966_2025.exe` | 已備妥 |
| 3 | Revit-IFC Exporter (v25.4.40) | `IFCSH\IFC.for.Revit.2025.4.40.0.msi` | 已安裝 |

### B. 官方 Toolkit 資源 (數據端 - COP Edition 3)

| # | 項目 | 檔案名稱 |
|---|------|----------|
| 4 | Shared Parameters | `IFC+SG_SharedParameters_R2024.txt` |
| 5 | Classification for Subtypes | `IFC+SG Classification for Subtypes.xlsx` |
| 6 | Property Set Mapping | `IFC+SG Property Sets.txt` |
| 7 | Model Checker Config | `IFC+SG_ModelCheckerConfiguration_R2024.xml` |
| 8 | SPT Configuration | `IFC+SG_SPTConfiguraton_R2024.xml` |
| 9 | Dynamo Script 1 | `1-Create a schedule to collect IFC parameters.dyn` |
| 10 | Dynamo Script 2 | `2-Export schedule into excel.dyn` |
| 11 | Dynamo Script 3 | `3-Import excel data to Revit elements.dyn` |

### C. 安裝檢查表

- [ ] Revit 2025 已更新至最新版本 (經由 Autodesk Access)
- [ ] 已安裝 Autodesk Interoperability Tools (2025 版本)
- [ ] 已從 GitHub 下載並覆蓋安裝最新版 Revit-IFC Exporter
- [ ] 已從 CORENET X 官網下載最新 IFC-SG Toolkit

> [!CAUTION]
> CORENET X 標準會定期更新（例如從 v1.0 更新至 v1.1），請務必在下載時確認文件上的 "Last Updated" 日期。

---

## 貳、工具角色定位 (必讀！操作前務必理解)

在開始操作之前，您必須清楚理解這四個工具各自扮演的角色：

### 工具一覽表

| 工具 | 比喻 | 功能 | 操作時機 |
|------|------|------|----------|
| **SPT** (Shared Parameters Tool) | 印出空白履歷表 | 在模型中「建立標準化的空白欄位」 | 步驟 1 (最先執行) |
| **Dynamo 腳本** | 把散落的履歷表收集整理成冊 | 自動產生明細表，將隱蔽的 IFC 欄位集中顯示 | 步驟 3 |
| **SDT** (Standardized Data Tool) | 選填政府規定的標準職業代碼 | 賦予元件合規的官方分類 (`IfcObjectType`) | 步驟 4 |
| **Model Checker** | 送審前的模擬考 | 自動掃描所有欄位，產出錯誤報告 | 步驟 5 (最後執行) |

### 關鍵觀念釐清

1. **SPT 執行完畢後，所有欄位都是空白的** — 這是正常的，因為 SPT 只負責「建欄位」。
2. **SDT 專門且主要用來填寫 `IfcObjectType`** — 它處理的是「政府規定的全大寫標準分類」（如 `WATERSTORAGE`），具備防呆的下拉選單機制，大小寫絕對不會錯。
3. **Dynamo 腳本負責「批次處理專案個別資料」** — 用來處理設計端自己定義的流水號、系統名稱等（如 `SystemName = L1-PW-01`），這些是每個元件都不同的資料，不歸 SDT 管。
4. **SDT 一次只能填入「一種分類」給「選取的元件」** — 但可以同時選取複數個相同類型的元件，一次批次寫入。例如選取 10 個水箱後，一次指定 `WATERSTORAGE`。

---

## 參、SOP 步驟總覽

```
步驟 1：導入參數 (SPT)
    ↓
步驟 2：盤點模型類別 (Revit Multi-Category Schedule)
    ↓
步驟 3：產生 IFC 明細表 (Dynamo)
    ↓
步驟 4：填寫官方分類 (SDT)
    ↓
步驟 5：合規性驗證 (Model Checker)
    ↓
步驟 6：匯出 IFC (Export)
```

---

## 肆、步驟 1：導入 IFC-SG 參數 (SPT)

### 目的
使用 Shared Parameters Tool (SPT) 將新加坡政府規定的所有 IFC 參數欄位，一次性導入到 Revit 模型中。

### 操作步驟
1. 開啟 Revit，載入目標模型。
2. 點擊上方功能區 (Ribbon) 的 **[Add-Ins]** 頁籤 ➔ 找到 **[Interoperability Tools]** 群組 ➔ 點擊 **[Shared Parameters Tool]**。
3. 在 SPT 介面中，**先點擊 [Setup]**：
   - 在 **Step 2: Shared Parameters Files** 區塊中，瀏覽並指定共享參數檔案路徑為：
     `C:\Users\Use\Desktop\IFCSH\IFC+SG_SharedParameters_R2024.txt`
   - 此步驟確保 SPT 知道要從哪份官方參數定義檔讀取欄位，**不可跳過**。若未指定，SPT 可能會使用錯誤的參數來源，導致後續欄位缺漏。
4. 回到主介面，點擊 **[Load Configuration]** ➔ 瀏覽並選擇 `IFC+SG_SPTConfiguration_R2024.xml`。
5. 點擊 **[Run]** 執行。

### ⚠️ 踩雷警告：SPT 出現紅框或 "Choose..."
- **現象**：載入 XML 後，部分參數（如 `SiteName`）顯示紅框且無法點擊 Run。
- **解決**：必須手動在下拉選單指定 **Group** 為 `IFC Parameters`。若未完成此動作，模型將不會出現該欄位。

### ⚠️ 踩雷警告：2025 版本新增欄位
針對 Revit 2025 增加或需手動確認的欄位，請依照以下設定：
- **必須勾選 (Essential)**：`IfcObjectType`（務必確保最左側勾選框已勾，並設為 **Instance**）。
- **Type (類型屬性)**：`BeamFaçade`, `DoubleBayFaçade`, `NumberOfRiser`, `PrefabricatedReinforcementCage`, `PrefinishedFaçade`, `SeatingCapacity`, `Watertight`。
- **Instance (實體屬性)**：`ExternalReference`, `SiteName`, `IfcObjectType`。

> [!CAUTION]
> **如果漏勾 `IfcObjectType`**，後續步驟 4 的 SDT 工具將會噴出 "Parameter not found" 錯誤，導致整個流程卡死。這是最常見的初學者失誤。

### 驗證方式
隨意點選模型中的一根管子或一個設備，在左側「Properties (屬性面板)」中往下滑動，應該會看到一大堆新出現的空白欄位（如 `IfcObjectType`、`SystemName` 等）。全部都是空白是正常的。

---

## 伍、步驟 2：盤點模型類別 (Multi-Category Schedule)

### 目的
在動手操作 Dynamo 腳本之前，先讓 Revit 自己告訴我們：「這個模型裡面到底裝了哪些種類的東西？各有幾個？」
這是整套 SOP 的「聖旨」— 後續所有操作都必須嚴格依據這張盤點表的結果。

### 操作步驟
1. 在 Revit 中，點擊上方功能區 (Ribbon) 的 **[View (視圖)]** 頁籤。
2. 點擊 **[Schedules (明細表)]** ➔ 選擇 **[Schedule/Quantities (明細表/數量)]**。
3. 在彈出的 "New Schedule" 對話框中，選擇 **`<Multi-Category>` (多重類別)**，按 OK。
4. 在 "Schedule Properties" 的 **Fields** 頁籤中，從左側 "Available fields" 加入以下欄位到右側：
   - **`Family and Type`**（族群與類型）
   - **`Category`**（類別）
   - **`Count`**（計數）
5. 切換到 **Sorting/Grouping** 頁籤：
   - 設定排序依據為 **`Category`**。
   - **取消勾選** 最下方的 `Itemize every instance (列舉每個例證)`。
6. 按 OK。

### 預期結果
您會得到一張簡潔的表格，列出模型中所有的元件類別與數量。例如：

| Category | Count |
|----------|-------|
| Generic Models | 9 |
| Mechanical Equipment | 39 |
| Pipe Fittings | 1258 |
| Pipes | 2500 |
| Plumbing Equipment | 4 |
| Plumbing Fixtures | 0 |
| Specialty Equipment | 12 |
| Pipe Accessories | 85 |

### ⚠️ 關鍵決策點：白名單篩選

> [!WARNING]
> **盤點表上出現的類別，不代表全部都要處理！**
> 必須使用「白名單 (Whitelist)」原則，只處理新加坡 IFC-SG 認可的 Revit Category。

#### 🔴 絕對不要處理的類別（以及原因）

| 類別 | 為什麼不能用 |
|------|-------------|
| **`Generic Models` (一般模型)** | 🚨 **致命地雷！** IFC-SG 嚴禁使用。如果照原樣送審，系統會直接退件。正確做法：找到這些物件，進入「編輯族群」，把它們的類別改為正確的機電類別。 |
| **`Pipe Accessories` (管配件/閥類)** | 屬於 Revit 的系統輔助分類，通常在 IFC 轉換時會自動對應，不需要人工賦予 `IfcObjectType`。 |
| **`Piping Systems` / `Duct Systems` 等系統類別** | 這些是 Revit 自動生成的虛擬系統群組，不是實體元件，無法也不需要賦予 IFC 分類。 |

#### 🟢 白名單 A：Plumbing (給排水) 專案

> **【死規矩】** 當你在盤點表看到結果後，**只允許**挑選以下清單上有出現的英文字放進 Dynamo 腳本：

| 白名單類別 | 中文名稱 | 典型內容物 |
|-----------|---------|-----------|
| `Mechanical Equipment` | 機械設備 | 泵浦 (Pump)、水箱 (Tank)、過濾器 |
| `Pipe Fittings` | 管接頭 | 彎頭 (Elbow)、三通 (Tee)、異徑接頭 |
| `Pipes` | 管 | 各種材質的水管 |
| `Plumbing Equipment` | 給排水設備 | 給排水專用設備 |
| `Specialty Equipment` | 特殊設備 | 特殊用途設備 |

#### 🟢 白名單 B：HVAC (空調通風) 專案

| 白名單類別 | 中文名稱 | 典型內容物 |
|-----------|---------|-----------|
| `Mechanical Equipment` | 機械設備 | 冰水主機 (Chiller)、空調箱 (AHU)、冷卻水塔 (Cooling Tower) |
| `Ducts` | 風管 | 各種材質的送/回風管 |
| `Duct Fittings` | 風管接頭 | 彎頭、三通、變徑接頭 |
| `Duct Accessories` | 風管配件 | 風門 (Damper)、風量調節閥 |
| `Air Terminals` | 出風口 | 出風口 (Diffuser)、回風口 (Grille) |
| `Flex Ducts` | 軟管 | 可撓式軟風管 |

#### 🟢 白名單 C：Fire Protection (消防) 專案

| 白名單類別 | 中文名稱 | 典型內容物 |
|-----------|---------|-----------|
| `Mechanical Equipment` | 機械設備 | 消防泵浦 (Fire Pump)、消防水箱 |
| `Pipe Fittings` | 管接頭 | 消防管路接頭 |
| `Pipes` | 管 | 消防水管 |
| `Sprinklers` | 灑水頭 | 各式灑水頭 (Sprinkler Head) |
| `Specialty Equipment` | 特殊設備 | 消防栓 (Fire Hose Reel)、滅火器箱 |
| `Fire Alarm Devices` | 火警設備 | 偵煙器 (Smoke Detector)、火警警報器 |

> [!TIP]
> **給管理者的備註**：如果盤點表上出現的類別不在上述對應系統的白名單中，操作人員應直接跳過，不要自行判斷。若有疑問，應回報給具工程背景的主管確認。
> 不同系統的白名單可能有重複的類別（如 `Mechanical Equipment` 同時出現在三張清單中），這是正常的，因為同一個 Revit Category 可能橫跨多個系統。

---

## 陸、步驟 3：產生 IFC 明細表 (Dynamo)

### 目的
使用官方 Dynamo 腳本 `1-Create a schedule to collect IFC parameters.dyn`，自動為步驟 2 篩選出的白名單類別建立明細表，並將所有隱蔽的 IFC 參數欄位自動拉出來排列整齊。

### 操作步驟

#### 3-1. 開啟 Dynamo 腳本
1. 確認 Revit 已開啟目標模型。
2. 點擊上方功能區 (Ribbon) 的 **[Manage (管理)]** ➔ **[Dynamo]**。
3. 在 Dynamo 畫面中點擊 **[Open (開啟)]**，瀏覽並打開 `1-Create a schedule to collect IFC parameters.dyn`。

#### 3-2. 設定 Categories 輸入節點
打開腳本後，看向畫面的**最左邊**，您會看到已有的 `Categories` 下拉選單節點。

**根據步驟 2 的白名單結果，您需要：**

1. **擴充清單 (List Create)**：點擊中間 `List Create` 節點上的 **`+` 號**，直到插槽顯示 `item0` 到 `item4`（總共 5 個洞）。
2. **複製類別節點**：點選最左邊的 `Categories` 節點，按 `Ctrl+C` 和 `Ctrl+V`，直到畫面上總共有 **5 個** `Categories` 節點。
3. **選擇白名單類別**：將這 5 個節點的下拉選單，分別選擇：
   - `Mechanical Equipment`
   - `Pipe Fittings`
   - `Pipes`
   - `Plumbing Equipment`
   - `Specialty Equipment`
4. **連線**：用滑鼠把這 5 個節點右邊的輸出點，分別拉線連到 `List Create` 的 5 個插槽。

> [!WARNING]
> **🚨 經實測驗證的超級大地雷：字首太像選錯了！**
>
> Dynamo 的下拉選單是按英文字母排序的，以下兩組名字極容易混淆：
>
> | ❌ 錯誤選擇 | ✅ 正確選擇 | 後果 |
> |------------|------------|------|
> | `Medical Equipment` (醫療設備) | `Mechanical Equipment` (機械設備) | 模型裡 0 個醫療設備，腳本會直接跳過，不產生明細表 |
> | `Plumbing Fixtures` (衛浴設備) | `Plumbing Equipment` (給排水設備) | 同上，模型裡 0 個衛浴設備，明細表不會產生 |
>
> **防呆方法**：請嚴格對照步驟 2 盤點表上的「完整英文單字」，一個字母都不能錯。
> **Dynamo 搜尋小撇步**：展開下拉選單後，直接用鍵盤快速敲打目標字首（如敲 `M-E` 跳到 Mechanical），不用辛苦滾動尋找。

#### 3-3. 確認其他節點設定
- **Code Block 節點**：保持預設的 `A+"_IFC"` 即可（腳本會自動用類別名稱加上 `_IFC` 作為明細表的名稱）。
- **Include BuiltIn Parameters in IFC Group**：保持 **`False`** 即可。

#### 3-4. 執行腳本
確認所有連線完成後，按下左下角的 **[Run (執行)]** 按鈕。

### 3-5. 驗證結果

#### 檢查點 1：核對明細表數量與名稱
1. 回到 Revit，在 **Project Browser (專案瀏覽器)** 中展開 **Schedules/Quantities (明細表/數量)**。
2. 應該會看到精準的 5 張新明細表：
   - `Mechanical Equipment_IFC`
   - `Pipe Fittings_IFC`
   - `Pipes_IFC`
   - `Plumbing Equipment_IFC`
   - `Specialty Equipment_IFC`

> [!WARNING]
> **如果少了幾張明細表？**
> 這是腳本內建的防呆機制在發威！腳本的 Python 程式碼裡有一段保護邏輯 (`if sEle == None: continue`)：
> 「如果進去模型裡找，發現這個類別的數量是 0 個（連一個樣本都沒有），就直接跳過，不建表。」
>
> **排查步驟**：
> 1. 回到步驟 2 的盤點表，確認該類別的 Count 是否真的 > 0。
> 2. 回到 Dynamo 畫面，逐一核對每個 `Categories` 節點的下拉選單，是否選錯了相似名稱的類別。
> 3. 修正後重新按 Run。

#### 檢查點 2：核對欄位表頭
1. **雙擊**打開其中一個明細表（例如 `Pipes_IFC`）。
2. 點擊左側屬性面板的 **Fields (欄位)**，查看右側的 **Scheduled fields (已排入欄位)**。
3. 應該會看到一系列由 SPT 工具（步驟 1）導入的 IFC 參數，例如：
   - `Type`, `ConstructionMethod`, `SystemName`, `SystemType`, `Gradient`, `Thickness`, `TradeEffluent`, `Perforated`, `PreInsulated`, `InnerDiameter`, `DemountableStructureAbovePipe`, `IfcObjectType` 等。

> [!NOTE]
> **「為什麼只看到一個 `Ifc` 開頭的？其他的呢？」**
> 這是非常常見的視覺誤解。新加坡官方在制定資料字典時，並沒有把每個字首都加上 "Ifc"。
> 例如 `SystemName`、`SystemType`、`Gradient`、`Thickness` 等，雖然沒有 "Ifc" 前綴，但它們 100% 都是官方規定的 IFC-SG 專屬送審參數。
> 只要出現在 Scheduled fields 清單裡的（除了 `Type` 是方便辨識用的以外），全部都是官方設定檔強制打進去的專屬欄位。

---

### 3-6. 必要的手動微調：為設備類明細表加入 `Family and Type` 欄位

> [!IMPORTANT]
> **為什麼需要這一步？**
> 官方 Dynamo 腳本只會自動帶入 `Type (類型)` 這個單一欄位，不會帶入完整的 `Family and Type (族群與類型)`。
> 對於「管線類」明細表（如 `Pipes_IFC`），這不是問題，因為管子都是同質的。
> 但對於「設備類」明細表（如 `Mechanical Equipment_IFC`），裡面可能混雜了泵浦、水箱、過濾器等不同設備。如果沒有 `Family and Type`，操作人員將無法分辨這些設備的身分，後續步驟 4 的 SDT 分類就會出錯。
>
> **本操作完全不需要修改官方 Dynamo 腳本。** 只是在 Revit 產出的明細表中，手動點擊加回一個 Revit 原生欄位（只需 3 秒鐘），屬於正常的 Revit 基礎操作。

**操作步驟（對以下明細表各做一次）：**
- `Mechanical Equipment_IFC`
- `Plumbing Equipment_IFC`
- `Specialty Equipment_IFC`

1. 雙擊打開明細表。
2. 點擊左側屬性面板的 **Fields (欄位)**。
3. 在左側 "Available fields" 清單中，找到 **`Family and Type`**。
4. 雙擊將它加到右側的 "Scheduled fields"。
5. **🔺 【關鍵】用右側的上移箭頭 ↑ 將 `Family and Type` 移到最上方（第一欄）。** 如果不移到第一欄，後續的 Sorting/Grouping 排序效果會不正確，操作人員將無法正確辨識設備身分。
6. 按 **OK**。
7. 進入 **Sorting/Grouping (排序/群組)** 頁籤：
   - 設定排序依據為 **`Family and Type`**。
   - **取消勾選** `Itemize every instance (列舉每個例證)`。
   - 按 **OK**。

**預期結果**：明細表會從幾百行縮減為數行，每行代表一種設備族群。例如 `Mechanical Equipment_IFC` 會顯示：

| Family and Type | Type |
|-----------------|------|
| ci_@P_Centrifugal Pump_Horizontal: 90 GPM | 90 GPM - 24 Foot Head |
| ci_@P_Storage Tank: 200 Gallon | 200 Gallon |
| M_Storage Tank - Vertical: 7600 L | 7600 L |
| M_Storage Tank - Vertical: 11400 L | 11400 L |
| ... | ... |

---

## 柒、步驟 4：填寫官方分類 (SDT)

### 目的
使用 Standardized Data Tool (SDT) 將新加坡政府規定的標準分類（全大寫英文單字），寫入每個元件的 `IfcObjectType` 欄位。

### 前置作業
1. 確認 SDT 已載入官方分類資料庫：點擊 **[SDT]** ➔ **[Setup]** ➔ 瀏覽並載入 `IFC+SG Classification for Subtypes.xlsx`。
2. 確認步驟 1 (SPT) 已成功執行，模型中已存在 `IfcObjectType` 參數。

### 核心觀念：兩種截然不同的操作情境

> [!IMPORTANT]
> **千萬不要盲目全選每一張明細表！**
> 這 5 張 `_IFC` 明細表必須分為兩種情境來處理，混淆將導致全盤皆輸。

#### 🟢 情境一：可以「全選」的明細表 (同質性高)

**適用明細表**：`Pipes_IFC`、`Pipe Fittings_IFC`

**為什麼可以全選？**
在 IFC 的底層邏輯裡，不管水管是 2 吋還是 4 吋、是 PVC 還是白鐵 (SUS304)、是熱水還是冷水，只要它是水管，它的 IFC 身分/類別通通都統一。材質差異屬於 Material (材質) 屬性的範疇，跟負責身分的 `IfcObjectType` 無關。

**操作步驟**：
1. 在明細表中全選所有行。
2. 執行「選取確認流程」（見下方 4-A 節）。
3. 打開 SDT，搜尋對應的分類關鍵字，Assign 即可。

#### 🔴 情境二：絕對「不可以全選」的明細表 (異質性高)

**適用明細表**：`Mechanical Equipment_IFC`、`Plumbing Equipment_IFC`、`Specialty Equipment_IFC`

**為什麼不可以全選？**
`Mechanical Equipment` 是一個超級大雜燴！裡面可能同時住著水箱 (Tank)、泵浦 (Pump)、過濾器等完全不同的設備。

**災難演練**：如果您全選後用 SDT 統一指定了 `WATERSTORAGE`，那麼模型裡所有的泵浦在新加坡審查系統裡都會被誤認為「長得很像泵浦的水箱」，導致退件。

**操作步驟**：
1. 依照步驟 3-6 的手動微調，確認明細表已有 `Family and Type` 欄位且已啟用 Sorting/Grouping。
2. 看著收合後的設備名稱，**依據 `Family and Type` 的特徵分批點擊**。
3. 每一批單獨執行「選取確認流程」（見下方 4-A 節）。
4. 對每一批分別打開 SDT，搜尋並指定正確的分類。

**實際範例**（依據實測截圖）：

| Family and Type 特徵 | 分批次序 | SDT 搜尋關鍵字 | 應指定的分類 |
|---------------------|---------|---------------|-------------|
| `Centrifugal Pump_Horizontal...` | 第 1 批 | "Pump" | ⚠️ 見下方「特殊情況處理」 |
| `Storage Tank: 200 Gallon` + 所有 `M_Storage Tank` 行 | 第 2 批 (可 Shift 多選) | "Tank" | 依實際用途選擇（見下方說明） |

---

### 4-A. 選取確認流程 (Isolate & Switch)

> [!IMPORTANT]
> **這是整套 SOP 中操作難度最高、最容易失敗的環節。**
> 請部下嚴格遵守以下「精確點擊步驟」，少一步都會導致選取失敗。

#### 方案 A：HI / HR 獨立顯示確認法 (推薦)

**前置條件**：明細表已啟用 Sorting/Grouping，且取消勾選 `Itemize every instance`。

1. **正確點選整行**：
   - 把滑鼠游標移到目標行**最左邊的灰色行標頭位置**點下去。
   - 整行變成藍色 = 選中了整個集合。
   - ⚠️ **不要只點文字儲存格**，那樣只會選中單一欄位。
   - 如需多選：點第一行後，**按住 Shift** 再點最後一行。

2. **在模型中大顯 (Highlight in Model)**：
   - 點擊明細表上方的 **[Highlight in Model]** 按鈕。
   - Revit 會跳轉到 3D 視圖，並彈出 "Show Elements in View" 小對話框。

3. **🔥 關閉對話框（絕對不要點擊背景！）🔥**：
   - 直接按下小對話框的 **[Close (關閉)]** 按鈕。
   - **千萬不要用滑鼠去點擊背後的模型畫面！** 只要不小心點到背景，原本選好的設備會瞬間被取消選取。

4. **按下快速鍵 `H` `I` (Isolate Element / 獨立顯示元素)**：
   - 雙手離開滑鼠，直接在鍵盤上依序敲擊 `H` 然後 `I`。
   - 畫面中除了剛剛選到的設備之外，整棟建築會**瞬間全部隱藏**。
   - **防呆效果**：部下可以直觀地看到畫面上只剩下「被選中的設備」，100% 證明沒有漏抓。

5. **確認數量**：
   - 看一眼左側「Properties (屬性面板)」最上方，應該會顯示類似 `Mechanical Equipment (5)` 的數字。
   - 括號內有複數數字 = 成功批次選取。

6. **執行 SDT 工具**：
   - 視覺確認無誤後，直接點開 SDT 進行 Assign。

7. **按下快速鍵 `H` `R` (Reset / 重設獨立顯示)**：
   - 填完後按 `H` 然後 `R`，整棟建築恢復原狀。

8. **按下 `Ctrl + Tab` (切換視窗)**：
   - 跳回明細表，繼續點擊下一批次。

#### 方案 B：備用方案 (在 3D 視圖中直接操作)

如果部下覺得明細表切換太混亂，可以改用以下方式：
1. 看著明細表上的設備名稱（例如 `Centrifugal Pump_Horizontal`）。
2. 切換回 3D 視圖，找到一顆該型號的設備。
3. 對著它 **點擊滑鼠右鍵** ➔ 選擇 **`Select All Instances (選取所有例證)`** ➔ 選擇 **`In Entire Project (在整個專案中)`**。
4. 屬性面板確認有括號 `(數量)` 後，打開 SDT 指定分類。

---

### 4-B. SDT 操作細節

#### 搜尋分類的正確方式
1. 打開 SDT 後，您會看到右上角有一個 **Filter (篩選)** 下拉選單。
2. **預設情況下**，Filter 會自動對應到您選取元件的 Revit Category（如 `Mechanical Equipment`）。
3. SDT 會只顯示新加坡政府認定屬於該 Category 的分類選項。

> [!WARNING]
> **⚠️ 經實測發現的重大陷阱：跨國標準衝突**
>
> Revit 的 Category 與新加坡 IFC-SG 的分類體系**並不是一一對應的**！
>
> **實際案例**：泵浦 (Centrifugal Pump) 在 Revit 裡被歸類在 `Mechanical Equipment`，但新加坡政府的 SDT 資料庫 (`IFC+SG Classification for Subtypes.xlsx`) 在 `Mechanical Equipment` 底下**只有**以下選項：
> - Hose Reel - `STANDBYFIREHOSE`
> - Refuse Chute 系列 - `REFUSECONTAINER`, `REFUSECOMPACTOR` 等
> - Tank 系列 - `DETENTIONTANK`, `RAINWATERHARVESTINGTANK`, `IRRIGATIONTANK`, `SPRINKLERTANK`, `BALANCINGTANK`, `SECTIONAL`, `RECHARGEWELL`
>
> **完全沒有 Pump 的分類！**
>
> 這代表新加坡政府在這份標準中，並未針對一般泵浦制定專屬的子類別標籤。

#### 🏆 SDT 分類填寫的最高指導原則

> **有查到 ➔ 點擊 Assign**
> 如果 SDT 清單中出現符合的選項，點擊 Assign 寫入 `IfcObjectType`。
>
> **沒查到 ➔ 直接跳過 (保持空白)**
> 如果搜尋不到（即使把 Filter 改成 `All` 仍找不到），**什麼動作都不用做！**
> 嚴禁自行手動打字發明或填補任何 IFC 參數。
> 這代表該設備非官方管控之節點。

> [!IMPORTANT]
> **合約責任與防禦性建模原則 (Defensive Modeling)**
>
> 如果新加坡政府的 CORENET X 標準（包含 SDT 官方表單）根本沒有列出某個項目，就代表在他們的自動化審查邏輯中，該設備並非關鍵的法規檢核點。
>
> 我們的立場：「已嚴格遵守並完全落實官方提供的 Toolkit 進行作業。官方清單上有的，一字不漏填寫；清單上沒有的，保持空白。」
>
> 若政府未來審查時認為有缺，那是他們應該盡到更新 SDT 標準資料庫的責任，而不是由承包商耗費人力去逆向猜測。
>
> **絕對不要自作聰明去手動補上 `IfcExportAs` 或其他自定義參數。** 不僅增加無意義的工時，萬一因為「主動補上」的參數導致退件或相容性錯誤，責任反而落到我們頭上。

#### 水箱 (Tank) 的分類細節
新加坡政府對水箱的要求非常細緻，不是只有一個通用的 `WATERSTORAGE`！
操作人員必須依照專案的「實際用途」，從以下清單中選擇最精確的分類：

| SDT 分類 | 對應用途 |
|---------|---------|
| `DETENTIONTANK` | 滯洪槽 |
| `RAINWATERHARVESTINGTANK` | 雨水回收槽 |
| `IRRIGATIONTANK` | 灌溉用水箱 |
| `SPRINKLERTANK` | 消防灑水用水箱 |
| `BALANCINGTANK` | 平衡水箱 |
| `SECTIONAL` | 組合式水箱 |
| `RECHARGEWELL` | 補注井 |

> [!TIP]
> 如果無法確定水箱的實際用途，應回報給具工程背景的主管確認，不要自行猜測填入。

---

## 捌、步驟 5：合規性驗證 (Model Checker)

### 目的
在匯出 IFC 之前，使用 Model Checker 進行「模擬考」，自動掃描所有欄位，找出遺漏或錯誤。

### 操作步驟
1. 點擊 **[Add-Ins]** ➔ **[Model Checker]**。
2. 載入 `IFC+SG_ModelCheckerConfiguration_R2024.xml`。
3. 點擊 **[Run Check]**。
4. 檢視報告：
   - **Error (錯誤)**：必須修正，否則送審會被退件。
   - **Warning (警告)**：建議修正，但不一定會被退件。
5. 對於每個 Error，可以點擊報告中的元件連結，系統會自動定位到該元件，方便修正。

### 驗證循環
```
執行 Model Checker ➔ 修正 Error ➔ 再次執行 ➔ 直到 0 Error
```

---

## 玖、步驟 6：匯出 IFC 模型 (Export)

### 操作步驟
1. 點擊 **[File]** ➔ **[Export]** ➔ **[IFC]**。
2. **必須選擇 IFC 4x3** 版本的設定配置。
3. 在 Property Sets 設定中，載入 `IFC+SG Property Sets.txt` 確保匯出時包含所有新加坡專用屬性。
4. 匯出後，**強烈建議使用第三方軟體驗證**（如 BIMcollab ZOOM）。

### 檔案大小限制
- **單一 IFC 檔案大小絕對不可超過 800 MB**。
- 若 MEP 模型過大，必須依據系統（MVAC、Plumbing、Fire Protection）或區域進行拆分。

---

## 拾、故障排除 (Troubleshooting)

### 1. SPT 工具出現紅框或 "Choose..."
- **現象**：載入 XML 後，部分參數顯示紅框且無法點擊 Run。
- **解決**：手動在下拉選單指定 Group 為 `IFC Parameters`。

### 2. SDT 分類清單是空的
- **現象**：點選 Assign Picklist 後視窗沒有內容。
- **解決**：
  1. 檢查是否已執行 `SDT > Setup` 並載入 `IFC+SG Classification for Subtypes.xlsx`。
  2. 確保步驟 1 已點擊 Run，若模型中沒有 `IfcObjectType` 參數，SDT 無法寫入資料。

### 3. SDT 搜尋不到設備分類（如 Pump）
- **現象**：在 SDT 中搜尋設備關鍵字，Filter 設為 `All` 仍找不到。
- **解決**：這不是錯誤！代表官方表單 (`IFC+SG Classification for Subtypes.xlsx`) 中沒有為該設備定義專屬的子類別。
- **正確做法**：保持 `IfcObjectType` 欄位空白，不要自行填寫。

### 4. Dynamo 執行後明細表數量不足
- **現象**：選了 5 個 Category 但只產出 3 張明細表。
- **解決**：
  1. 腳本有防呆機制，模型中數量為 0 的類別會被自動跳過。
  2. 核對下拉選單是否選錯了相似名稱：`Medical` vs `Mechanical`、`Fixtures` vs `Equipment`。

### 5. Highlight in Model 後選取跑掉
- **現象**：點擊 Highlight in Model 後，切換到 3D 視圖，但屬性面板顯示選取數量為 0。
- **解決**：
  1. 確認是點擊了「行標頭」而非文字儲存格。
  2. 關閉 "Show Elements in View" 對話框時，使用 Close 按鈕，絕對不要點擊背景。
  3. 使用快速鍵 `H` `I` 進行獨立顯示確認。

### 6. PDF 頁碼對照提醒
- 官方文件的 PDF 閱讀器顯示頁碼與右下角標註頁碼可能不符。
- **請統一以頁面右下角標註為準**（例如：給排水系統規範在第 423 頁）。

---

## 拾壹、實務策略補充

### 1. 空間與座標對齊
- **共用座標 (Shared Coordinates)**：所有模型必須使用 **SVY21** 座標系統。
- **樓層高程一致性**：MEP 的 Levels 必須與建築模型完全一致，建議使用 Copy/Monitor 連結建築模型高程。

### 2. 專業分工與邊界釐清
- 外部環境與景觀應由建築 (Architect) 負責。
- 外部的衛生下水道 (External Sanitary / IC) 由 MEP 負責建立並確保連接。

### 3. 品質保證與第三方覆核
匯出後強烈建議使用：
- **BIMcollab ZOOM** (免費)：檢查 IFC 屬性是否正確寫入。
- **BIM Vision**：單純的模型觀看。
- **Navisworks Manage**：碰撞檢查與統整。

### 4. 階段送審注意事項
- 目前重點在 **Design Gateway**，主要針對消防、空調、給排水。
- 設計變更後必須確保 IFC 資訊同步更新。

---

> [!NOTE]
> **版本紀錄**
> | 版本 | 日期 | 變更內容 |
> |------|------|---------|
> | 2.0.0 | 2026-05-04 | 基於實際操作測試，全面重寫為零經驗 SOP 格式，加入所有踩雷經驗與防呆機制 |
> | 1.0.0 | 初版 | 基於會議逐字稿整理的策略指南 |
