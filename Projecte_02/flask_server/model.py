from paddleocr import PaddleOCR
from ultralytics import YOLO
import cv2
from config import Config

def cargar_modelo_yolo():
    try:
        model_matr = YOLO(Config.MODEL_PATH)
        return model_matr
    except FileNotFoundError as e:
        raise Exception(f"Error al cargar el modelo: {e}")

def cargar_modelo_ocr():
    try:
        ocr = PaddleOCR(use_angle_cls=True, lang='es')
        return ocr
    except Exception as e:
        raise Exception(f"Error al cargar el modelo OCR: {e}")
    
def predecir_yolo(photo, model):
    results = model.predict(
        source=photo,
        conf=0.25,
        save=False,
        save_txt=False,
        verbose=False
    )
    return results[0]

def predecir_ocr(image, ocr_engine):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)
    try:
        result = ocr_engine.ocr(binary, cls=True)
        if result and result[0]:
            return result[0][0][1][0]  
        return None
    except Exception as e:
        print(f"❌ Error en OCR: {str(e)}")
        return None