from rich import print
import sys
import os
import json
import typer
import config

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
    print(f"Hello {resource_filename}")


@app.command()
def pseudonymize(resource_filename: str):
    resource = read_file(resource_filename)
    settings = config.Settings()
    print(f"Hello {resource_filename}")


@app.command()
def depseudonymize(resource_filename: str):
    resource = read_file(resource_filename)
    settings = config.Settings()
    print(f"Hello {resource_filename}")


if __name__ == "__main__":
    app()
