# PROYECTO 1: OFERTAS MOBILES

## DESCRIPCIÓN
Este proyecto implementa un modelo de inteligencia artificial el cual, vía una interfaz de usuario, indica la calidad sobre una oferta de un dispositivo mobil. 

Se ha utilizado web scrapping mediante una API para obtener una gran cantidad de datos mobiles, luego se ha realizado una limpieza de los mismos para poder entrenar un modelo.

Luego se ha diseñado una interfaz interactiva con el usuario para poder indicar tanto los componentes del mobil como el precio, el modelo realizara una prediccion de su precio, luego esta se compara con el precio real.

## ESTRUCTURA DEL PROYECTO
```
📂 proyecto_01
│-- 📂 web_scraping
│   │-- Comparar_ids.ipynb
│   │-- Get_products.ipynb
|
│-- 📂 data_cleaning
│   │-- CleanDaraframe.ipynb
│   │-- Outliders.ipynb
|
│-- 📂 visualizacion
│   │-- Visualizacion.ipynb
|
│-- 📂 model_training
|   |
│   │-- 📂 models
|   |   |-- encoder_ohe.joblib
|   |   |-- model_gb_data.zip
|   |   |-- model.joblib
|   |   |-- scaler.joblib
|   |   |-- X_test.csv
|   |   |-- X_train.csv
|   |   |-- y_test.csv
|   |   |-- y_train.csv
│   │-- TrainModel.ipynb
|
│-- 📂 interfaz
│   │-- interficie_online.py
│   │-- mobile_icon.png
|
│-- 📂 flask_server
│   │-- main.py
|   |
│   │-- 📂 model
|   |   |-- encoder_ohe.joblib
|   |   |-- model_gb_data.zip
|   |   |-- model.joblib
|   |   |-- scaler.joblib
|   |   |-- X_test.csv
|   |   |-- X_train.csv
|   |   |-- y_test.csv
|   |   |-- y_train.csv
|
│-- 📂 Other
│   │-- graficos.pdf
│   │-- data_stats.md
|
│-- 📂 res
│-- README.md
│-- requirements.txt
│-- config.json
```

## INSTALACIÓN

1. Clonar el repositorio:
```sh
$ git clone https://github.com/usuario/proyecto.git
$ cd proyecto
```
2. Crear un entorno virtual e instalar dependencias:
```sh
$ python -m venv env
$ source env/bin/activate  # Windows: env\Scripts\activate
$ pip install -r requirements.txt
```

## USO DEL REPOSITORIO

### 1. Web Scraping
Ejecuta los siguientes cuadernos de jupyter de web scraping para obtener los datos:  

[Comparar Ids](web_scraping/Comparar_ids.ipynb)  
[Get Products](web_scraping/Comparar_ids.ipynb)


### 2. Limpieza de Datos

Ejecuta los siguientes cuadernos de jupyter de limpieza para obtener datos limpios:  

[Clean Dataframe](web_scraping/Comparar_ids.ipynb)  
[Outliders](web_scraping/Comparar_ids.ipynb)

### 3. Visualización
Ejecuta el siguiente cuaderno de jupyter para obtener distintos graficos sobre los datos y para generar un .md con diferentes estadisticas:

[Visualizacion](web_scraping/Comparar_ids.ipynb)  

>[!NOTE]
>Los contenidos generados en la visualización se encuentran en la carpeta Others

### 4. Entrenamiento del Modelo
Ejecuta el siguiente cuaderno de jupyter para realizar entrenamiento del modelo y posteriormente guardarlo:  

[Entrenamiento del Modelo](web_scraping/Comparar_ids.ipynb)  


### 5. Servidor Flask
Levanta el servidor Flask para iniciar las peticiones de oferta:

[Servidor Flask](web_scraping/Comparar_ids.ipynb)  

### 6. Interfaz

Ejecuta la interfaz para interactuar con el modelo:

[Interfaz](web_scraping/Comparar_ids.ipynb)  


## ARCHIVOS ADICIONALES
- **others/**: Contiene otros archivos auxiliares.
- **res/**: Carpeta de recursos, imágenes, modelos entrenados, etc.
- **config.json**: Configuración del proyecto.

## CONTRIBUCIÓN
Si deseas contribuir, por favor sigue estos pasos:
1. Realiza un fork del repositorio.
2. Crea una nueva rama.
3. Realiza tus cambios y haz un commit.
4. Envía un pull request.

## LICENCIA
Este proyecto es completamente de codigo abierto.
