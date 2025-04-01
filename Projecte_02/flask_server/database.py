from pymongo import MongoClient
from config import Config

class MongoDB:
    def __init__(self):
        """Inicializa la conexión con MongoDB usando la configuración de Config."""
        self.cliente = MongoClient(Config.MONGO_URI, serverSelectionTimeoutMS=5000)
        self.db = self.cliente[Config.DB_NAME]
        self.coleccion = self.db[Config.COLLECTION_NAME]

    def save_update(self, matricula, status):
        try:
            self.coleccion.update_one(
                {"_id": matricula},
                {"$set": {"status": status}},
                upsert=True
            )
        except Exception as e:
            print(f"Error al guardar o actualizar en MongoDB: {e}")


def guardar_mongodb(matricula, status):
    """Función que maneja la lógica de insertar datos en MongoDB."""
    try:
        mongo_db = MongoDB()  
        mongo_db.save_update(matricula, status)
    except Exception as e:
        print(f"Error: No se ha podido guardar en Mongo.\n{e}")