
CAR_MODEL_PATH = 'yolov8n.pt'
LICENSE_PLATE_MODEL_PATH = 'license_plate_detector.pt'

VIDEO_PATH = 'car.mp4'

TESSERACT_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
OCR_CONFIG = '--psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

LICENSE_PLATE_PATTERN = r'^[A-Z]{2}\d{2}[A-Z]{3}$'

CHAR_MAP = {
    '0': 'O',
    'O': '0',
    '1': 'I',
    'I': '1',
    '5': 'S',
    'S': '5',
    '8': 'B',
    'B': '8'
}