from typing import Union
from fastapi import Depends, FastAPI
from functools import lru_cache
from pydantic import BaseModel
import yaml
import config


@lru_cache()
def get_settings():
    return config.Settings()


app = FastAPI()


def read_config(filename="config.yaml"):
    with open(filename) as f:
        data = yaml.load(f)
    print(data)
    return data


@app.get("/")
def read_root(settings: config.Settings = Depends(get_settings)):
    read_config()
    return {"Under": "Construction", "appname": settings.app_name, }


@app.post("/de-identify")
def deidentify(settings: config.Settings = Depends(get_settings)):
    return {"Under": "Construction"}


@app.post("/pseudonymize")
def pseudonymize(settings: config.Settings = Depends(get_settings)):
    return {"Under": "Construction"}


@app.post("/de-pseudonymize")
def depseudonymize(settings: config.Settings = Depends(get_settings)):
    return {"Under": "Construction"}
