from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional #para parametros opcionales

app = FastAPI()

@app.get("/")     # dirección base / me devuelve el json en formato string
async def read_root():
    return {"Hello": "World"}

# si hay uno con path /items/hola o algo asi evalua siempre el que tiene path por parametro
# por lo que hay que poner el de path fijo antes
@app.get("/items/{item_id}")   # como le paso el parametro opcional? /items/10?q=Mi%20Parametro%20Opcional
async def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

# montamos el servidor con uvicorn main:app --reload
# la documentacion esta en http://127.0.0.1:8000/docs o alternativamente http://127.0.0.1:8000/redoc

# Aca defino el tipo de objeto que recibe el metodo put
class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None

# update item debe recibir el numero que se lo paso por la url
# y un objeto tipo Item que me lo pasan por el body
# el body se lo podemos pasar desde la pagina de documentacion
# en el boton try out del metodo put
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
