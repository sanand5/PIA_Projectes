import requests
import base64
import json
import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

def existe_matricula(uri: str, nombre_db: str, nombre_coleccion: str, texto_matricula: str) -> bool:
    try:
        client = MongoClient(uri)
        client.admin.command('ping')
        
        # Obtener la colección
        db = client[nombre_db]
        coleccion = db[nombre_coleccion]
        
        # Buscar el texto en el campo matricula
        resultado = coleccion.find_one({"matricula": texto_matricula})
        return resultado is not None
        
    except ConnectionFailure:
        print("Error: No se pudo conectar a MongoDB")
        return False
    except Exception as e:
        print(f"Error inesperado: {e}")
        return False
    
    finally:
        if 'client' in locals():
            client.close()



def image_to_base64(image_path):
    """Convierte una imagen a base64"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def test_api(image_path, api_url="http://127.0.0.1:8085/model_v2"):
    """
    Prueba la API de reconocimiento de matrículas
    
    Args:
        image_path (str): Ruta a la imagen a enviar
        api_url (str): URL del endpoint de la API
    """
    try:
        # Convertir imagen a base64
        image_base64 = image_to_base64(image_path)
        
        # Preparar los datos de la petición
        payload = {
            "photo": image_base64,
            "matricula": "",  # Este campo parece opcional según tu API
            "status": "test"  # Valor de ejemplo para status
        }
        
        # Encabezados de la petición
        headers = {
            "Content-Type": "application/json"
        }
        
        print(f"Enviando imagen {os.path.basename(image_path)} a la API...")
        
        # Enviar la petición POST
        response = requests.post(api_url, data=json.dumps(payload), headers=headers)
        
        # Procesar la respuesta
        if response.status_code == 200:
            result = response.json()
            print("¡Prueba exitosa!")
            print(f"Matrícula detectada: {result.get('matricula')}")
            print(f"Timestamp: {result.get('timestamp')}")
        else:
            print(f"Error en la petición. Código de estado: {response.status_code}")
            print(f"Respuesta: {response.text}")
            
    except Exception as e:
        print(f"Ocurrió un error durante la prueba: {str(e)}")

if __name__ == "__main__":
    # Ejemplo de uso
    image_path = "./1668448029089_jpg.rf.779ea16b2d2e47a624e8ebfa0d3e96a9.jpg"  # Cambia esto por la ruta de tu imagen
    test_api(image_path)