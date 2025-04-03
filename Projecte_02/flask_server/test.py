import requests
import base64
import json
from datetime import datetime
import time
import os
from config import Config

# Configuración
API_URL = "http://127.0.0.1:8085/model_v2"
IMAGE_PATH = os.path.join(Config.BASE_PATH, "matricula_test.jpg")

STATUS = 2  # 0: DENTRO, 1: SALIENDO, 2: FUERA

def encode_image_to_base64(image_path):
    """Codifica una imagen a base64"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def make_request(image_base64=None, status=0):
    """Hace una petición a la API"""
    payload = {
        "photo": image_base64,
        "status": status
    }
    
    try:
        start_time = time.time()
        response = requests.post(API_URL, json=payload)
        elapsed_time = time.time() - start_time
        
        if response.status_code == 200:
            print("\n✅ Petición exitosa:")
            print(f"Matrícula detectada: {response.json()['matricula']}")
            print(f"Timestamp: {response.json()['timestamp']}")
            print(f"Tiempo de respuesta: {elapsed_time:.2f} segundos")
        else:
            print("\n❌ Error en la petición:")
            print(f"Código de estado: {response.status_code}")
            print(f"Error: {response.json().get('error', 'Sin mensaje de error')}")
            
        return response.json()
    
    except requests.exceptions.RequestException as e:
        print(f"\n🔥 Error de conexión: {str(e)}")
        return None

if __name__ == "__main__":
    print("=== Prueba de la API de reconocimiento de matrículas ===")
    
    # Ejemplo 1: Petición con imagen real
    try:
        image_base64 = encode_image_to_base64(IMAGE_PATH)
        print(f"\n📤 Enviando imagen: {IMAGE_PATH} con estado: {STATUS}")
        result = make_request(image_base64, STATUS)
    except FileNotFoundError:
        print(f"\n⚠️ No se encontró la imagen {IMAGE_PATH}, usando ejemplo con imagen dummy")
        
        # Ejemplo 2: Petición con imagen dummy (si no hay imagen real)
        dummy_image = {
            "photo": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z/C/HgAGgwJ/lK3Q6wAAAABJRU5ErkJggg==",
            "status": STATUS
        }
        print("\n📤 Enviando imagen dummy (rectángulo rojo 1x1)")
        result = make_request(**dummy_image)
    
    # Ejemplo 3: Petición con estado inválido (para probar errores)
    print("\n🧪 Probando con estado inválido (99)")
    make_request(image_base64, 99)
    
    # Ejemplo 4: Petición sin imagen (para probar validación)
    print("\n🧪 Probando petición sin imagen")
    make_request(status=0)