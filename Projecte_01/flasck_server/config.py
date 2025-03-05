import os

class Config:
    # Configuración del modelo
    MODEL_PATH = os.path.join(os.path.dirname(__file__), "model")
    
    # Configuración de MongoDB
    MONGO_URI = "mongodb://localhost:27020/"
    DB_NAME = "PIA"
    COLLECTION_NAME = "peticions"
