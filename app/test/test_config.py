import unittest
from config import Settings
import unittest
from deidentify import perform_deidentification
from depseudonymize import perform_depseudonymization
from pseudonymize import perform_pseudonymization
from cli import deidentify, read_resource_from_file


class TestConfig(unittest.TestCase):
    """
    Testing settings applied to FHIR resources
    """

    def test_read(self):
        settings = Settings()
        self.assertIsNotNone(settings.rules)

    def test_keep(self):
        config_filename = 'test/config/keep.yaml'
        resource_filename = 'test/fhir/simple_patient.json'
        resource = read_resource_from_file(resource_filename)
        settings = Settings(config_filename)
        ret = perform_deidentification(resource, settings)
        self.assertEqual(resource['name']['family'], 'Chalmers')

    def test_deidentify_redact(self):
        config_filename = 'test/config/redact.yaml'
        resource_filename = 'test/fhir/simple_patient.json'
        resource = read_resource_from_file(resource_filename)
        settings = Settings(config_filename)
        ret = perform_deidentification(resource, settings)
        self.assertRaises(KeyError, lambda: resource['name'])

    def test_deidentify_perturb(self):
        config_filename = 'test/config/perturb.yaml'
        resource_filename = 'test/fhir/simple_patient.json'
        resource = read_resource_from_file(resource_filename)
        settings = Settings(config_filename)
        ret = perform_deidentification(resource, settings)
        self.assertFalse(True) # assert the birth date in around the original date

    def test_deidentify_cryptohash(self):
        config_filename = 'test/config/cryptohash.yaml'
        resource_filename = 'test/fhir/simple_patient.json'
        resource = read_resource_from_file(resource_filename)
        settings = Settings(config_filename)
        ret = perform_deidentification(resource, settings)
        # what if the target is a list ? (e.g. patient['name']) 
        self.assertEqual(resource['patient']['id'], 'a1234todotodo') 
    
    def test_deidentify_substitute(self):
        config_filename = 'test/config/substitute.yaml'
        resource_filename = 'test/fhir/simple_patient.json'
        resource = read_resource_from_file(resource_filename)
        settings = Settings(config_filename)
        ret = perform_deidentification(resource, settings)
        self.assertEqual(resource['name']['family'], 'foo')


    def test_pseudonymize_ttp(self):
        config_filename = 'test/config/ttp.yaml'
        resource_filename = 'test/fhir/simple_patient.json'
        resource = read_resource_from_file(resource_filename)
        settings = Settings(config_filename)
        ret = perform_pseudonymization(resource, settings)
        # Under construction
        
    def test_pseudonymize_encrypt(self):
        config_filename = 'test/config/encrypt.yaml'
        resource_filename = 'test/fhir/simple_patient.json'
        resource = read_resource_from_file(resource_filename)
        settings = Settings(config_filename)
        ret = perform_pseudonymization(resource, settings)
        self.assertEqual(resource['name']['family'], 'ENCRYPTED HEX HERE')

    def test_depseudonymize_encrypt(self):
        config_filename = 'test/config/encrypt.yaml'
        resource_filename = 'test/fhir/simple_patient_encrypted.json'
        resource = read_resource_from_file(resource_filename)
        settings = Settings(config_filename)
        ret = perform_deidentification(resource, settings)
        self.assertEqual(resource['name']['family'], 'Chalmers')

if __name__ == '__main__':
    unittest.main()
