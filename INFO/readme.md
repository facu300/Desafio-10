Mer



Comados para correr el server
(1) En carpeta contenedora del proyecto
Para ejecutar comandos de git(clonar)
- git clone url_del_repo

(2) En la carpeta del repositorio
Para ejecutar comandos del entorno
- python -m venv nombre_entorno  #para crear el entorno
- nombre_entorno\Scripts\activate
- nombre_entorno\Scripts\desactivate
- Si no les reconoce el comando >>> cd nombre_entorno >>> cd Scripts >>> activate o deactivate
- python -m pip install --upgrade pip

(3) En la carpeta del repositorio instalar paquetes del archivo requeriment.txt
- pip install -r requeriments.txt

(4) En la carpeta del proyecto
Para ejecutar comandos del manage.py
- python manage.py runserver
