from flask import Flask, jsonify, request
import datetime
from model import cargar_modelo_yolo, cargar_modelo_ocr
from database import guardar_mongodb, buscar_matricula_en_db
from funtions import obtener_matricula

from typing import Dict, Any, Optional

app = Flask(__name__)

try:
    model_yolo = cargar_modelo_yolo()  
    model_ocr = cargar_modelo_ocr()

except Exception as e:
    raise RuntimeError("No se pudieron cargar los modelos") from e

def validar_peticion(datos: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Valida la estructura y contenido de la petición"""
    if not datos:
        raise ValueError("No se recibieron datos en la petición")
    
    if not isinstance(datos, dict):
        raise ValueError("Los datos deben ser un objeto JSON")
    
    photo = datos.get("photo")
    status = datos.get("status")
    
    if not photo:
        raise ValueError("El campo 'photo' es requerido")
    
    if status is None:
        raise ValueError("El campo 'status' es requerido")
    
    try:
        status = int(status)
    except (ValueError, TypeError):
        raise ValueError("El campo 'status' debe ser un número entero")
    
    if status not in [0, 1, 2]:
        raise ValueError("El campo 'status' debe ser 0 (DENTRO), 1 (SALIENDO) o 2 (FUERA)")
    
    return {
        "photo": photo,
        "status": status
    }

@app.route("/model_v2", methods=["POST"])
def parking():
    try:
        if not request.is_json:
            return jsonify({
                "error": "Content-Type debe ser application/json",
                "detalle": "El encabezado Content-Type debe estar configurado como application/json"
            }), 415
        
        datos = request.get_json()
        
        try:
            peticion = validar_peticion(datos)
        except ValueError as e:
            return jsonify({
                "error": "Datos de entrada inválidos",
                "detalle": str(e)
            }), 400
        
        try:
            matricula = obtener_matricula(peticion['photo'], model_yolo, model_ocr)
            if not matricula:
                return jsonify({
                    "error": "No se pudo reconocer la matrícula",
                    "detalle": "El modelo no pudo detectar una matrícula válida en la imagen proporcionada"
                }), 400
        except Exception as e:
            return jsonify({
                "error": "Error procesando la imagen",
                "detalle": "Ocurrió un error interno al procesar la imagen de matrícula"
            }), 500
        
        timestamp = int(datetime.datetime.now().timestamp() * 1000)

        try:
            guardar_mongodb(matricula, peticion["status"], timestamp)
        except Exception as e:
            return jsonify({
                "error": "Error al guardar los datos",
                "detalle": "Ocurrió un error al registrar la información en la base de datos"
            }), 500
        
        return jsonify({
            "matricula": matricula,
            "timestamp": timestamp,
        }), 200
    
    except Exception as e:
        return jsonify({
            "error": "Error interno del servidor",
            "detalle": "Ocurrió un error inesperado al procesar la solicitud"
        }), 500

@app.route("/matricula", methods=["GET"])
def get_matricula_info():
    matricula = request.args.get("matricula")
    
    if not matricula:
        return jsonify({
            "error": "El parámetro 'matricula' es requerido"
        }), 400
    
    try:
        info = buscar_matricula_en_db(matricula)
        if not info:
            return jsonify({
                "error": "No se encontró información para la matrícula proporcionada"
            }), 404
        
        return jsonify(info), 200
    
    except Exception as e:
        return jsonify({
            "error": "Error al obtener información de la matrícula",
            "detalle": str(e)
        }), 500

if __name__ == "__main__":
    try:
        app.run(host="127.0.0.1", port=8085, debug=False)
    except Exception as e:
        print(f"Error al iniciar el servidor: {str(e)}")