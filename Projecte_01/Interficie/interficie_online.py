import flet as ft
import pandas as pd
import requests
from funciones import prediccion

def sacar_promedio(num_estrellas, num_valoraciones):
    return num_valoraciones / num_estrellas if num_estrellas != 0 else 0

def main(page: ft.Page):
    
    page.title = "ANÁLISIS DE OFERTAS MÓVILES"
    page.bgcolor = ft.colors.BLUE_50
    page.scroll = "auto"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window_width = 800
    page.window_height = 1000

    def textfield(label, value):
        return ft.TextField(width=220, label=label, value=value, border_color=ft.colors.BLACK,label_style=ft.TextStyle(color=ft.colors.BLACK), text_style=ft.TextStyle(color=ft.colors.BLACK))

    precio = textfield("Precio (€)", "300")
    precio_anterior = textfield("Precio anterior (€)", "350")
    
    image = ft.Image(src="/home/aluvesprada/Escritorio/VISUAL_STUDIO/PIA/PROJECTE/5.Interfaz/mobile_icon.png", width=150, height=150)
    title = ft.Text("ANÁLISIS DE OFERTAS MÓVILES", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE)
    subtitle = ft.Text("Ingrese su oferta en dispositivos móviles y le calcularemos lo buena que es:", size=16, italic=True, color=ft.colors.BLUE_900)
    
    title_row = ft.Column([image, title], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    
    fecha = textfield("Año de salida", "2023")
    marca = textfield("Marca", "samsung")
    pantalla_in = textfield("Tamaño de pantalla (pulgadas)", "6.5")
    pantalla_tipo = textfield("Tipo de pantalla", "amoled")
    grosor = textfield("Profundidad (cm)", "0.8")
    peso = textfield("Peso (g)", "180")
    velocidad_gpu = textfield("Velocidad de CPU (GHz)", "2.84")
    ancho_px = textfield("Ancho (px)", "1080")
    alto_px = textfield("Alto (px)", "2400")
    memoria = textfield("Número de Memoria","8GB")
    almacenamiento = textfield("Almacenamiento","128GB")
    bateria = textfield("Batería","5000 MaH")
    numero_valoraciones = textfield("Número de valoraciones", "1500")
    numero_estrellas = textfield("Número de estrellas", "4")

    resultado = ft.Text(color=ft.colors.BLACK)
    
    def calcular_oferta(e):
        try:
            promedio_valoraciones = sacar_promedio(int(numero_estrellas.value), int(numero_valoraciones.value))
        except ValueError:
            resultado.value = "Por favor, ingrese números válidos para las valoraciones y estrellas."
            resultado.color = ft.colors.RED
            page.update()
            return

        try:
            precio_oferta = float(precio.value)
            precio_anterior_val = float(precio_anterior.value)
        except ValueError:
            resultado.value = "Por favor, ingrese un precio válido (número)."
            resultado.color = ft.colors.RED
            page.update()
            return

        try:
            memoria_int = int(memoria.value.replace("GB", ""))
            almacenamiento_int = int(almacenamiento.value.replace("GB", "").replace("TB", "000"))
            bateria_int = int(bateria.value.replace(" MaH", ""))
            pantalla_in_float = float(pantalla_in.value)
            grosor_float = float(grosor.value)
            peso_float = float(peso.value)
            velocidad_gpu_float = float(velocidad_gpu.value)
            ancho_px_float = float(ancho_px.value)
            alto_px_float = float(alto_px.value)
            fecha_int = int(fecha.value)
        except ValueError:
            resultado.value = "Por favor, ingrese números válidos para los campos numéricos."
            resultado.color = ft.colors.RED
            page.update()
            return
        
        datos_movil = {
                    "ano":fecha_int,
                    "almacenamiento": almacenamiento_int,
                    "marca": marca.value,
                    "pantalla_in": pantalla_in_float, 
                    "pantalla_tipo": pantalla_tipo.value, 
                    "velocidad_cpu_ghz": velocidad_gpu_float,
                    "ram": memoria_int, 
                    "grosor": grosor_float, 
                    "peso": peso_float,
                    "ancho_px": ancho_px_float, 
                    "alto_px": alto_px_float,     
                    "bateria": bateria_int,  
                    "promedio_valoraciones": promedio_valoraciones, 
                    "precio_anterior": precio_anterior_val,
                    "precio_actual": 0,
                }

        try:
            #---------- LOCAL------------------------#
            df_movil = pd.DataFrame([datos_movil])
            precio_prediccion = prediccion(df_movil)

            #---------- SERVIDOR---------------------#
            response = requests.post("http://127.0.0.1:8081/model_v1", json=datos_movil)
            response_data = response.json()
            precio_prediccion = response_data.get("precio_modelo")

                        # Define el porcentaje máximo que se considera aceptable
            porcentaje_maximo = 10  # Puedes cambiar este valor para ajustar el umbral

            if precio_oferta < precio_prediccion:
                resultado.value = "Es una buena oferta"
                resultado.color = ft.colors.GREEN
                page.update()
            elif precio_oferta >= precio_prediccion and precio_oferta <= precio_prediccion * (1 + porcentaje_maximo / 100):
                resultado.value = "Es una oferta aceptable"
                resultado.color = ft.colors.YELLOW  # Puedes cambiar el color si prefieres otro
                page.update()

            else:
                resultado.value = "No es una buena oferta"
                resultado.color = ft.colors.RED
                page.update()

        except Exception as ex:
            resultado.value = f"Error en la predicción: {ex}"
            print(f"Error en la predicción: {ex}")
            resultado.color = ft.colors.RED

        page.update()
    
    def validar_campos():
        campos = [
            precio, precio_anterior, fecha, marca, pantalla_in, pantalla_tipo, 
            grosor, peso, velocidad_gpu, ancho_px, alto_px, memoria, almacenamiento, 
            bateria, numero_valoraciones, numero_estrellas
        ]
        
        # Comprobar si algún campo está vacío
        for campo in campos:
            if not campo.value.strip():
                boton.bgcolor = ft.colors.GREY  # Desactivar el botón (gris)
                boton.disabled = True
                page.update()
                return
        
        # Si todos los campos están completos
        boton.bgcolor = ft.colors.BLUE  # Activar el botón
        boton.disabled = False
        page.update()

    # Se ejecuta cada vez que se actualiza algún campo
    for campo in [precio, precio_anterior, fecha, marca, pantalla_in, pantalla_tipo, 
                grosor, peso, velocidad_gpu, ancho_px, alto_px, memoria, almacenamiento, 
                bateria, numero_valoraciones, numero_estrellas]:
        campo.on_change = lambda e: validar_campos()

    boton = ft.ElevatedButton("Calcular oferta", on_click=calcular_oferta, bgcolor=ft.colors.GREY, color=ft.colors.WHITE, width=220, disabled=True)
    autores = ft.Text("\n\nHecho por: Andreu Sanz y Gerard Grau", size=14, italic=True, color=ft.colors.BLUE)
    
    fondo = ft.Container(
        expand=True, width=800, height=1000,
        gradient=ft.LinearGradient(begin=ft.alignment.top_center, end=ft.alignment.bottom_center, colors=[ft.colors.BLUE_100, ft.colors.WHITE]),
        content=ft.Column([
            title_row, subtitle,
            ft.Row([precio, precio_anterior], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([marca, fecha, pantalla_in], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([memoria, almacenamiento, bateria], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([grosor, peso, velocidad_gpu], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([ancho_px, alto_px, pantalla_tipo], alignment=ft.MainAxisAlignment.CENTER),
            boton, resultado, autores
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )
    
    page.add(fondo)

ft.app(target=main)
