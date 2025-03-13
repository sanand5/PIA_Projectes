from flask import Flask, jsonify, request
import datetime
from model import cargar_modelo, predecir_precio
from database import guardar_mongodb
from config import Config

app = Flask(__name__)

scaler, encoder, model, X_data_columns, modas = cargar_modelo()

@app.route("/model_v1", methods=["POST"])
def enviar():
    try:
        datos = request.json 
        if not datos:
            return jsonify({"error": "No se recibieron datos"}), 400
        
        peticion = {
            "ano": datos.get("ano"),
            "almacenamiento": datos.get("almacenamiento"),
            "marca": datos.get("marca").lower(),
            "pantalla_in": datos.get("pantalla_in"), 
            "pantalla_tipo": datos.get("pantalla_tipo").lower(), 
            "velocidad_cpu_ghz": datos.get("velocidad_cpu_ghz"),
            "ram": datos.get("ram"), 
            "grosor": datos.get("grosor"), 
            "peso": datos.get("peso"),
            'ancho_px': datos.get("ancho_px"), 
            'alto_px': datos.get("alto_px"),     
            "bateria": datos.get("bateria"),  
            'promedio_valoraciones': datos.get("promedio_valoraciones"),
            'precio_anterior': datos.get("precio_anterior"),
        }
        
        preu_model = predecir_precio(peticion.copy(), scaler, encoder, model, X_data_columns, modas)
        timestamp = int(datetime.datetime.now().timestamp() * 1000)
        guardar_mongodb(peticion, preu_model, datos.get("opinion_cliente"))
        return jsonify({"precio_modelo": preu_model, "timestamp": timestamp})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    try:
        app.run(host="127.0.0.1", port=8085)
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
