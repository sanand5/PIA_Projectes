import flet as ft
import pandas as pd
import requests

# FUNCIONES
def sacar_promedio(num_estrellas, num_valoraciones):
    return num_valoraciones / num_estrellas if num_estrellas != 0 else 0

def textfield(label, value):
    return ft.TextField(width=220, label=label, value=value, border_color=ft.colors.BLACK,label_style=ft.TextStyle(color=ft.colors.BLACK), text_style=ft.TextStyle(color=ft.colors.BLACK))

def checkbox(label):
    return ft.Checkbox(label=label, label_style=ft.TextStyle(color=ft.colors.BLACK))

# MAIN
def main(page: ft.Page):
    
    # Parametros
    page.title = "ANÁLISIS DE OFERTAS MÓVILES"
    page.bgcolor = ft.colors.BLUE_50
    page.scroll = "auto"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window_width = 800
    page.window_height = 1000

    # Campos
    precio = textfield("Precio (€)", "100")
    precio_anterior = textfield("Precio anterior (€)", "300")
    image = ft.Image(src="../res/mobile_icon.png", width=150, height=150)
    title = ft.Text("COMPARE MOBILE",size=50,  weight=ft.FontWeight.W_900, color=ft.colors.BLUE)
    subtitle = ft.Text("Ingrese su oferta en dispositivos móviles y le calcularemos lo buena que es:",weight=ft.FontWeight.W_900, size=16, italic=True, color=ft.colors.BLUE_900)
    fecha = textfield("Año de salida", "2013")
    marca = textfield("Marca", "Samsung")
    pantalla_in = textfield("Tamaño de pantalla (pulgadas)", "4.3")
    pantalla_tipo = textfield("Tipo de pantalla", "lcd")
    grosor = textfield("Profundidad (cm)", "1.27")
    peso = textfield("Peso (g)", "77")
    velocidad_gpu = textfield("Velocidad de CPU (GHz)", "1.7")
    ancho_px = textfield("Ancho (px)", "540")
    alto_px = textfield("Alto (px)", "960")
    memoria = textfield("Número de Memoria","2")
    almacenamiento = textfield("Almacenamiento ","256")
    bateria = textfield("Batería (MaH)","5000")
    numero_valoraciones = textfield("Número de valoraciones", "5000")
    numero_estrellas = textfield("Número de estrellas", "5")
    texto_opinion= ft.Text("Te parece una buena oferta?",color=ft.Colors.BLACK)
    checkbox_si = checkbox("Si")
    checkbox_no = checkbox("No")
    resultado = ft.Text(color=ft.colors.BLACK)
    autores = ft.Text("\n\nHecho por: Andreu Sanz y Gerard Grau", size=14, italic=True, color=ft.colors.BLUE)
    campos = [
            precio, precio_anterior, fecha, marca, pantalla_in, pantalla_tipo, 
            grosor, peso, velocidad_gpu, ancho_px, alto_px, memoria, almacenamiento, 
            bateria, numero_valoraciones, numero_estrellas
        ]
    
    # Funciones internas
    def on_checkbox_change(e):

        if checkbox_si.value:
            checkbox_no.value = False

        elif checkbox_no.value:
            checkbox_si.value = False

        elif not checkbox_si.value and not checkbox_no.value:
            checkbox_si.value = False
            checkbox_no.value = False
        page.update()

    checkbox_si.on_change = on_checkbox_change
    checkbox_no.on_change = on_checkbox_change
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
                    "marca": marca.value.lower(),
                    "pantalla_in": pantalla_in_float, 
                    "pantalla_tipo": pantalla_tipo.value.lower(), 
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
            response = requests.post("http://127.0.0.1:8085/model_v1", json=datos_movil)
            response_data = response.json()
            precio_prediccion = response_data.get("precio_modelo")
            
            rangos_descuento = [
                (100, 300, 15),   # Para móviles entre 100 y 300€, se considera buena oferta con un 15% de descuento
                (301, 700, 12),   # Para móviles entre 301 y 700€, se considera buena oferta con un 12% de descuento
                (701, 1200, 10),  # Para móviles entre 701 y 1200€, se considera buena oferta con un 10% de descuento
                (1201, 2000, 8)   # Para móviles entre 1201 y 2000€, se considera buena oferta con un 8% de descuento
            ]
            
            porcentaje_maximo = 10  
            for rango in rangos_descuento:
                if rango[0] <= precio_prediccion <= rango[1]:
                    porcentaje_maximo = rango[2]
                    break
                    
            precio_limite_buena = precio_prediccion * (1 - porcentaje_maximo / 100)
            precio_limite_aceptable = precio_prediccion * (1 + porcentaje_maximo / 100)
            
            if precio_oferta <= precio_limite_buena:
                resultado.value = "Es una buena oferta"
                resultado.color = ft.colors.GREEN
            elif precio_limite_buena < precio_oferta <= precio_limite_aceptable:
                resultado.value = "Es una oferta aceptable"
                resultado.color = ft.colors.ORANGE  
            else:
                resultado.value = "No es una buena oferta"
                resultado.color = ft.colors.RED
            page.update()   

        except Exception as ex:
            resultado.value = f"Error en la predicción: {ex}"
            print(f"Error en la predicción: {ex}")
            resultado.color = ft.colors.RED

        page.update()
    boton = ft.ElevatedButton("Calcular oferta", on_click=calcular_oferta, bgcolor=ft.colors.GREY, color=ft.colors.WHITE,height=50, width=300, disabled=False)

    def validar_campos():

        
        for campo in campos:
            page.update()
            if not campo.value.strip():
                boton.bgcolor = ft.colors.GREY #Deshabilitar boton  
                boton.disabled = True
                page.update()
                return
        
        boton.bgcolor = ft.colors.BLUE  #Habilitar boton
        boton.disabled = False
        page.update()

    for campo in [precio, precio_anterior, fecha, marca, pantalla_in, pantalla_tipo, 
                grosor, peso, velocidad_gpu, ancho_px, alto_px, memoria, almacenamiento, 
                bateria, numero_valoraciones, numero_estrellas]:
        campo.on_change = lambda e: validar_campos()

    title_row = ft.Column(
        [image, title],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10 
    )
    # Contenido
    fondo = ft.Container(
        expand=True,
        content=ft.Column([
                title_row, 
                subtitle,
                ft.Container(
                    content=ft.Row([precio, precio_anterior], alignment=ft.MainAxisAlignment.CENTER),
                    padding=ft.Padding(top=60, bottom=10,left=0,right=0)
                ),
                ft.Container(
                    content=ft.Row([marca, fecha, pantalla_in], alignment=ft.MainAxisAlignment.CENTER),
                    padding=ft.Padding(top=10, bottom=10,left=0,right=0)
                ),
                ft.Container(
                    content=ft.Row([memoria, almacenamiento, bateria], alignment=ft.MainAxisAlignment.CENTER),
                    padding=ft.Padding(top=10, bottom=10,left=0,right=0)
                ),
                ft.Container(
                    content=ft.Row([grosor, peso, velocidad_gpu], alignment=ft.MainAxisAlignment.CENTER),
                    padding=ft.Padding(top=10, bottom=10,left=0,right=0)
                ),
                ft.Container(
                    content=ft.Row([ancho_px, alto_px, pantalla_tipo], alignment=ft.MainAxisAlignment.CENTER),
                    padding=ft.Padding(top=10, bottom=10,left=0,right=0)
                ),
                ft.Container(
                    content=ft.Row([numero_valoraciones, numero_estrellas], alignment=ft.MainAxisAlignment.CENTER),
                    padding=ft.Padding(top=10, bottom=10,left=0,right=0)
                ),
                texto_opinion,
                ft.Container(
                    content=ft.Row([checkbox_si, checkbox_no], alignment=ft.MainAxisAlignment.CENTER),
                    padding=ft.Padding(top=10, bottom=10,left=0,right=0)
                ),
                boton, 
                resultado,
                ft.Container(
                    content=ft.Row([autores], alignment=ft.MainAxisAlignment.CENTER),
                    expand=True,
                    padding=ft.Padding(top=10, bottom=10,left=0,right=0)
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER, 
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

    page.add(fondo)

#Ejecutar Main
ft.app(target=main, view=ft.WEB_BROWSER)
