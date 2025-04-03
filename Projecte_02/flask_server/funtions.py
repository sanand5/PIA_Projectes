import cv2
from model import predecir_yolo, predecir_ocr
import base64
import numpy as np
from config import Config
import os
import uuid

def base64_to_cv2(base64_string):
    image_bytes = base64.b64decode(base64_string)
    np_array = np.frombuffer(image_bytes, dtype=np.uint8)
    return cv2.imdecode(np_array, cv2.IMREAD_COLOR)

def obtener_bbox(result, max_len=1):
    boxes_with_confs = [(box.xyxy, box.conf.item()) for box in result.boxes]
    boxes_sorted = sorted(boxes_with_confs, key=lambda x: x[1], reverse=True)
    recuadros = [box[0] for box in boxes_sorted[:max_len]]
    return recuadros

def recortar_matricula(bboxes, photo_path):
    img = cv2.imread(photo_path)
    if img is None:
        raise ValueError(f"No se pudo leer la imagen: {photo_path}")
    
    recortes = []
    for i, bbox in enumerate(bboxes):
        coords = bbox.tolist()[0]
        x1, y1, x2, y2 = map(int, coords)
        
        h, w = img.shape[:2]
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(w, x2), min(h, y2)
        
        if x2 > x1 and y2 > y1:
            recorte = img[y1:y2, x1:x2]
            recortes.append(recorte)  
    return recortes

def predecir_bbox(photo_path, model, max_len=1):
    result = predecir_yolo(photo_path, model)
    bboxes = obtener_bbox(result, max_len)
    recortes = recortar_matricula(bboxes, photo_path)
    return recortes


def obtener_matricula(photo_b64, model_yolo, model_ocr):
    try:
        photo = base64_to_cv2(photo_b64)
        photo_path = os.path.join(Config.BASE_PATH, f"photo_{uuid.uuid4()}.jpg")
        cv2.imwrite(photo_path, photo)  # Guarda la imagen en formato JPG        

        matriculas_img_sort_conf = predecir_bbox(photo_path, model_yolo)
        if not matriculas_img_sort_conf:
            return None
        matricula_path = os.path.join(Config.BASE_PATH, f"matricula_{uuid.uuid4()}.jpg")
        cv2.imwrite(matricula_path, matriculas_img_sort_conf[0])

        matricula_string = predecir_ocr(matricula_path, model_ocr)
        return matricula_string
    
    except Exception as e:
        return None
    
    finally:
        if os.path.exists(photo_path):
            os.remove(photo_path)
        if os.path.exists(matricula_path):
            os.remove(matricula_path)