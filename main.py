from fastapi import FastAPI, Query, Path
from pydantic import BaseModel
from typing import Optional, List #para parametros opcionales

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
# Ejemplo de url que funciona http://127.0.0.1:8000/items/query/restringida/?q=fixedquery
@app.get("/items/query/restringida/")
async def read_items(
    q: Optional[str] = Query(None, min_length=3, max_length=50, regex="^fixedquery$")
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# Si la variable es una lista hay que importar la libreria List 
# q: Optional[List[str]] = Query(None) decimos que q es opcional de tipo lista de string y su default es None
# para pasarle parametros via url  hay que usar http://localhost:8000/items/listas/?q=foo&q=bar
# q: List[str] = Query(["foo", "bar"]) aca es lo mismo que arriba pero definiendo el default como ["foo", "bar"]
# q: list = Query([])  

@app.get("/items/listas/")
async def read_items(q: Optional[List[str]] = Query(["foo", "bar"])):
    query_items = {"q": q}
    return query_items

# a los parametros de la query se les puede agregar metadatos 
# como titulo, description, si esta deprecado o no y un alias para la variable
# en vez de tener que usar el parametro q pasamos ese alias a la url
# la url indicada para este caso (con alias incluido ) es
# http://127.0.0.1:8000/items/metadatos/?item-query=foobaritems
@app.get("/items/metadatos/")
async def read_items(
    q: Optional[str] = Query(
        None,
        title="Query string",
        description="Query string for the items to search in the database that have a good match",
        min_length=3,
        alias="item-query",
        deprecated=True
    )
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# Para hacer validaciones numericas es necesation importar Path desde fastapi
# Path es analogo a Query que permite hacer validaciones pero esta ve para valores enteros
# si nuestra url recibe varios parametro es importante que se ponga primero los parametros 
# requeridos y luego los opcionales
# tambien es importante que pongamos antes los que tienen un default definido que los que no lo tienen
# * si el primer parametro es un asterisco entonces indicamos que la funcion recibe por parametro kwargs 
# un tamaño de parametro indeterminado incluso si hay parametros sin default 

# item_id: int = Path(..., title="The ID of the item to get", ge=1) en esta linea pedimos que item_id sea requerido y 
# ademas debe cumplir que sea mayor o igual a 1 (greather or equal)
# gt: greather than  #le: less or equal

#  size: float = Query(..., gt=0, lt=10.5) esta linea requiere un valor float con las restricciones escritas dentro
# notar que se usa Query y no path

@app.get("/items/integerValidations/{item_id}/")
async def read_items(
    *, 
    q: str, 
    item_id: int = Path(..., title="The ID of the item to get", gt=0, le=1000),
    size: float = Query(..., gt=0, lt=10.5)
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results