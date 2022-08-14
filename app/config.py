import yaml
import sys
import os
from rich import print


class Settings():
    def __init__(self):
        self.parse("config.yaml")

    def parse(self, filename):
        try:
            with open(filename, "r") as ymlfile:
                cfg = yaml.safe_load(ymlfile)
                print(f":thumbs_up: settings loaded")
        except IOError as e:
            print(
                f":sad_but_relieved_face: Settings file {filename} does not exist.")
            print(e)
            sys.exit(os.EX_OSFILE)
        except yaml.YAMLError as e:
            print(
                f":sad_but_relieved_face: Cannot parse settings yaml data.")
            print(e)
            sys.exit(os.EX_OSFILE)
