# Fast Api

Este es un proyecto para explorar la libreria Fast Api según la [documentación](https://fastapi.tiangolo.com/es/)

Para ejecutar este proyecto en tu computadora tendras que ejecutar los siguientes pasos.

`git clone https://github.com/fernandopaz1/fastApiTest.git`

`cd fastApiTest`

### Entorno virtual

Creamos un entorno virtual y lo activamos

`python3 -m venv myvenv`

`source myenv/bin/activate`

Actualizamos el gestor de paquetes de python e instalamos los requerimientos de este proyecto.

`python3 -m pip install --upgrade pip`

` pip install -r requirements.txt`

### Levantar servidor

Para montar el servidor usamos el comando

`uvicorn main:app --reload`

Listo tu pagina deberia estar dispoible en la dirección [localhost](http://127.0.0.1:8000/)

ante cualquier cambio del código que hagas la pagina se actualiza automáticamente debido a la opción `--reload`
