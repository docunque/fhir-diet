import typer
from processor import process_data
from utils.util import read_resource_from_file
import config
from rich import print


app = typer.Typer()


@app.command()
def process(resource_filename: str, config_filename: str = typer.Argument("config.yaml")):
    resource = read_resource_from_file(resource_filename)
    settings = config.Settings(config_filename)
    ret = process_data(resource, settings)
    print(f'CLI Process Result={ret}')


if __name__ == "__main__":
    app()
