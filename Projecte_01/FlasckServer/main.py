import pandas as pd
import joblib, os
import datetime

from flask import Flask, jsonify, request
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from pymongo import MongoClient

modelo_path = os.path.join(os.path.dirname(__file__),"./model")

scaler = joblib.load(os.path.join(modelo_path,"scaler.joblib"))
encoder = joblib.load(os.path.join(modelo_path,"encoder_ohe.joblib"))
model = joblib.load(os.path.join(modelo_path,"model.joblib"))
X_train = pd.read_csv(os.path.join(modelo_path,"X_train.csv"))
X_train.drop(['_id'], inplace = True, axis = 1)
cliente = MongoClient("mongodb://localhost:27020/")
db = cliente["PIA"]
coleccion = db["peticions"]

app=Flask(__name__)

def prediure_preu(peticion):
    peticion['precio_actual'] = 0
    peticion_df = pd.DataFrame([peticion])
    peticion_scaled = scaler.transform(peticion_df.select_dtypes(include=['number']))
    peticion_encoder = encoder.transform(peticion_df.select_dtypes(include=['object']))

    peticion_df_scaled = pd.DataFrame(peticion_scaled, columns=peticion_df.select_dtypes(include=['number']).columns)
    peticion_df_encoded = pd.DataFrame(peticion_encoder, columns=encoder.get_feature_names_out())

    peticion_final = pd.concat([peticion_df_scaled, peticion_df_encoded], axis=1)
    peticion_final.drop(['precio_actual'], inplace = True, axis = 1)
    peticion_final = peticion_final[X_train.columns]

    prediccio = model.predict(peticion_final)

    peticion_scaled_pred = peticion_scaled.copy()
    indice_precio_actual = peticion_df_scaled.columns.get_loc('precio_actual')

    peticion_scaled_pred[:, indice_precio_actual] = prediccio 
    prediccion_escalada_inversa = scaler.inverse_transform(peticion_scaled_pred)

    prediccion_final = prediccion_escalada_inversa[0, indice_precio_actual] 

    return prediccion_final

def guardar_mongodb(peticion, preu_model, opinion_cliente):
    peticion['precio_modelo'] = preu_model
    if opinion_cliente:
        peticion['opinion_client'] = opinion_cliente

    coleccion.insert_one(peticion)

@app.route("/model_v1", methods=["POST"])
def enviar():
    datos = request.json 
    if not datos:
        return jsonify({"error": "No se recibieron datos"}), 400

    peticion = {
        "ano": datos.get("ano"),
        "almacenamiento": datos.get("almacenamiento"),
        "marca": datos.get("marca"),
        "pantalla_in": datos.get("pantalla_in"), 
        "pantalla_tipo": datos.get("pantalla_tipo"), 
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
    preu_model = prediure_preu(peticion.copy())
    timestamp = int(datetime.datetime.now().timestamp() * 1000)
    guardar_mongodb(peticion, preu_model, datos.get("opinion_cliente"))
    return jsonify({"precio_modelo": preu_model, "timestamp": timestamp})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8085, debug=True)
    # app.run(host="127.0.0.1", port=8085)
# Gestiuonar Errores