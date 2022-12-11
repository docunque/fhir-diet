import unittest
from config import Settings
from cli import read_resource_from_file
from config import Settings
from deidentify import perform_deidentification
from Crypto.Hash import SHA3_256
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from processor import process_data
import copy
import os
import json


class TestPseudonymize(unittest.TestCase):
    global infile
    infile = 'test/fhir/simple_patient.json'

    def assertIsFile(self, path):
        if not os.path.isfile(path):
            raise AssertionError("File does not exist: %s" % str(path))

    def test_ttp_rules(self):
        print(f"======== TEST TTP RULES ========")
        # List generation checks
        list_outfile = 'test/pseudonymization/list.csv'
        if os.path.isfile(list_outfile):
            os.remove(list_outfile)
        list_config_filename = 'test/config/ttp_gen_list.yaml'
        list_settings = Settings(list_config_filename)
        pseudo_config_filename = 'test/config/ttp_pseudonymize.yaml'
        pseudo_settings = Settings(pseudo_config_filename)
        depseudo_config_filename = 'test/config/ttp_depseudonymize.yaml'
        depseudo_settings = Settings(depseudo_config_filename)
        resource_filename = 'test/fhir/patient_R5DB.json'
        resource = read_resource_from_file(resource_filename)
        ret = process_data(resource, list_settings)
        print(f"Checking TTP list generation...\t\t", end="", flush=True)
        self.assertIsFile(list_outfile)
        print(f"OK")
        # Pseudonym application checks
        original_resource = copy.deepcopy(ret)
        ret = process_data(ret, pseudo_settings)
        print(f"Checking TTP pseudonymization...\t", end="", flush=True)
        self.assertEqual(
            ret['name'][0]['family'], 'Cha2')
        self.assertEqual(
            ret['name'][2]['family'], 'Win5')
        print(f"OK")
        # Depseudonym application checks
        ret = process_data(ret, depseudo_settings)
        print(f"Checking TTP depseudonymization...\t", end="", flush=True)
        self.assertEqual(
            ret['name'][0]['family'], original_resource['name'][0]['family'])
        self.assertEqual(
            ret['name'][2]['family'], original_resource['name'][2]['family'])
        print(f"OK")

    def test_encrypt1(self):
        print(f"========= TEST ENCRYPT =========")
        # initial test case
        key = get_random_bytes(16)
        nonce = get_random_bytes(12)
        settings = Settings()
        settings.rules = [
            {'match': "Patient.id",
             'action': 'encrypt',
             'params': {
                'key': key,
                'nonce': nonce
             }}
        ]
        resource = read_resource_from_file(infile)
        #print(f"Resource loaded: {resource}")
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        ciphertext, tag = cipher.encrypt_and_digest(resource['id'].encode())
        enc_str = { 'ciphertext': ciphertext, 'tag': tag }
        expected = copy.deepcopy(resource)
        expected['id'] = enc_str
        print(f"\nExpected: {expected}\n")
        result = perform_deidentification(resource, settings)
        print(f"Actual: {result}\n\n\n\n")
        self.assertDictEqual(expected, result)