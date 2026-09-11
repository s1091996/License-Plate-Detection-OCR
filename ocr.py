
import cv2
import pytesseract
import re
from string import ascii_uppercase, digits
from config import TESSERACT_PATH, OCR_CONFIG, LICENSE_PLATE_PATTERN, CHAR_MAP

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

LETTERS = list(ascii_uppercase)
DIGITS = list(digits)

def preprocess_license_plate(image):
    # 放大影像 2 倍
    image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    # 轉為灰度
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # OTSU 閾值處理
    _, gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # 提升對比
    gray = cv2.equalizeHist(gray)
    # 去除噪點
    processed_image = cv2.bilateralFilter(gray, 11, 17, 17)
    # 裁剪中間 90%
    height, width = processed_image.shape[:2]
    crop_percentage = 0.9
    new_width = int(width * crop_percentage)
    new_height = int(height * crop_percentage)
    start_x = (width - new_width) // 2
    start_y = (height - new_height) // 2
    end_x = start_x + new_width
    end_y = start_y + new_height
    return processed_image[start_y:end_y, start_x:end_x]

def correct_license_plate(text, confidence_data):
    text = text.upper().replace(' ', '').strip()

    # 如果文字長度 >= 8，取後 7 個字
    if len(text) >= 8:
        text = text[-7:]
        print(f"Text trimmed to last 7 characters: {text}")

    # 如果原始文字已符合格式，直接返回
    if len(text) == 7 and re.match(LICENSE_PLATE_PATTERN, text):
        return text

    corrected_text = [''] * 7

    for i in range(7):
        expected_type = 'letter' if i in [0, 1, 4, 5, 6] else 'digit'
        candidates = confidence_data.get(i, [])

        if candidates:
            # 選擇符合預期類型的候選字元
            valid_candidates = [
                (char, conf) for char, conf in candidates
                if (char in LETTERS if expected_type == 'letter' else char in DIGITS)
            ]

            # 如果沒有符合的候選字元，嘗試常見 OCR 錯誤對應
            if not valid_candidates:
                valid_candidates = [
                    (CHAR_MAP.get(char, char), conf) for char, conf in candidates
                    if CHAR_MAP.get(char, char) in (LETTERS if expected_type == 'letter' else DIGITS)
                ]

            # 取信心值最高的字元
            if valid_candidates:
                best_char, best_conf = max(valid_candidates, key=lambda x: x[1])
                corrected_text[i] = best_char
            elif i < len(text):
                char = CHAR_MAP.get(text[i], text[i])
                corrected_text[i] = char if char in (LETTERS if expected_type == 'letter' else DIGITS) else ''
        elif i < len(text):
            char = CHAR_MAP.get(text[i], text[i])
            corrected_text[i] = char if char in (LETTERS if expected_type == 'letter' else DIGITS) else ''

    corrected_text = ''.join(corrected_text)

    # 驗證校正後是否符合車牌格式
    if len(corrected_text) == 7 and re.match(LICENSE_PLATE_PATTERN, corrected_text):
        return corrected_text

    return text

def recognize_license_plate(image):
    # 車牌影像預處理
    processed_image = preprocess_license_plate(image)

    # OCR 辨識並取得每個文字的信心值
    ocr_result = pytesseract.image_to_data(
        processed_image,
        config=OCR_CONFIG,
        output_type=pytesseract.Output.DICT
    )

    text_list = ocr_result['text']
    confidences = ocr_result['conf']

    # 收集 OCR 結果
    confidence_data = {}
    char_index = 0
    combined_text = ''

    for i, char in enumerate(text_list):
        if char.strip() and confidences[i] != -1:
            confidence_data[char_index] = confidence_data.get(char_index, []) + [
                (char.upper(), confidences[i])
            ]
            combined_text += char.upper()
            char_index += 1

    # 校正車牌文字
    corrected_text = correct_license_plate(
        combined_text,
        confidence_data
    )

    return corrected_text

