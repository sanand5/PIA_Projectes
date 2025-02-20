import flet as ft


#-- CAMBIOS A REALIZAR --#
# 1. Arreglar opcion de campos vacios

def main(page: ft.Page):
    page.title = "ANÁLISIS DE OFERTAS MÓVILES"
    page.bgcolor = ft.colors.BLUE_50
    oferta = True
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    fondo = ft.Container(
        expand=True,  
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center, 
            end=ft.alignment.bottom_center,  
            colors=[ft.colors.BLUE_100, ft.colors.WHITE]
        ),
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[]
        )
    )
    def actualizar_precio(e):
        precio_label.value = f"Precio: {int(slider_precio.value)} €"
        page.update()

    precio_label = ft.Text("Precio", color=ft.colors.BLACK)

    slider_precio = ft.Slider(min=0, max=3000, divisions=1500, value=1500, on_change=actualizar_precio)
    image = ft.Image(src="PIA/PROJECTE/mobile_icon.png", width=200, height=200)

    title = ft.Text("ANÁLISIS DE OFERTAS MÓVILES", size=32, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE)
    title_row = ft.Column([
        image,
        title
    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    subtitle = ft.Text("Ingrese su oferta en dispositivos móviles y le calcularemos lo buena que es:\n", size=20, italic=True, color=ft.colors.BLUE_900)

    fecha = ft.TextField(width=250,bgcolor=ft.colors.WHITE, label="Año de salida", border_color=ft.colors.BLACK, label_style=ft.TextStyle(color=ft.colors.BLACK), text_style=ft.TextStyle(color=ft.colors.BLACK))

    marca = ft.TextField(width=250,bgcolor=ft.colors.WHITE, label="Marca", border_color=ft.colors.BLACK, label_style=ft.TextStyle(color=ft.colors.BLACK), text_style=ft.TextStyle(color=ft.colors.BLACK))
    resolucion = ft.TextField(width=250,bgcolor=ft.colors.WHITE, label="Resolución", border_color=ft.colors.BLACK, label_style=ft.TextStyle(color=ft.colors.BLACK), text_style=ft.TextStyle(color=ft.colors.BLACK))

    memoria = ft.Dropdown(width=250, label="Número de Memoria", options=[
        ft.dropdown.Option("2GB"),
        ft.dropdown.Option("4GB"),
        ft.dropdown.Option("6GB"), 
        ft.dropdown.Option("8GB"), 
        ft.dropdown.Option("12GB"), 
        ft.dropdown.Option("16GB"), 
        ft.dropdown.Option("24GB")
    ], border_color=ft.colors.BLACK, label_style=ft.TextStyle(color=ft.colors.BLACK), text_style=ft.TextStyle(color=ft.colors.BLACK), bgcolor=ft.colors.WHITE)

    almacenamiento = ft.Dropdown(width=250, label="Almacenamiento", options=[
        ft.dropdown.Option("16GB"),
        ft.dropdown.Option("32GB"),
        ft.dropdown.Option("64GB"),
        ft.dropdown.Option("128GB"),
        ft.dropdown.Option("256GB"),
        ft.dropdown.Option("512GB"),
        ft.dropdown.Option("1TB"),
    ], border_color=ft.colors.BLACK, label_style=ft.TextStyle(color=ft.colors.BLACK), text_style=ft.TextStyle(color=ft.colors.BLACK), bgcolor=ft.colors.WHITE)

    bateria = ft.Dropdown(width=250, label="Bateria", options=[
        ft.dropdown.Option("2000 MaH"),
        ft.dropdown.Option("3000 MaH"),
        ft.dropdown.Option("3500 MaH"),
        ft.dropdown.Option("4000 MaH"),
        ft.dropdown.Option("5000 MaH"),
        ft.dropdown.Option("6000 MaH"),
        ft.dropdown.Option("7000 MaH"),
    ], border_color=ft.colors.BLACK, label_style=ft.TextStyle(color=ft.colors.BLACK), text_style=ft.TextStyle(color=ft.colors.BLACK), bgcolor=ft.colors.WHITE)

    resultado = ft.Text(color=ft.colors.BLACK)

    campos_vacios = any(not campo.value for campo in [fecha, marca, memoria, almacenamiento, bateria, slider_precio])

    def calcular_oferta(e):
        page.update()
        if campos_vacios:
            resultado.value = "Faltan campos por rellenar"
            resultado.color = ft.colors.GREY
            resultado.weight = ft.FontWeight.BOLD

        elif oferta: 
            resultado.value = "La oferta introducida es una buena oferta!"
            resultado.color = ft.colors.GREEN
            resultado.weight = ft.FontWeight.BOLD
        else:
            resultado.value = "La oferta introducida no es buena :("
            resultado.color = ft.colors.RED
            resultado.weight = ft.FontWeight.BOLD
        
        page.update()
    boton = ft.ElevatedButton("Calcular oferta",
                            on_click=calcular_oferta,
                            bgcolor=ft.colors.BLUE,
                            color=ft.colors.WHITE,
                            width=260,
                            height=50,
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)))
    
    autores = ft.Text("\n\nHecho por: Andreu Sanz y Gerard Grau", size=16, italic=True, color=ft.colors.BLUE)

    fondo.content.controls.extend([
        title_row, subtitle, 
        ft.Row([precio_label],alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([slider_precio],alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([marca, fecha,resolucion], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([memoria, almacenamiento, bateria], alignment=ft.MainAxisAlignment.CENTER),
        boton, resultado, autores
    ])


    page.add(fondo)

ft.app(target=main) 