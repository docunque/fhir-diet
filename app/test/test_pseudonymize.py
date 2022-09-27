import unittest
from config import Settings
from cli import read_file
from config import Settings
from deidentify import perform_deidentification
from Crypto.Hash import SHA3_256
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import copy
import json


class TestPseudonymize(unittest.TestCase):
    def test_pseudo1(self):
        pass