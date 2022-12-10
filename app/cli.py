import sys
import os
import json
import typer
from processor import process_data
import config
from deidentify import perform_deidentification
from depseudonymize import perform_depseudonymization
from pseudonymize import perform_pseudonymization
from rich import print


app = typer.Typer()


def read_resource_from_file(filename: str):
    """
    Read a fhir resource from file and return the json data
    """
    try:
        with open(filename, 'r') as jfile:
            json_data = json.load(jfile)
            # python -m rich.emoji
            print(f":thumbs_up: json {filename} read")
            return json_data
    except IOError as e:
        print(
            f":sad_but_relieved_face: File {filename} does not exist.")
        print(e)
        sys.exit(os.EX_OSFILE)
    except ValueError as e:
        print(
            f":sad_but_relieved_face: Cannot parse json data.")
        print(e)
        sys.exit(os.EX_OSFILE)


@app.command()
def deidentify(resource_filename: str, config_filename: str = typer.Argument("config.yaml")):
    resource = read_resource_from_file(resource_filename)
    settings = config.Settings(config_filename)
    ret = perform_deidentification(resource, settings)
    print(f'CLI Deidentify Result={ret}')


@app.command()
def pseudonymize(resource_filename: str, config_filename: str = typer.Argument("config.yaml")):
    resource = read_resource_from_file(resource_filename)
    settings = config.Settings(config_filename)
    ret = perform_pseudonymization(resource, settings)
    print(f'CLI Pseudonimize Result={ret}')


@app.command()
def depseudonymize(resource_filename: str, config_filename: str = typer.Argument("config.yaml")):
    resource = read_resource_from_file(resource_filename)
    settings = config.Settings(config_filename)
    ret = perform_depseudonymization(resource, settings)
    print(f'CLI Depseudonimize Result={ret}')


@app.command()
def process(resource_filename: str, config_filename: str = typer.Argument("config.yaml")):
    resource = read_resource_from_file(resource_filename)
    settings = config.Settings(config_filename)
    ret = process_data(resource, settings)
    print(f'CLI Process Result={ret}')


if __name__ == "__main__":
    app()
