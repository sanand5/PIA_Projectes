import requests

# URL de la API o servidor donde se enviará la petición
url = "http://localhost:8085/model_v1"

# Datos de prueba
datos_prueba = {
    "ano": 2023,
    "almacenamiento": 128,
    "marca": "samsung",
    "pantalla_in": 6.5,
    "pantalla_tipo": "lcd",
    "velocidad_cpu_ghz": 2.84,
    "ram": 8,
    "grosor": 7.9,
    "peso": 1,
    "ancho_px": 1080,
    "alto_px": 2400,
    "bateria": 5000,
    "promedio_valoraciones": 4.5,
    "precio_anterior": 799.99,
}

# Realizar la petición POST
respuesta = requests.post(url, json=datos_prueba)

# Mostrar la respuesta del servidor
print("Código de estado:", respuesta.status_code)
print("Respuesta:", respuesta.json())