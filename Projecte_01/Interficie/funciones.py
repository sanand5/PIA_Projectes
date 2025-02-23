
def prediccion (movil, modelo):
    prediccion = modelo.predict(movil)
    return prediccion

def obtener_valor_numerico(texto, archivo="C:/Users/Gerard/Desktop/VISUAL_STUDIO/PIA/PROYECTO/limpieza/diccionario.txt"):
    """Busca un valor en el diccionario y devuelve su número asignado."""
    try:
        with open(archivo, "r") as file:
            for linea in file:
                clave, valor = linea.strip().split(":")
                if clave == texto:
                    return int(valor)
    except FileNotFoundError:
        print("El archivo de diccionario no existe.")
    return -1  
