import unittest
from config import Settings
import unittest
from deidentify import perform_deidentification
from depseudonymize import perform_depseudonymization
from pseudonymize import perform_pseudonymization
from cli import deidentify, read_resource_from_file
import dateutil.parser as parser
from datetime import timedelta

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
        resource_filename = 'test/fhir/patient_R5DB.json'
        resource = read_resource_from_file(resource_filename)
        settings = Settings(config_filename)
        ret = perform_deidentification(resource, settings)
        # check if the perturbation is in the stated range
        perturbed_date = parser.parse(ret['birthDate'])
        ref_date = parser.parse('1974-12-25')
        min_date = ref_date - timedelta(days=5)
        max_date = ref_date + timedelta(days=10)
        self.assertTrue(perturbed_date < max_date)
        self.assertTrue(perturbed_date > min_date)

    def test_deidentify_cryptohash(self):
        config_filename = 'test/config/cryptohash.yaml'
        resource_filename = 'test/fhir/simple_patient.json'
        resource = read_resource_from_file(resource_filename)
        settings = Settings(config_filename)
        ret = perform_deidentification(resource, settings)
        # what if the target is a list ? (e.g. patient['name']) 
        self.assertEqual(ret['patient']['id'], 'a1234todotodo') 
    
    def test_deidentify_substitute(self):
        config_filename = 'test/config/substitute.yaml'
        resource_filename = 'test/fhir/simple_patient.json'
        resource = read_resource_from_file(resource_filename)
        settings = Settings(config_filename)
        ret = perform_deidentification(resource, settings)
        self.assertEqual(ret['name']['family'], 'foo')


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
        self.assertEqual(ret['name']['family'], 'ENCRYPTED HEX HERE')

    def test_depseudonymize_encrypt(self):
        config_filename = 'test/config/encrypt.yaml'
        resource_filename = 'test/fhir/simple_patient_encrypted.json'
        resource = read_resource_from_file(resource_filename)
        settings = Settings(config_filename)
        ret = perform_deidentification(resource, settings)
        self.assertEqual(ret['name']['family'], 'Chalmers')

if __name__ == '__main__':
    unittest.main()
