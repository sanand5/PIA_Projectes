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

def cargar_modelo():
    try:
        # Configuración
        model_path = "./models/model_27_03_2025_19_30.pt"
        model_matr = YOLO(model_path)
        return model_matr
    except FileNotFoundError as e:
        raise Exception(f"Error al cargar el modelo: {e}")

def predecir_recuadro(photo, model):
    img = cv2.imread(photo)    
    results = model.predict(img)

    return results
