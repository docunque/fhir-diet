import unittest
from config import Settings
from cli import read_file
from config import Settings
from deidentify import perform_deidentification
from hashlib import sha3_256
import copy


class TestDeidentify(unittest.TestCase):
    def test_redact1(self):
        # initial test case
        settings = Settings()
        settings.rules = [
            {'match': "Patient.name",
             'action': 'redact'}
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
             'action': 'cryptoHash'}
        ]
        resource = read_file('test/fhir/simple_patient.json')
        print(f"Resource loaded: {resource}")
        hash_str = sha3_256(resource['id'].encode()).hexdigest()
        expected = copy.deepcopy(resource)
        expected['id'] = hash_str # redact the name attribute
        print(f"Expected: {expected}")
        result = perform_deidentification(resource, settings)
        print(f"Actual: {result}")
        self.assertDictEqual(expected, result)

if __name__ == '__main__':
    unittest.main()
