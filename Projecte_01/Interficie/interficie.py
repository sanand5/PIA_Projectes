import flet as ft

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


    image = ft.Image(src="PIA/PROJECTE/mobile_icon.png", width=200, height=200, )

    title = ft.Text("ANÁLISIS DE OFERTAS MÓVILES\n", size=32, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE)
    title_row = ft.Column([
        image,
        title
    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    subtitle = ft.Text("Ingrese su oferta en dispositivos móviles y le calcularemos lo buena que es:\n", size=20, italic=True, color=ft.colors.BLUE_900)

    marca = ft.TextField(width=250,bgcolor=ft.colors.WHITE, label="Marca", border_color=ft.colors.BLACK, label_style=ft.TextStyle(color=ft.colors.BLACK), text_style=ft.TextStyle(color=ft.colors.BLACK))
    precio = ft.TextField(width=250, bgcolor=ft.colors.WHITE, label="Precio (€)", keyboard_type=ft.KeyboardType.NUMBER, border_color=ft.colors.BLACK, label_style=ft.TextStyle(color=ft.colors.BLACK), text_style=ft.TextStyle(color=ft.colors.BLACK))

    memoria = ft.Dropdown(width=250, label="Número de Memoria", options=[
        ft.dropdown.Option("2 GB"),
        ft.dropdown.Option("4 GB"),
        ft.dropdown.Option("6 GB"), 
        ft.dropdown.Option("8 GB"), 
        ft.dropdown.Option("12 GB"), 
        ft.dropdown.Option("16 GB"), 
        ft.dropdown.Option("24 GB")
    ], border_color=ft.colors.BLACK, label_style=ft.TextStyle(color=ft.colors.BLACK), text_style=ft.TextStyle(color=ft.colors.BLACK), bgcolor=ft.colors.WHITE)

    almacenamiento = ft.Dropdown(width=250, label="Almacenamiento", options=[
        ft.dropdown.Option("16 GB"),
        ft.dropdown.Option("32 GB"),
        ft.dropdown.Option("64 GB"),
        ft.dropdown.Option("128 GB"),
        ft.dropdown.Option("256 GB"),
        ft.dropdown.Option("512 GB"),
        ft.dropdown.Option("1 TB"),
    ], border_color=ft.colors.BLACK, label_style=ft.TextStyle(color=ft.colors.BLACK), text_style=ft.TextStyle(color=ft.colors.BLACK), bgcolor=ft.colors.WHITE)

    resultado = ft.Text(color=ft.colors.BLACK)

    def calcular_oferta(e):
        if oferta: 
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
        ft.Row([marca, precio], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([memoria, almacenamiento], alignment=ft.MainAxisAlignment.CENTER),
        boton, resultado, autores
    ])


    page.add(fondo)

ft.app(target=main) 