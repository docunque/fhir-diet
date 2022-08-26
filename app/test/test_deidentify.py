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


class TestDeidentify(unittest.TestCase):
    def test_redact1(self):
        # initial test case
        settings = Settings()
        settings.rules = [
            {'match': "Patient.name",
             'action': 'redact',
             'params': {}}
        ]
        resource = read_file('test/fhir/simple_patient.json')
        print(f"Resource loaded: {resource}")
        expected = copy.deepcopy(resource)
        del expected['name']  # redact the name attribute
        print(f"Expected: {expected}")
        result = perform_deidentification(resource, settings)
        print(f"Actual: {result}")
        self.assertDictEqual(expected, result)

    def test_cryptoHash1(self):
        # initial test case
        settings = Settings()
        settings.rules = [
            {'match': "Patient.id",
             'action': 'cryptoHash',
             'params': {}}
        ]
        resource = read_file('test/fhir/simple_patient.json')
        print(f"Resource loaded: {resource}")
        expected = copy.deepcopy(resource)
        hash_str = SHA3_256.new(expected['id'].encode()).hexdigest()
        expected['id'] = hash_str # redact the name attribute
        print(f"Expected: {expected}")
        result = perform_deidentification(resource, settings)
        print(f"Actual: {result}")
        self.assertDictEqual(expected, result)

    def test_keep1(self):
        # initial test case
        settings = Settings()
        settings.rules = [
            {'match': "Patient",
             'action': 'keep',
             'params': {}}
        ]
        resource = read_file('test/fhir/simple_patient.json')
        print(f"Resource loaded: {resource}")
        expected = copy.deepcopy(resource)
        print(f"Expected: {expected}")
        result = perform_deidentification(resource, settings)
        print(f"Actual: {result}")
        self.assertDictEqual(expected, result)

    def test_substitute1(self):
        # initial test case
        settings = Settings()
        settings.rules = [
            {'match': "Patient.id",
             'action': 'substitute',
             'params': {
                'new_value': 'newID'
             }}
        ]
        resource = read_file('test/fhir/simple_patient.json')
        print(f"Resource loaded: {resource}")
        expected = copy.deepcopy(resource)
        expected['id'] = 'newID'
        print(f"Expected: {expected}")
        result = perform_deidentification(resource, settings)
        print(f"Actual: {result}")
        self.assertDictEqual(expected, result)

    def test_encrypt1(self):
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
        resource = read_file('test/fhir/simple_patient.json')
        print(f"Resource loaded: {resource}")
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        ciphertext, tag = cipher.encrypt_and_digest(resource['id'].encode())
        enc_str = { 'ciphertext': ciphertext, 'tag': tag }
        expected = copy.deepcopy(resource)
        expected['id'] = enc_str # redact the name attribute
        print(f"Expected: {expected}")
        result = perform_deidentification(resource, settings)
        print(f"Actual: {result}")
        self.assertDictEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
