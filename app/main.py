from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
import yaml


class Item(BaseModel):
    name: str
    price: float


app = FastAPI()


def read_config(filename="config.yaml"):
    with open(filename) as f:
        data = yaml.load(f)
    print(data)
    return data


@app.get("/")
def read_root():
    read_config()
    return {"Under": "Construction"}


@app.post("/de-identify")
def deidentify(item: Item):
    return {"Under": "Construction"}


@app.post("/pseudonymize")
def deidentify():
    return {"Under": "Construction"}


@app.post("/de-pseudonymize")
def deidentify():
    return {"Under": "Construction"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
