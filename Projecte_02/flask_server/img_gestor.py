import os
import cv2
from model import predecir_yolo
import io
import base64
from PIL import Image
import numpy as np

def obtener_bbox(result, max_len=1):
    boxes_with_confs = [(box.xyxy, box.conf.item()) for box in result.boxes]
    boxes_sorted = sorted(boxes_with_confs, key=lambda x: x[1], reverse=True)
    recuadros = [box[0] for box in boxes_sorted[:max_len]]
    return recuadros

def recortar_y_guardar_matricula(bboxes, photo):
    img = cv2.imread(photo)
    if img is None:
        raise ValueError(f"No se pudo leer la imagen: {photo}")
    
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

def obtener_matricula(photo, model, max_len=1):
    result = predecir_yolo(photo, model)
    bboxes = obtener_bbox(result, max_len)
    recortes = recortar_y_guardar_matricula(bboxes, photo)
    return recortes

def base64_to_cv2(base64_string):
    image_bytes = base64.b64decode(base64_string)
    np_array = np.frombuffer(image_bytes, dtype=np.uint8)
    return cv2.imdecode(np_array, cv2.IMREAD_COLOR)

def cv2_to_base64(cv2_image, format=".jpg"):
    success, encoded_image = cv2.imencode(format, cv2_image)
    if not success:
        raise ValueError("No se pudo codificar la imagen")
    return base64.b64encode(encoded_image).decode('utf-8')