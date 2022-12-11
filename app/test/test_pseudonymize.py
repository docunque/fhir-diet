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

    def test_pseudonymize_encrypt(self):
        print(f"=== TEST PSEUDONYMIZE/DEPSEUDONYMIZE ENCRYPT ===")
        config_filename = 'test/config/encrypt.yaml'
        resource_filename = 'test/fhir/simple_patient.json'
        resource = read_resource_from_file(resource_filename)
        settings = Settings(config_filename)
        original_resource = copy.deepcopy(resource)
        #ret = perform_pseudonymization(resource, settings)
        ret = process_data(resource, settings)
        config_filename = 'test/config/decrypt.yaml'
        settings = Settings(config_filename)
        #ret2 = perform_depseudonymization(ret, settings)
        ret2 = process_data(ret, settings)
        #dec_names = [ json.loads(rsa_decrypt(bytes.fromhex(name), settings.rules[0]['params']).decode('utf-8')) for name in resource['name']]
        self.assertEqual(ret2['name'][0], original_resource['name'][0])
        self.assertEqual(ret2['name'][1], original_resource['name'][1])
        self.assertEqual(ret2['name'][2], original_resource['name'][2])


    def test_depseudonymize_decrypt(self):
        print(f"=== TEST SAFE HARBOUR REDACT ===")
        config_filename = 'test/config/safe_harbour_redact.yaml'
        resource_filename = 'test/fhir/patient_R5DB.json'
        resource = read_resource_from_file(resource_filename)
        settings = Settings(config_filename)
        #ret = perform_deidentification(resource, settings)
        ret = process_data(resource, settings)
        #print(f'RET={ret}')
        self.assertRaises(KeyError, lambda: ret['name'])
        self.assertRaises(KeyError, lambda: ret['contact'][0]['name'])
        self.assertRaises(KeyError, lambda: ret['address'][0]['text'])
        self.assertRaises(KeyError, lambda: ret['address'][0]['line'])
        self.assertRaises(KeyError, lambda: ret['address'][0]['city'])
        self.assertRaises(KeyError, lambda: ret['address'][0]['district'])
        self.assertRaises(KeyError, lambda: ret['address'][0]['postalCode'])
        self.assertRaises(
            KeyError, lambda: ret['contact'][0]['address']['line'])
        self.assertRaises(
            KeyError, lambda: ret['contact'][0]['address']['city'])
        self.assertRaises(
            KeyError, lambda: ret['contact'][0]['address']['district'])
        self.assertRaises(
            KeyError, lambda: ret['contact'][0]['address']['postalCode'])
        self.assertRaises(KeyError, lambda: ret['birthDate'])
        self.assertRaises(
            KeyError, lambda: ret['_birthDate']['extension'][0]['valueDateTime'])
        self.assertRaises(
            KeyError, lambda: ret['address'][0]['period']['start'])
        self.assertRaises(
            KeyError, lambda: ret['contact'][0]['address']['period']['start'])
        self.assertRaises(KeyError, lambda: ret['telecom'][0]['value'])
        self.assertRaises(
            KeyError, lambda: ret['contact'][0]['telecom'][0]['value'])
