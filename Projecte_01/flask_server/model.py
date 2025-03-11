import joblib
import pandas as pd
import os
from config import Config

def cargar_modelo():
    try:
        scaler = joblib.load(os.path.join(Config.MODEL_PATH, "scaler.joblib"))
        encoder = joblib.load(os.path.join(Config.MODEL_PATH, "encoder_ohe.joblib"))
        model = joblib.load(os.path.join(Config.MODEL_PATH, "model.joblib"))
        X_train = pd.read_csv(os.path.join(Config.MODEL_PATH, "X_train.csv"))
        X_test = pd.read_csv(os.path.join(Config.MODEL_PATH, "X_test.csv"))
        X_train.drop(['_id'], inplace=True, axis=1)
        X_test.drop(['_id'], inplace=True, axis=1)
        X_data = pd.concat([X_train, X_test], axis=0, ignore_index=True)
        modas = {}
        for col_name in encoder.feature_names_in_:
            modas[col_name] = calcular_mode(col_name, X_data)
        return scaler, encoder, model, X_data.columns, modas
    except FileNotFoundError as e:
        raise Exception(f"Error al cargar los archivos del modelo: {e}")

def calcular_mode(columna, df):
    columns = [c for c in df.columns if c.startswith(columna)]
    mode = {col: df[col].sum() for col in columns}
    col_mas_alta = max(mode, key=mode.get)
    mode_value = col_mas_alta.replace(f'{columna}_', '')
    return mode_value

def predecir_precio(peticion, scaler, encoder, model, X_data_columns, modas):
    try:
        categorias_por_columna = {col: encoder.categories_[i] for i, col in enumerate(encoder.feature_names_in_)}
        for col in encoder.feature_names_in_:
            if peticion[col] not in categorias_por_columna[col]:
                peticion[col] = modas[col]

        peticion['precio_actual'] = 0
        peticion_df = pd.DataFrame([peticion])
        
        # Escalar y codificar
        peticion_scaled = scaler.transform(peticion_df.select_dtypes(include=['number']))
        peticion_encoded = encoder.transform(peticion_df.select_dtypes(include=['object']))
        
        peticion_df_scaled = pd.DataFrame(peticion_scaled, columns=peticion_df.select_dtypes(include=['number']).columns)
        peticion_df_encoded = pd.DataFrame(peticion_encoded, columns=encoder.get_feature_names_out())
        
        peticion_final = pd.concat([peticion_df_scaled, peticion_df_encoded], axis=1)
        peticion_final = peticion_final[X_data_columns]

        # Predicción
        prediccion = model.predict(peticion_final)
        
        # Inversión de la escala
        peticion_scaled_pred = peticion_scaled.copy()
        indice_precio_actual = peticion_df_scaled.columns.get_loc('precio_actual')
        peticion_scaled_pred[:, indice_precio_actual] = prediccion 
        prediccion_escalada_inversa = scaler.inverse_transform(peticion_scaled_pred)
        
        return prediccion_escalada_inversa[0, indice_precio_actual]
    except Exception as e:
        raise Exception(f"Error durante la predicción: {e}")
