from typing import Union, Any, Dict
from fastapi import Depends, FastAPI
from functools import lru_cache
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from pseudonymize import perform_pseudonymization
from depseudonymize import perform_depseudonymization
from deidentify import perform_deidentification
import json

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


@app.post("/de-identify")
def deidentify(resource: Dict[Any, Any], settings: config.Settings = Depends(get_settings)):
    """De-identify a FHIR resource. 
    Accept a FHIR resource as any valid JSON. 
    Then apply the settings rules and return the de-identified object.
    """
    return perform_deidentification(resource, settings)


@app.post("/pseudonymize")
def pseudonymize(resource: Dict[Any, Any], settings: config.Settings = Depends(get_settings)):
    """Pseudonymize a FHIR resource. 
    Accept a FHIR resource as any valid JSON. 
    Then apply the settings rules and return the pseudonymized object.
    """
    return perform_pseudonymization(resource, settings)


@app.post("/de-pseudonymize")
def depseudonymize(resource: Dict[Any, Any], settings: config.Settings = Depends(get_settings)):
    """De-pseudonymize a FHIR resource. 
    Accept a pseudonymized FHIR resource as any valid JSON. 
    Then apply the settings rules and return the de-pseudonymized object.
    """
    return perform_depseudonymization(resource, settings)
