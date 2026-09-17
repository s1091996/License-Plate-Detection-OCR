# 車牌偵測與辨識系統

## 1. 專案名稱與簡介（Project Title & Overview）

**車牌偵測與辨識系統**

本專案使用 YOLOv8 與 Tesseract OCR，實作一個能從道路行車影片中自動找出車輛、定位車牌並辨識出車牌號碼的系統。

開發這個專案是為了解決行車影片中車牌辨識容易受到背景干擾，以及 OCR 文字辨識容易看錯相似字（例如英文字母 `O` 與數字 `0`、字母 `I` 與數字 `1`）的問題。系統先偵測車輛位置，再從車子範圍內切出車牌進行影像強化，並透過字元替換與格式檢查來提高辨識準確率。

使用者只要提供一段行車影片（如 `car.mp4`），執行主程式後便能在畫面上看到車輛與車牌的位置，並讀取辨識出的車牌號碼。

## 2. 功能特色（Features）

- 先用 `yolov8n.pt` 找出畫面中的車輛，再用 `license_plate_detector.pt` 從車輛範圍內找出車牌，減少背景干擾。
- **車牌影像強化處理**：
  - 將切出的車牌放大 2 倍，讓字體更清晰。
  - 轉為灰階並使用 OTSU 自動二值化與直方圖等化，加強黑白對比。
  - 使用雙邊濾波去除雜訊，同時保留文字邊緣。
  - 裁切去除周圍 10% 邊緣，避免車牌外框與螺絲干擾辨識。
- **車牌號碼校正與檢查**：
  - 使用 Tesseract OCR 讀取文字與各字元的辨識信心度。
  - 根據標準車牌格式（前 2 碼英文、中間 2 碼數字、後 3 碼英文）自動更正容易看錯的字（例如在數字位置將 `O` 換成 `0`，在英文位置將 `1` 換成 `I`）。
  - 若辨識字數大於等於 8 碼，自動取後 7 碼進行比對。
- **記住已辨識車牌**：根據車牌在畫面上的位置記錄辨識結果，只要該位置已經成功辨識出正確格式的車牌，就會直接沿用。
- **即時畫面標記與顯示**：在畫面上用紅框標記車輛、藍框標記車牌，並在車牌上方以綠字即時顯示辨識出的號碼，按下 ESC 鍵即可結束程式。

## 3. 系統流程／架構（System Architecture）

```text
輸入車輛影片（car.mp4）
        ↓
讀取影格並以 YOLOv8 偵測車輛（紅框）
        ↓
切出車輛範圍，偵測車牌位置（藍框）
        ↓
檢查該位置是否已成功辨識過車牌
   ├── 是：直接沿用已記錄的車牌號碼
   └── 否：進行車牌影像前處理（放大、灰階、二值化、去噪）
        ↓
使用 Tesseract OCR 讀取文字與信心度
        ↓
依格式規則校正易錯字元（如 O/0、I/1）並驗證格式
        ↓
畫面標示結果並於終端機印出車牌號碼
```

- `main.py`：程式主要執行檔案，負責讀取影片、呼叫偵測與辨識函式、記錄已辨識的車牌，並在畫面上繪製框線與文字。
- `detection.py`：負責目標偵測，包含偵測車輛的 `detect_cars()` 與偵測車牌的 `detect_license_plates()`。
- `ocr.py`：負責車牌影像前處理（`preprocess_license_plate`）、呼叫 Tesseract OCR 辨識，以及文字校正邏輯（`correct_license_plate`）。
- `config.py`：存放所有參數設定，包含模型權重檔路徑、輸入影片路徑、Tesseract 執行檔路徑、OCR 參數、車牌正則規則與字元替換表。

## 4. 專案結構（Project Structure）

```text
Final/
├── .gitignore
├── config.py
├── detection.py
├── license_plate_detector.pt
├── main.py
├── ocr.py
└── yolov8n.pt
```

| 檔案 | 用途 |
| --- | --- |
| `main.py` | 主程式；讀取影片、整合偵測與 OCR 流程並顯示辨識畫面。 |
| `detection.py` | YOLO 車輛與車牌偵測功能。 |
| `ocr.py` | 車牌影像強化、Tesseract OCR 辨識與號碼校正邏輯。 |
| `config.py` | 集中管理模型路徑、影片路徑、Tesseract 設定與車牌格式規則。 |
| `yolov8n.pt` | YOLOv8 官方模型權重檔，用來偵測車輛。 |
| `license_plate_detector.pt` | 車牌偵測模型權重檔，用來定位車牌位置。 |

## 5. 安裝與快速開始（Installation & Quick Start）

### 必要工具

- Python 3.8 以上版本
- [Tesseract-OCR](https://github.com/UB-Mannheim/tesseract/wiki)（文字辨識引擎）

### 安裝步驟

1. **下載專案**

   ```bash
   git clone https://github.com/s1091996/Final.git
   cd Final
   ```

2. **建立並啟動虛擬環境**

   - **Windows**：
     ```powershell
     python -m venv venv
     .\venv\Scripts\activate
     ```

3. **安裝必要套件**

   ```bash
   pip install ultralytics opencv-python pytesseract numpy
   ```

4. **安裝與設定 Tesseract OCR**

   - **Windows**：
     下載並安裝 [Tesseract-OCR 安裝檔](https://github.com/UB-Mannheim/tesseract/wiki)（預設安裝路徑為 `C:\Program Files\Tesseract-OCR\tesseract.exe`）。若安裝在其他路徑，請打開 `config.py` 修改 `TESSERACT_PATH`。
     安裝後需將 `config.py` 內的 `TESSERACT_PATH` 改為 `'tesseract'`。

5. **執行程式**

   ```bash
   python main.py
   ```

## 6. 使用範例（Usage / Examples）

直接執行 `main.py`：

```bash
python main.py
```

### 執行說明

1. 程式啟動後會讀取 `car.mp4` 影片，並開啟標題為 `License Plate Detection` 的視窗。
2. 畫面中的車子會被標上**紅色方框**，車牌會被標上**藍色方框**。
3. 成功辨識出號碼後，車牌上方會顯示**綠色文字**，終端機也會同步印出辨識結果：

```text
Text trimmed to last 7 characters: NAI3NRU
Stored license plate: NA13NRU
Detected license plate number: NA13NRU
```

4. 想要關閉程式時，只要點擊影片視窗並按下鍵盤的 <kbd>ESC</kbd> 鍵即可退出。

## 7. 結果（Results）

### 車牌校正範例

在實際影片測試中，校正機制能成功修正 OCR 容易看錯的字元：

| 原始 OCR 辨識結果 | 規則校正後結果 | 說明 |
| --- | --- | --- |
| `NAI3NRU` | `NA13NRU` | 第 3 碼為數字欄位，自動將字母 `I` 修正為數字 `1`。 |

## 8. 限制與注意事項（Limitations / Notes）

- **需安裝 Tesseract-OCR**：執行前必須在電腦上安裝 Tesseract，且 `config.py` 中的 `TESSERACT_PATH` 必須對應到正確的執行檔路徑，否則會出現找不到檔案的錯誤。
- **車牌格式限定**：目前 `config.py` 與 `ocr.py` 設定的檢查規則為特定 7 碼格式（2 碼英文 + 2 碼數字 + 3 碼英文，如 `NA13NRU`）。若要辨識台灣車牌或其他格式，需自行修改 `config.py` 中的 `LICENSE_PLATE_PATTERN` 與 `ocr.py` 中的字元位置判定邏輯。
