from pymongo import MongoClient
from datetime import datetime
from config import Config, Status

class MongoDB:
    def __init__(self):
        self.client = MongoClient(Config.MONGO_URI, serverSelectionTimeoutMS=5000)
        self.db = self.client[Config.DB_NAME]
        self.collection = self.db[Config.COLLECTION_NAME]
        
        self.collection.create_index("_id")
        self.collection.create_index("status")
        self.collection.create_index("entradas")

    def save_vehicle_data(self, matricula, status, timestamp=None):
        if timestamp is None:
            timestamp = datetime.now()
            
        data = {
            "status": status,
        }
        
        try:
            if status == Status.DENTRO.value:
                data["entrada_timestamp"] = timestamp
                self.collection.update_one(
                    {"_id": matricula},
                    {"$set": data},
                    upsert=True
                )
                
            elif status == Status.SALIENDO.value:
                data["saliendo_timestamp"] = timestamp
                self.collection.update_one(
                    {"_id": matricula},
                    {"$set": data},
                    upsert=True
                )
                
            elif status == Status.FUERA.value:
                self.collection.update_one(
                    {"_id": matricula},
                    {
                        "$inc": {"entradas": 1},  # Incrementa el contador
                        "$unset": {
                            "entrada_timestamp": "",
                            "saliendo_timestamp": "",
                            "status": "",
                        },
                        "$set": {
                            "ultima_salida": timestamp  # Guardamos también la hora de salida
                        }
                    },
                    upsert=True
                )
                
        except Exception as e:
            print(f"Error al guardar datos en MongoDB: {e}")
            raise
    
    def buscar_matricula(self, matricula):
        try:
            if not isinstance(matricula, str) or not matricula.strip():
                raise ValueError("La matrícula debe ser un texto no vacío")
            
            matricula = matricula.strip().upper()
            datos = self.collection.find_one({"_id": matricula})
            
            if datos:
                datos['_id'] = str(datos['_id'])
                
                for campo, valor in datos.items():
                    if isinstance(valor, datetime):
                        datos[campo] = valor.isoformat()
                
                return datos
            return None

        except Exception as error:
            print(f"Error buscando matrícula: {error}")
            raise

    def close_connection(self):
        self.client.close()


def guardar_mongodb(matricula, status, timestamp=None):
    try:
        # Validaciones
        if status not in [s.value for s in Status]:
            raise ValueError(f"Estado no válido. Debe ser uno de: {[s.value for s in Status]}")
        
        if not isinstance(matricula, str):
            raise ValueError("La matrícula debe ser una cadena de texto.")
            
        matricula = matricula.strip().upper()  # Normalizamos a mayúsculas
        if not matricula:
            raise ValueError("La matrícula no puede estar vacía.")

        # Conexión y guardado
        mongo_db = MongoDB()
        mongo_db.save_vehicle_data(matricula, status, timestamp)
        
    except ValueError as ve:
        print(f"Error de validación: {ve}")
        raise
    except Exception as e:
        print(f"Error al guardar en MongoDB: {e}")
        raise
    finally:
        if 'mongo_db' in locals():
            mongo_db.close_connection()

def buscar_matricula_en_db(matricula):
    db = None
    try:
        db = MongoDB()
        return db.buscar_matricula(matricula)
    except Exception as error:
        print(f"Error en búsqueda: {error}")
        return None
    finally:
        if db:
            db.close_connection()