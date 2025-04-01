import os

class Config:
    # Configuración del modelo
    MODEL_PATH = os.path.join(os.path.dirname(__file__), "models")
    
    # Configuración de MongoDB
    MONGO_URI = "mongodb://localhost:27022/"
    DB_NAME = "PIA"
    COLLECTION_NAME = "matriculas"
