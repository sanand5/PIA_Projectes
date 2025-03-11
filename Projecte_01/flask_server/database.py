# database.py
from pymongo import MongoClient
from config import Config

class MongoDB:
    def __init__(self):
        """Inicializa la conexión con MongoDB usando la configuración de Config."""
        self.cliente = MongoClient(Config.MONGO_URI, serverSelectionTimeoutMS=5000)
        self.db = self.cliente[Config.DB_NAME]
        self.coleccion = self.db[Config.COLLECTION_NAME]

    def guardar(self, peticion):
        """Guarda el documento en la colección de MongoDB."""
        try:
            self.coleccion.insert_one(peticion)
        except Exception as e:
            print(f"Error al guardar en MongoDB: {e}")

def guardar_mongodb(peticion, preu_model, opinion_cliente):
    """Función que maneja la lógica de insertar datos en MongoDB."""
    try:
        mongo_db = MongoDB()  
        peticion['precio_modelo'] = preu_model
        if opinion_cliente:
            peticion['opinion_client'] = opinion_cliente
        mongo_db.guardar(peticion)
    except Exception as e:
        print(f"Error: No se ha podido guardar en Mongo.\n{e}")