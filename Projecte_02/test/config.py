import os

class Config:
    # Configuración del modelo
    MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "model_27_03_2025_19_30.pt")
    
    # Configuración de MongoDB
    MONGO_URI = "mongodb://localhost:27022/"
    DB_NAME = "PIA"
    COLLECTION_NAME = "matriculas"
