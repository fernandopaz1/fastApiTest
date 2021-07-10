from fastapi import FastAPI
from typing import Optional

app = FastAPI()

@app.get("/")     # dirección base / me devuelve el json en formato string
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")   # como le paso el parametro opcional? /items/10?q=Mi%20Parametro%20Opcional
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

# montamos el servidor con uvicorn main:app --reload
# la documentacion esta en http://127.0.0.1:8000/docs o alternativamente http://127.0.0.1:8000/redoc

