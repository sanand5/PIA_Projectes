from flask import Flask, jsonify, request
import pandas as pd
import joblib, os
from sklearn.preprocessing import LabelEncoder, StandardScaler, OneHotEncoder
import datetime

modelo_path = os.path.join(os.path.dirname(__file__),"./model")

scaler = joblib.load(os.path.join(modelo_path,"scaler.joblib"))
encoder = joblib.load(os.path.join(modelo_path,"encoder_ohe.joblib"))
model = joblib.load(os.path.join(modelo_path,"model.joblib"))

app=Flask(__name__)

def prediure_preu(peticion):
    peticion_df = pd.DataFrame([peticion])
    peticion_scaled = scaler.transform(peticion_df.select_dtypes(include=['number']))
    peticion_encoder = encoder.transform(peticion_df.select_dtypes(include=['object']))

    peticion_df_scaled = pd.DataFrame(peticion_scaled, columns=peticion_df.select_dtypes(include=['number']).columns)
    peticion_df_encoded = pd.DataFrame(peticion_encoder, columns=encoder.get_feature_names_out())

    peticion_final = pd.concat([peticion_df_scaled, peticion_df_encoded], axis=1)
    peticion_final.drop(['precio_actual'], inplace = True, axis = 1)

    X_train = pd.read_csv(os.path.join(modelo_path,"X_train.csv"))
    X_train.drop(['_id'], inplace = True, axis = 1)
    peticion_final = peticion_final[X_train.columns]

    prediccio = model.predict(peticion_final)

    peticion_scaled_with_pred = peticion_scaled.copy()
    peticion_scaled_with_pred[:, peticion_df_scaled.columns.get_loc('precio_actual')] = prediccio
    prediccion_escalada_inversa = scaler.inverse_transform(peticion_scaled_with_pred)

    prediccion_final = prediccion_escalada_inversa[0, peticion_df_scaled.columns.get_loc('precio_actual')]

    return prediccion_final

def indicar_nivel_oferta(p_cliente, p_modelo):
    # Ver segun el precio del cliente i del modelo si es una buena o mala oferta, despues devlover un numero de nivel de oferta por ejemplo
    # 1 = Buena oferta
    # 2 = Precio asecible
    # 3 = Mala oferta
    return 1

@app.route("/model_v1", methods=["POST"])
def enviar():
    datos = request.json 
    if not datos:
        return jsonify({"error": "No se recibieron datos"}), 400

    peticion = {
        "ano":datos.get("ano"),
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
        'precio_actual': datos.get("precio_actual")
    }
    preu_model = prediure_preu(peticion)
    oferta = indicar_nivel_oferta(peticion.get("precio_actual"), preu_model)
    timestamp = int(datetime.datetime.now().timestamp() * 1000)
    return jsonify({"Nivel_oferta": oferta, "timestamp": timestamp})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
    # app.run(host="127.0.0.1", port=8080)
# Necesite una funció per a poder recibir les dades de el client i de lo que me retorne el model guardar-ho en una base de datos 