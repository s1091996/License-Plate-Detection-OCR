# 車牌偵測與辨識系統 (License Plate Detection and Recognition System)

## 1. 專案名稱與簡介（Project Title & Overview）

**車牌偵測與辨識系統 (License Plate Detection and Recognition System)**

本專案的核心目標是基於 YOLOv8 物件偵測與 Tesseract OCR 文字辨識技術，針對動態道路車輛影片即時進行車輛定位、車牌擷取與號碼格式校正。

在智慧交通管理、道路監控與停車場自動化等應用中，車牌辨識是至關重要的技術環節；然而在動態行駛環境下，直接對整張影像進行文字辨識往往會受到複雜背景干擾，且 OCR 容易對相似字元（如 0 與 O、1 與 I、8 與 B）產生誤判。本專案先鎖定車輛再擷取車牌，並結合影像增強預處理與正則表達式字元信心度進行修正，提升車牌文字辨識的準確度。系統透過讀取影片，在畫面上追蹤標註車輛與車牌，並儲存已正確辨識的車牌號碼。

---

## 2. 功能特色（Features）

- 首先利用 `yolov8n.pt` 偵測影像中的車輛目標，排除非車輛背景雜訊。再將車輛裁切區域傳入 `license_plate_detector.pt` 模型，定位車牌邊界。
- **車牌影像預處理**
  - 放大尺寸：採用雙立方插值（Cubic Interpolation）將車牌局部影像放大 2 倍，增強文字邊緣解析度。
  - 灰階與對比增強：轉為單通道灰階圖後，進行直方圖等化（Histogram Equalization）提高明暗對比。
  - 閥值處理與去噪：透過 OTSU 自動二值化分離文字與底板，並套用雙邊濾波（Bilateral Filter）去除噪點同時保留邊緣銳利度。
  - 邊界裁切：自動裁切車牌中央 90% 區域，排除車牌外框、螺絲固定孔或車身接縫造成的 OCR 誤判。
- **字元信心度分析與格式校正（OCR Correction & Regular Expression Validation）**
  - 透過 `pytesseract.image_to_data` 取得每個辨識字元的信心值（Confidence score）。
  - 內建混淆字元映射機制（`CHAR_MAP`：如 `0 ↔ O`、`1 ↔ I`、`5 ↔ S`、`8 ↔ B`），依據車牌格式預期的字元型態（字母或數字）優先選用高信心候選字。
  - 支援格式長度修正（當辨識字數大於等於 8 碼時自動擷取後 7 碼），並依據標準車牌正則表達式（`^[A-Z]{2}\d{2}[A-Z]{3}$`）驗證最終結果。
- **車牌辨識結果空間快取（Spatial Key Caching）**
  - 根據車牌全圖像素座標建立唯一識別鍵（`x1_y1_x2_y2`）。
  - 當特定位置之車牌已成功辨識並符合規格時自動快取，後續幀若處於相同座標範圍則直接沿用歷史結果，避免後續影格因動態模糊覆蓋正確辨識值。
- **即時視覺化繪圖與顯示（Real-time Visualization）**
  - 即時於影像影格上繪製紅色車輛框（Red Bounding Box）、藍色車牌框（Blue Bounding Box），並於車牌上方標註綠色識別字串（Green Text）。
  - 畫面自動等比縮小（0.3x）以便於在各式螢幕解析度下流暢監看。

---

## 3. 系統流程／架構（System Architecture）

系統從輸入影片到完成車牌文字辨識並呈現結果的完整運作流程如下：
```text
影片輸入 (car.mp4)
        ↓
車輛目標偵測 (YOLOv8: yolov8n.pt)
        ↓
車牌位置偵測 (YOLO: license_plate_detector.pt)
        ↓
全圖座標轉換與快取比對 (Global Coordinates & Cache Check)
        ↓
車牌影像預處理 (放大2x → 灰階 → OTSU二值化 → 等化 → 雙邊濾波 → 裁切90%)
        ↓
Tesseract OCR 辨識與信心度擷取 (--psm 7)
        ↓
字元規則驗證 (CHAR_MAP 替換 & Regex Check)
        ↓
儲存快取與繪圖顯示 (OpenCV 視窗輸出)
'''
