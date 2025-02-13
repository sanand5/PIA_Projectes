# Diari de el projecte 01
## 11/02/2025
Planificació del projecte i tecnologies a útlilitzar.

### Planificació
La idea es obtindre en webscraping una datases per a entrenar la IA.
Poducte: Mobils
Dades a recollir: Marca,Modelo,Fecha de lanzamiento,Precio de venta,Procesador,RAM (GB),Almacenamiento (GB),Batería (mAh),Cámaras traseras,Resolución cámara principal (MP),FPS cámara trasera,Resolución cámara frontal (MP),FPS cámara frontal,Tamaño pantalla (pulgadas),Resolución pantalla,Frecuencia actualización (Hz),Precio de lanzamiento
Despres de recollir les dades necesitarem fer webscraing per a veure quines dades podem obtindre , també hem de determinar quin resultat volem obtindre esa dir si volem un true o false per a si es una bona resposta o no o volem un percentattje de quan bona oferta es
Target: De moment nem ha deixar-ho en True o False per a ssaber si es o no una bona oferta en un futur es valorara fer per percentatje de bona oferta.
Despres de tindre el dataset entrenarem la ia, de moment nem a centrarmos en el dataset.

Nem a intentar fer webscraping de amazon , phonearea i si no de mercado libre
Hem decidir gastar la api de rapidapi per a poder fer web scraping de amazon


## Coses a fer:
- Web scrapping
- Pujar dataset a mongo
- Crear un model per a entrenar
- Crear una api
- Crear el frontend pogent fer peticio a la api

### Tecnologies
Python
BBDD : MongoDB
Interficie: Flet
Llibreries IA: (sckitlearn / keras)
