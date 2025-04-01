from flask import Flask, jsonify, request
import datetime
from model import cargar_modelo, predecir_precio
from database import guardar_mongodb
from config import Config

app = Flask(__name__)

scaler, encoder, model, X_data_columns, modas = cargar_modelo()

@app.route("/model_v2", methods=["POST"])
def enviar():
    try:
        datos = request.json 
        if not datos:
            return jsonify({"error": "No se recibieron datos"}), 400
        
        peticion = {
            "photo": datos.get("photo"),
            "matricula": datos.get("matricula"),
            "status": datos.get("status")
        }

        img = convertir_img(peticion['photo'])
        # recuadro = predecir_yolo(peticion["photo"])
        # matricula = ocr_get_mattr(recuadro)
        # timestamp = int(datetime.datetime.now().timestamp() * 1000)

        
        # guardar_mongodb(matricula, peticion["status"], timestamp)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def convertir_img(img):
    return img

if __name__ == "__main__":
    try:
        app.run(host="127.0.0.1", port=8085)
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
