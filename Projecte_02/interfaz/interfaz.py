import flet as ft
from datetime import datetime, timedelta
import requests

def main(page: ft.Page):

    # Configuración de la página con colores
    page.title = "Parking Controller"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 30
    page.bgcolor = "#E0E0E0" 
    
    # Variables de estado
    matricula = ft.Ref[ft.TextField]()
    estado = ft.Ref[ft.Text]()
    hora_limite = ft.Ref[ft.Text]()
    boton_pagar = ft.Ref[ft.ElevatedButton]()
    boton_comprobar = ft.Ref[ft.ElevatedButton]()
    
    # Función para validar matrícula
    def validar_matricula(e):
        if matricula.current.value.strip():
            boton_comprobar.current.disabled = False
            boton_comprobar.current.bgcolor = "#6d0899" 
        else:
            boton_comprobar.current.disabled = True
            boton_comprobar.current.bgcolor = "#616161"  # Gris oscuro desactivado
            boton_pagar.current.disabled = True
            boton_pagar.current.bgcolor = "#616161"  # Gris oscuro desactivado
        page.update()
    
    # Función para comprobar matrícula
    def comprobar_matricula(e):
        try:
            # Llamada a la API
            response = requests.get(f"http://localhost:8000/api/vehiculos/{matricula.current.value}")
            print(response)
            if response == 1:
                estado.current.value = "DENTRO"
                hora_limite.current.value = "--:--:--"
                estado.current.color = "#388E3C"  
                boton_pagar.current.disabled = False
                boton_pagar.current.bgcolor = "#1976D2" 
            elif response == 0:
                estado.current.value = "NO REGISTRADA"
                estado.current.color = "#D32F2F"  
                boton_pagar.current.disabled = True
                boton_pagar.current.bgcolor = "#616161"  
            elif response.status_code == 404:
                estado.current.value = "Error en el servidor"
                estado.current.color = "#D32F2F"  
                boton_pagar.current.disabled = True
                boton_pagar.current.bgcolor = "#616161"
        except Exception as ex:
            estado.current.value = f"ERROR: {str(ex)}"
            estado.current.color = "#D32F2F"        
        page.update()

    # Función para pagar
    def pagar_salir(e):
        ahora = datetime.now()
        limite = ahora + timedelta(minutes=15)
        hora_limite.current.value = limite.strftime("%H:%M:%S")
        hora_limite.current.color = "#1976D2"  # Azul
        estado.current.value = "PAGADO - PUEDE SALIR"
        estado.current.color = "#388E3C"  # Verde
        boton_pagar.current.disabled = True
        boton_pagar.current.bgcolor = "#616161"  # Gris oscuro desactivado
        boton_comprobar.current.disabled = True
        boton_comprobar.current.bgcolor = "#616161"  # Gris oscuro desactivado
        page.update()
    
    page.add(
        ft.Container(
            ft.Column(
                [
                    # Título
                    ft.Container(
                        ft.Text("PARKING CONTROLLER", 
                            size=32, 
                            weight=ft.FontWeight.BOLD,
                            color="#333333"),
                        padding=ft.padding.only(bottom=30)
                    ),
                    
                    ft.Container(
                        ft.TextField(
                            ref=matricula,
                            label="Matrícula del vehículo",
                            width=350,
                            height=50,
                            border_radius=10,
                            border_color="#BDBDBD",
                            focused_border_color="#1976D2",
                            bgcolor="#FFFFFF",
                            text_size=16,
                            on_change=validar_matricula,
                            autofocus=True,
                            capitalization=ft.TextCapitalization.CHARACTERS
                        ),
                        padding=ft.padding.only(bottom=20)
                    ),
                    

                    ft.Container(
                        ft.ElevatedButton(
                            ref=boton_comprobar,
                            text="COMPROBAR MATRÍCULA",
                            disabled=True,
                            on_click=comprobar_matricula,
                            width=350,
                            height=50,
                            bgcolor="#908d91",  
                            color="white",
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=10),
                                padding=20
                            )
                        ),
                        padding=ft.padding.only(bottom=10)
                    ),
                      
                    ft.Container(
                        ft.ElevatedButton(
                            ref=boton_pagar,
                            text="PAGAR Y SALIR",
                            disabled=True,
                            on_click=pagar_salir,
                            width=350,
                            height=50,
                            bgcolor="#908d91",  # Gris oscuro (desactivado)
                            color="white",
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=10),
                                padding=20
                            )
                        ),
                        padding=ft.padding.only(bottom=30)
                    ),
                    
                    # Estado
                    ft.Container(
                        ft.Row(
                            [
                                ft.Text("Estado: ", 
                                    size=18, 
                                    weight=ft.FontWeight.BOLD,
                                    color="#555555"),
                                ft.Text(ref=estado, 
                                    value="...", 
                                    size=18,
                                    color="#757575")
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        padding=10,
                        bgcolor="#FFFFFF",
                        border_radius=10,
                        width=350
                    ),
                    
                    # Hora límite
                    ft.Container(
                        ft.Row(
                            [
                                ft.Text("Hora límite de salida: ", 
                                    size=18, 
                                    weight=ft.FontWeight.BOLD,
                                    color="#555555"),
                                ft.Text(ref=hora_limite, 
                                    value="--:--:--", 
                                    size=18,
                                    color="#757575")
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        padding=10,
                        bgcolor="#FFFFFF",
                        border_radius=10,
                        width=350,
                        margin=ft.margin.only(top=15)
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            bgcolor="#EEEEEE",
            padding=40,
            border_radius=20
        )
    )

ft.app(target=main)