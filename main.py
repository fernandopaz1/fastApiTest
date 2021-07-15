from fastapi import FastAPI, Query
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
    tax: Optional[float] = None

# update item debe recibir el numero que se lo paso por la url
# y un objeto tipo Item que me lo pasan por el body
# el body se lo podemos pasar desde la pagina de documentacion
# en el boton try out del metodo put
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}



fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

# Para pasarle parametros a la función hay que pasarselos en la url despues del ?
# los parametros van separados por &
# url?param1=valor1&param2=valor2


@app.get("/items/{item_id}")
async def read_item(item_id: str, q: Optional[str] = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

# como bool se convierte automaticamente a boolean entnces en la url puedo
# porner short=true, 1, True, on, yes y lo toma como true

@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(user_id: int, item_id: str, q: Optional[str] = None, short: bool = False):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

# ejemplo de url con multiples parametros
# http://127.0.0.1:8000/users/1/items/2


@app.get("/items/needyGet/{item_id}")
async def read_user_item(item_id: str, needy: str):
    item = {"item_id": item_id, "needy": needy}
    return item

# Ejemplo de parametros requeridos, si no hay paramet
# http://127.0.0.1:8000/items/needyGet/1  asi como esta tira error
# http://127.0.0.1:8000/items/needyGet/1?needy=1 Esta es la froma correcta de hacer un get con 
# parametros necesarios


@app.post("/items/posted/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict
# Aca estamos procesando los datos pasados por el body de
# y los retornamos con modificaciones

@app.put("/items/{item_id}")
async def create_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.dict()}
# aca usamos put porque put es un metodo para poner elementos
# en la url, si se quiere hacer algo mas general se debe usar post


@app.put("/items/posted/{item_id}")
async def create_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.dict()}



# Podemos pasar parametros con valores default de la forma
# q: Optional[str] = none   define que el valor de q es opciona y por default es none
# q: Optiona[str] = Query(None) hace lo mimos pero permite agregar mas parametros
#     q: Optional[str] = Query(None, min_length=3, max_length=50, regex="^fixedquery$") 
# la ultima linea agrega restricciones de lognitud y un regex que debe cumplir
# q: Optional[str] = Query("fixedquery", min_length=3) en este caso el valor por default es fixedquery
# q: str es un valor requerido pero de esta forma no podemos hacer restricciones
# q: str = Query(..., min_length=3) la forma de meter restricciones con query es poniendo ... en lugar del default
@app.get("/items/")
async def read_items(
    q: Optional[str] = Query(None, min_length=3, max_length=50, regex="^fixedquery$")
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

