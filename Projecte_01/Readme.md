# PROJECTE 1: OFERTA MOBILS
- [PROJECTE 1: OFERTA MOBILS](#projecte-1-oferta-mobils)
  - [DESCRIPCIÓ](#descripció)
    - [Esquema de funcionament](#esquema-de-funcionament)
    - [Previsualització](#previsualització)
  - [ESTRUCTURA DEL PROJECTE](#estructura-del-projecte)
  - [INSTALACIÓ](#instalació)
  - [US DEL REPOSITORI](#us-del-repositori)
    - [1. Web Scraping](#1-web-scraping)
    - [2. Netetja de dades](#2-netetja-de-dades)
    - [3. Visualización](#3-visualización)
    - [4. Entrenament del model](#4-entrenament-del-model)
    - [5. Servidor amb Flask](#5-servidor-amb-flask)
    - [6. Interfície](#6-interfície)
  - [ARXIUS ADDICIONALS](#arxius-addicionals)
  - [CONTRIBUCIÓ](#contribució)
  - [LLICÈNCIA](#llicència)

## DESCRIPCIÓ
Aquest projecte implementa un model d'intel·ligència artificial que, mitjançant una interfície d'usuari, indica la qualitat d'una oferta d'un dispositiu mòbil.

S'ha utilitzat web scraping mitjançant una API (Scraper API) per a obtindre una gran quantitat de dades de mòbils. A continuació, s'ha fet una neteja d'aquestes dades per a poder entrenar el model.  

Després, s'ha dissenyat una interfície interactiva amb l'usuari perquè aquest puga introduir tant els components del mòbil com el seu preu. El model realitzarà una predicció del preu i, posteriorment, aquesta es compararà amb el preu real.

### Esquema de funcionament
![Funcionament](<other/Diagrama.png>)

### Previsualització
![Interficie](<other/Interfaz.png>)

## ESTRUCTURA DEL PROJECTE
```
📂 projecte_01 
│-- 📂 web_scraping
│   │-- comparar_ids.ipynb
│   │-- get_products.ipynb
│   │-- config.py
|
│-- 📂 data_cleaning
│   │-- clean_dataset.ipynb
│   │-- outliders.ipynb
|
│-- 📂 visualitzacio
│   │-- visualitzacio.ipynb
|
│-- 📂 model_training
│   │-- 📂 models
│   │-- train_model.ipynb
|
│-- 📂 interficie
│   │-- interficie.py
|
│-- 📂 flask_server
│   │-- app.py
│   │-- config.py
│   │-- database.py
│   │-- model.py
│   │-- 📂 model
|
│-- 📂 backup
│-- 📂 other
│-- 📂 res
│-- README.md
│-- requirements.txt
│-- docker-compose.yml
```

## INSTALACIÓ

1. Clonar el repositori:
```sh
$ git clone https://github.com/usuari/PIA_Projectes.git
$ cd PIA_Projectes
```
2. Crear un entorn virtual e instalar dependencies:
```sh
$ python -m venv env
$ source env/bin/activate  # Windows: env\Scripts\activate
$ pip install -r requirements.txt
```
3. Crear un contenidor de Mongodb
```sh
$ docker compose up -d
```

## US DEL REPOSITORI

### 1. Web Scraping
**[web_scraping/comparar_ids.ipynb](web_scraping/comparar_ids.ipynb):** Aquest quadern té utilitats per als fitxers d'IDs.  
**[web_scraping/get_products.ipynb](web_scraping/get_products.ipynb):** Per a realitzar el web scraping a Amazon amb Scraper API i pujar les dades a MongoDB.

### 2. Netegja de dades  
**[data_cleaning/clean_dataset.ipynb](data_cleaning/clean_dataset.ipynb):** Netegja de les dades.  
**[data_cleaning/outliders.ipynb](data_cleaning/outliders.ipynb):** Detecció de *outliers*.

### 3. Visualització  
**[visualitzacio/visualitzacio.ipynb](visualitzacio/visualitzacio.ipynb):** Obtenir diferents gràfics de les dades i generar una vista general del dataset.

>[!NOTE]  
>El contingut generat en aquest Jupyter es visualitza en la carpeta [other](other/).

### 4. Entrenament del model  
**[model_training/train_model.ipynb](model_training/train_model.ipynb):** Entrenament del model i desada d'aquest.
**[model_training/models](model_training/models):** models ja entrenats.

### 5. Servidor amb Flask  
**[flask_server/config.py](flask_server/config.py):** Configuració del servidor.  
**[flask_server/database.py](flask_server/database.py):** Gestiona les connexions amb la base de dades.  
**[flask_server/model.py](flask_server/model.py):** Gestiona la càrrega del model i les peticions.  
**[flask_server/app.py](flask_server/app.py):** Gestiona l'API.

>[!IMPORTANT]  
>El model ha d'estar carregat prèviament en [flask_server/model](flask_server/model).
### 6. Interfície  

**[Interfície](interficie/):** El usuari interactua amb una interfaç per a realitzar una petició al servidor amb les dades requerides, el servidor torna la predicció i es calcula lo bona que es la oferta.  
>[!IMPORTANT]  
>Per al correcte funcionament de la interfície, el servidor Flask ha d'estar en execució.  

## ARXIUS ADDICIONALS  
- **other/**: Conté altres arxius auxiliars.  
- **res/**: Carpeta de recursos, imatges, datasets, etc.  
- **backup/**: Es guarden les copies de seguretat necesaries  
- **requirements.txt**: Llistat de les dependències de Python necessàries.  

## CONTRIBUCIÓ  
Si vols contribuir, per favor segueix aquests passos:  
1. Fes un fork del repositori.  
2. Crea una nova branca.  
3. Fes els teus canvis i realitza un commit.  
4. Envia un pull request.  

## LLICÈNCIA  
Aquest projecte és completament de codi obert.
