# License Plate Detection and OCR
A computer vision project for detecting vehicles, locating license plates, and recognizing license plate characters from video.

## Features
* Vehicle detection using YOLO
* License plate detection using YOLO
* License plate image preprocessing
* Character recognition using Tesseract OCR
* License plate format validation and character correction

## Technologies
* Python
* YOLO
* OpenCV
* Tesseract OCR
* NumPy
* Jupyter Notebook

## Pipeline
```text
Video
  ↓
Vehicle Detection
  ↓
License Plate Detection
  ↓
License Plate Preprocessing
  ↓
Tesseract OCR
  ↓
License Plate Validation
  ↓
Recognized License Plate
```

## How to Run
Install the required Python packages and configure the paths in `config.py`.
Then run:
```bash
python main.py
```
The YOLO model weights and input video are not included in this repository because of file size limitations.
