
import cv2
import re
import pytesseract
from ultralytics import YOLO
from config import CAR_MODEL_PATH, LICENSE_PLATE_MODEL_PATH, VIDEO_PATH, TESSERACT_PATH, LICENSE_PLATE_PATTERN
from detection import detect_cars, detect_license_plates
from ocr import recognize_license_plate

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

car_detector = YOLO(CAR_MODEL_PATH)
license_plate_detector = YOLO(LICENSE_PLATE_MODEL_PATH)
license_plate_dict = {}

cap = cv2.VideoCapture(VIDEO_PATH)

def get_plate_key(x1, y1, x2, y2):
    return f"{int(x1)}_{int(y1)}_{int(x2)}_{int(y2)}"


while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 偵測車輛
    car_bboxes = detect_cars(frame, car_detector)

    for car_bbox in car_bboxes:
        x1, y1, x2, y2 = map(int, car_bbox[:4])
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

        car_crop = frame[y1:y2, x1:x2, :]
        if car_crop.size == 0:
            continue

        # 偵測車牌
        license_plate_bboxes = detect_license_plates(car_crop, license_plate_detector)

        for license_plate in license_plate_bboxes:
            lp_x1, lp_y1, lp_x2, lp_y2 = map(int, license_plate[:4])
            global_lp_x1, global_lp_y1 = x1 + lp_x1, y1 + lp_y1
            global_lp_x2, global_lp_y2 = x1 + lp_x2, y1 + lp_y2

            # 產生車牌唯一鍵
            plate_key = get_plate_key(global_lp_x1, global_lp_y1, global_lp_x2, global_lp_y2)

            # 如果之前已經辨識成功，就直接使用結果
            if plate_key in license_plate_dict and re.match(LICENSE_PLATE_PATTERN, license_plate_dict[plate_key]):
                corrected_text = license_plate_dict[plate_key]
            else:
                license_plate_crop = frame[global_lp_y1:global_lp_y2, global_lp_x1:global_lp_x2, :]
                if license_plate_crop.size == 0:
                    continue

                # OCR 辨識與文字校正
                corrected_text = recognize_license_plate(license_plate_crop)

                if corrected_text:
                    license_plate_dict[plate_key] = corrected_text
                    print(f"Stored license plate: {corrected_text}")

            # 畫出車牌框與辨識結果
            cv2.rectangle(frame, (global_lp_x1, global_lp_y1), (global_lp_x2, global_lp_y2), (255, 0, 0), 2)

            if corrected_text:
                cv2.putText(frame, corrected_text, (global_lp_x1, global_lp_y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                print(f"Detected license plate number: {corrected_text}")

    # 縮小畫面並顯示
    display_frame = cv2.resize(frame, None, fx=0.3, fy=0.3)
    cv2.imshow('License Plate Detection', display_frame)

    # 按 ESC 結束
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()