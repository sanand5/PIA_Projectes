from flask import Flask, jsonify, request
import datetime
from model import cargar_modelo_yolo, predecir_ocr, cargar_modelo_ocr
from database import guardar_mongodb
from img_gestor import obtener_matricula, base64_to_cv2

app = Flask(__name__)

model_yolo = cargar_modelo_yolo()  
model_ocr = cargar_modelo_ocr()

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
        photo = base64_to_cv2(peticion['photo'])
        print("Recibida la imagen", photo)
        matricula_img = obtener_matricula(photo, model_yolo)
        print("Matrícula detectada")
        matricula_string = predecir_ocr(matricula_img, model_ocr)
        print("Matrícula reconocida")
        timestamp = int(datetime.datetime.now().timestamp() * 1000)
        # guardar_mongodb(matricula, peticion["status"], timestamp)
        return jsonify({"matricula": matricula_string, "timestamp": timestamp}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
if __name__ == "__main__":
    try:
        app.run(host="127.0.0.1", port=8085)
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
