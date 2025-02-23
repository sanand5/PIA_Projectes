import flet as ft
import pandas as pd
import pickle
from funciones import obtener_valor_numerico
from funciones import prediccion

def cargar_modelo(path):
    with open(path, 'rb') as archivo:
        modelo = pickle.load(archivo) 
    return modelo
def sacar_promedio(num_estrellas, num_valoraciones):
    return num_valoraciones / num_estrellas


def main(page: ft.Page):
    modelo = cargar_modelo("C:/Users/Gerard/Desktop/VISUAL_STUDIO/PIA/PROYECTO/limpieza/modelo_entrenado.pkl")
    page.title = "ANÁLISIS DE OFERTAS MÓVILES"
    page.bgcolor = ft.colors.BLUE_50
    page.scroll = "auto"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    precio = ft.TextField(width=220, label="Precio (€)", border_color=ft.colors.BLACK, label_style=ft.TextStyle(color=ft.colors.BLACK), text_style=ft.TextStyle(color=ft.colors.BLACK))
    precio_anterior = ft.TextField(width=220, label="Precio anterior (€)", border_color=ft.colors.BLACK, label_style=ft.TextStyle(color=ft.colors.BLACK), text_style=ft.TextStyle(color=ft.colors.BLACK))
    
    image = ft.Image(src="C:/Users/Gerard/Desktop/VISUAL_STUDIO/PIA/PROYECTO/mobile_icon.png", width=150, height=150)
    title = ft.Text("ANÁLISIS DE OFERTAS MÓVILES", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE)
    subtitle = ft.Text("Ingrese su oferta en dispositivos móviles y le calcularemos lo buena que es:", size=16, italic=True, color=ft.colors.BLUE_900)
    
    title_row = ft.Column([image, title], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10)
    
    fecha = ft.TextField(width=220, label="Año de salida", border_color=ft.colors.BLACK, label_style=ft.TextStyle(color=ft.colors.BLACK), text_style=ft.TextStyle(color=ft.colors.BLACK))
    marca = ft.TextField(width=220, label="Marca", border_color=ft.colors.BLACK, label_style=ft.TextStyle(color=ft.colors.BLACK), text_style=ft.TextStyle(color=ft.colors.BLACK))
    pantalla = ft.TextField(width=220, label="Tamaño de pantalla (pulgadas)", border_color=ft.colors.BLACK, label_style=ft.TextStyle(color=ft.colors.BLACK), text_style=ft.TextStyle(color=ft.colors.BLACK))
    pantalla_tipo = ft.TextField(width=220, label="Tipo de pantalla", border_color=ft.colors.BLACK, label_style=ft.TextStyle(color=ft.colors.BLACK), text_style=ft.TextStyle(color=ft.colors.BLACK))
    grosor = ft.TextField(width=220, label="Profundidad (cm)", border_color=ft.colors.BLACK, label_style=ft.TextStyle(color=ft.colors.BLACK), text_style=ft.TextStyle(color=ft.colors.BLACK))
    peso = ft.TextField(width=220, label="Peso (g)", border_color=ft.colors.BLACK, label_style=ft.TextStyle(color=ft.colors.BLACK), text_style=ft.TextStyle(color=ft.colors.BLACK))
    velocidad_gpu = ft.TextField(width=220, label="Velocidad de CPU (GHz)", border_color=ft.colors.BLACK, label_style=ft.TextStyle(color=ft.colors.BLACK), text_style=ft.TextStyle(color=ft.colors.BLACK))
    ancho_px = ft.TextField(width=220, label="Ancho (px)", border_color=ft.colors.BLACK, label_style=ft.TextStyle(color=ft.colors.BLACK), text_style=ft.TextStyle(color=ft.colors.BLACK))
    alto_px = ft.TextField(width=220, label="Alto (px)", border_color=ft.colors.BLACK, label_style=ft.TextStyle(color=ft.colors.BLACK), text_style=ft.TextStyle(color=ft.colors.BLACK))
    memoria = ft.Dropdown(width=220, label="Número de Memoria", options=[ft.dropdown.Option(f"{x}GB") for x in [2, 4, 6, 8, 12, 16, 24]], border_color=ft.colors.BLACK)
    almacenamiento = ft.Dropdown(width=220, label="Almacenamiento", options=[ft.dropdown.Option(f"{x}GB") for x in [16, 32, 64, 128, 256, 512, '1TB']], border_color=ft.colors.BLACK)
    bateria = ft.Dropdown(width=220, label="Batería", options=[ft.dropdown.Option(f"{x} MaH") for x in [2000, 3000, 3500, 4000, 5000, 6000, 7000]], border_color=ft.colors.BLACK)
    numero_valoraciones = ft.TextField(width=220, label="Numero de valoraciones", border_color=ft.colors.BLACK, label_style=ft.TextStyle(color=ft.colors.BLACK), text_style=ft.TextStyle(color=ft.colors.BLACK))
    numero_estrellas = ft.TextField(width=220, label="Numero de estrellas", border_color=ft.colors.BLACK, label_style=ft.TextStyle(color=ft.colors.BLACK), text_style=ft.TextStyle(color=ft.colors.BLACK))

    resultado = ft.Text(color=ft.colors.BLACK)
    
    def calcular_oferta(e):
        marca_numerico = obtener_valor_numerico(marca.value)
        tipo_numerico = obtener_valor_numerico(pantalla_tipo.value)
        promedio_valoraciones = promedio_valoraciones(numero_estrellas,numero_valoraciones)
        precio_oferta = precio.value
        datos_movil = {
                "ano":fecha.value,
                "memoria": almacenamiento.value,
                "marca": marca_numerico,
                "pantalla_in": pantalla.value, 
                "pantalla_tipo": tipo_numerico, 
                "velocidad_cpu_ghz": velocidad_gpu.value,
                "ram": memoria.value, 
                "grosor": grosor.value, 
                "peso":peso.value,
                'ancho_px':ancho_px.value, 
                'alto_px':alto_px.value,     
                "bateria": bateria.value,  
                'promedio_valoraciones':promedio_valoraciones, 
                'precio_anterior':precio_anterior.value,
}
        df_movil = pd.DataFrame([datos_movil])
        precio_prediccion = prediccion(df_movil, modelo)

        if(precio_oferta<precio_prediccion):
                resultado.value = f"Es una buena oferta"
                resultado.color = ft.colors.GREEN
                resultado.weight = ft.FontWeight.BOLD
        else:
                resultado.value = f"No es una buena oferta"
                resultado.color = ft.colors.RED
                resultado.weight = ft.FontWeight.BOLD
        page.update()
    
    boton = ft.ElevatedButton("Calcular oferta", on_click=calcular_oferta, bgcolor=ft.colors.BLUE, color=ft.colors.WHITE, width=220, height=40)
    
    autores = ft.Text("\n\nHecho por: Andreu Sanz y Gerard Grau", size=14, italic=True, color=ft.colors.BLUE)
    
    fondo = ft.Container(
        expand=True, gradient=ft.LinearGradient(begin=ft.alignment.top_center, end=ft.alignment.bottom_center, colors=[ft.colors.BLUE_100, ft.colors.WHITE]),
        content=ft.Column([
            title_row, subtitle,
            ft.Row([precio, precio_anterior], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
            ft.Row([marca, fecha, pantalla], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
            ft.Row([memoria, almacenamiento, bateria], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
            ft.Row([grosor, peso, velocidad_gpu], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
            ft.Row([ancho_px, alto_px, pantalla_tipo], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
            boton, resultado, autores
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20)
    )
    
    page.add(fondo)

ft.app(target=main)
