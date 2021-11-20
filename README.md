# Proyecto-Grupo25-202120

## EJECUCIÓN PROGRAMA: 

Si desea ejecutar el proyecto se debe tener instalado en su máquina Docker y Docker-Compose.
En estos links puede encontrar buena información para ello. 
-	Docker : https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04-es
-	Docker-compose : https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-20-04-es

Clonar repositorio: 
-	git clone git@github.com:MISW-4204-ComputacionEnNube/Proyecto-Grupo25-202120.git

Ejecutar:
- cd Proyecto-Grupo25-202120
-	sudo docker-compose build --build-arg postgres_host=$POSTGRES_HOST --build-arg postgres_pass=$POSTGRES_PASS
-	sudo docker-compose up  -d
- cd flaskr 
- docker ps ( para revisar el container_id de la app de flask )
- docker exec -it container_id /bin/bash
- celery -A app.celery_app worker --detach
- exit

## DOCUMENTACIÓN PROYECTO:

En la [wiki](https://github.com/MISW-4204-ComputacionEnNube/Proyecto-Grupo25-202120/wiki) se encuentra la documentación del proyecto .
