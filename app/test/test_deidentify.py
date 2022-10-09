import unittest
from config import Settings
from cli import read_resource_from_file
from config import Settings
from deidentify import perform_deidentification
from Crypto.Hash import SHA3_256
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import copy
import json


class TestDeidentify(unittest.TestCase):

    global infile
    infile = 'test/fhir/simple_patient.json'
    
    def test_redact1(self):
        print(f"========== TEST REDACT ==========")
        # initial test case
        settings = Settings()
        settings.rules = [
            {'match': "Patient.name",
             'action': 'redact',
             'params': {}}
        ]
        resource = read_resource_from_file(infile)
        #print(f"Resource loaded: {resource}")
        expected = copy.deepcopy(resource)
        del expected['name']
        print(f"\nExpected: {expected}\n")
        result = perform_deidentification(resource, settings)
        print(f"Actual: {result}\n\n\n\n")
        self.assertDictEqual(expected, result)

    def test_cryptoHash1(self):
        print(f"======== TEST CRYPTOHASH ========")
        # initial test case
        settings = Settings()
        settings.rules = [
            {'match': "Patient.id",
             'action': 'cryptoHash',
             'params': {}}
        ]
        resource = read_resource_from_file(infile)
        #print(f"Resource loaded: {resource}")
        expected = copy.deepcopy(resource)
        hash_str = SHA3_256.new(expected['id'].encode()).hexdigest()
        expected['id'] = hash_str
        print(f"\nExpected: {expected}\n")
        result = perform_deidentification(resource, settings)
        print(f"Actual: {result}\n\n\n\n")
        self.assertDictEqual(expected, result)

    def test_keep1(self):
        print(f"=========== TEST KEEP ===========")
        # initial test case
        settings = Settings()
        settings.rules = [
            {'match': "Patient",
             'action': 'keep',
             'params': {}}
        ]
        resource = read_resource_from_file(infile)
        #print(f"Resource loaded: {resource}")
        expected = copy.deepcopy(resource)
        print(f"\nExpected: {expected}\n")
        result = perform_deidentification(resource, settings)
        print(f"Actual: {result}\n\n\n\n")
        self.assertDictEqual(expected, result)

    def test_substitute1(self):
        print(f"======== TEST SUBSTITUTE ========")
        # initial test case
        new_val = 'newID'
        settings = Settings()
        settings.rules = [
            {'match': "Patient.id",
             'action': 'substitute',
             'params': {
                'new_value': new_val
             }}
        ]
        resource = read_resource_from_file(infile)
        #print(f"Resource loaded: {resource}")
        expected = copy.deepcopy(resource)
        expected['id'] = new_val
        print(f"\nExpected: {expected}\n")
        result = perform_deidentification(resource, settings)
        print(f"Actual: {result}\n\n\n\n")
        self.assertDictEqual(expected, result)

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

    def test_perturb1(self):
        print(f"=========== TEST PERTURB ==========")
        noise = 10.2
        # initial test case
        settings = Settings()
        settings.rules = [
            {'match': "Patient.ttl",
             'action': 'perturb',
             'params': {
                'noise': noise
             }}
        ]
        resource = read_resource_from_file(infile)
        #print(f"Resource loaded: {resource}")
        expected = copy.deepcopy(resource)
        expected['ttl'] += noise
        print(f"\nExpected: {expected}\n")
        result = perform_deidentification(resource, settings)
        print(f"Actual: {result}\n\n\n\n")
        self.assertDictEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
