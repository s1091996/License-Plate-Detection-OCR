from ultralytics import YOLO


def detect_cars(frame, car_detector):
    """
    使用 YOLO 偵測影像中的車輛。
    class 2 為車輛。
    """
    results = car_detector(frame, classes=[2])
    car_bboxes = results[0].boxes.xyxy.cpu().numpy()

    return car_bboxes


def detect_license_plates(car_crop, license_plate_detector):
    """
    在車輛影像中偵測車牌。
    """
    results = license_plate_detector(car_crop)
    license_plate_bboxes = results[0].boxes.xyxy.cpu().numpy()

    return license_plate_bboxes