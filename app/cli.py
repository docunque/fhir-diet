from rich import print
import sys
import os
import json
import typer
import config
from deidentify import perform_deidentification
from depseudonymize import perform_depseudonymization
from pseudonymize import perform_pseudonymization


app = typer.Typer()


def read_file(filename: str):
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
def deidentify(resource_filename: str):
    resource = read_file(resource_filename)
    settings = config.Settings()
    ret = perform_deidentification(resource, settings)
    print(ret)


@app.command()
def pseudonymize(resource_filename: str):
    resource = read_file(resource_filename)
    settings = config.Settings()
    ret = perform_pseudonymization(resource, settings)
    print(ret)


@app.command()
def depseudonymize(resource_filename: str):
    resource = read_file(resource_filename)
    settings = config.Settings()
    ret = perform_depseudonymization(resource, settings)
    return ret


if __name__ == "__main__":
    app()
