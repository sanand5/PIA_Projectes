import joblib
import pandas as pd
import os
from config import Config
from roboflow import Roboflow
import os
from ultralytics import YOLO
import cv2
import numpy as np
from pathlib import Path

def cargar_modelo_yolo():
    try:
        # Configuración
        model_path = "./models/model_27_03_2025_19_30.pt"
        model_matr = YOLO(model_path)
        return model_matr
    except FileNotFoundError as e:
        raise Exception(f"Error al cargar el modelo: {e}")

def predecir_yolo(photo, model):
    results = model.predict(
        source=photo,
        conf=0.25,
        save=False,
        verbose=False
    )
    return results[0]

def obtener_bbox(result):
    recuadros = []
    for box in result.boxes:
        recuadros.append(box.xyxy)
    return recuadros