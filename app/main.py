from typing import Any, Dict
from fastapi import Depends, FastAPI
from functools import lru_cache
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from processor import process_data

import yaml
import config


@lru_cache()
def get_settings():
    return config.Settings()


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def read_config(filename="config.yaml"):
    with open(filename) as f:
        data = yaml.load(f)
    print(data)
    return data


@app.get("/")
async def read_root(settings: config.Settings = Depends(get_settings)):
    return RedirectResponse("/docs")


@app.post("/process")
def process(resource: Dict[Any, Any], settings: config.Settings = Depends(get_settings)):
    """Process a FHIR resource. 
    Accept a FHIR resource as any valid JSON. 
    Then apply the settings rules and return the processed object.
    """
    return process_data(resource, settings)
