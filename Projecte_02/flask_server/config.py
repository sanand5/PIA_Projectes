import os
from enum import Enum

class Config:
    # Configuración del modelo
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))
    MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "model_27_03_2025_19_30.pt")
    # Configuración de MongoDB
    MONGO_URI = "mongodb://localhost:27022/"
    DB_NAME = "PIA"
    COLLECTION_NAME = "matriculas"


class Status(Enum):
    DENTRO = 0
    SALIENDO = 1
    FUERA = 2