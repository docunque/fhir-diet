import unittest
from config import Settings
from deidentify import perform_deidentification
from depseudonymize import perform_depseudonymization
from pseudonymize import perform_pseudonymization
from cli import deidentify, read_resource_from_file
import dateutil.parser as parser
from datetime import timedelta
import copy
import json


class TestConfig(unittest.TestCase):
    """
    Testing settings applied to FHIR resources
    """

    def test_read_settings(self):
        print(f"=========== TEST READ SETTINGS ===========")
        settings = Settings()
        self.assertIsNotNone(settings.rules)

    def test_read_lists(self):
        print(f"=========== TEST READ LIST ===========")
        config_filename = 'test/config/keep.yaml'
        resource_filename = 'test/fhir/patient_list.json'
        resource = read_resource_from_file(resource_filename)
        original_value = resource['name']
        settings = Settings(config_filename)
        ret = perform_deidentification(resource, settings)
        self.assertEqual(ret['name'], original_value)

    def test_keep(self):
        print(f"=========== TEST KEEP ===========")
        config_filename = 'test/config/keep.yaml'
        resource_filename = 'test/fhir/simple_patient.json'
        resource = read_resource_from_file(resource_filename)
        original_value = resource['name']
        settings = Settings(config_filename)
        ret = perform_deidentification(resource, settings)
        self.assertEqual(ret['name'], original_value)

    def test_deidentify_redact(self):
        print(f"========== TEST REDACT ==========")
        config_filename = 'test/config/redact.yaml'
        resource_filename = 'test/fhir/simple_patient.json'
        resource = read_resource_from_file(resource_filename)
        settings = Settings(config_filename)
        ret = perform_deidentification(resource, settings)
        self.assertRaises(KeyError, lambda: ret['name'])

    def test_deidentify_perturb(self):
        print(f"========== TEST PERTURB =========")
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
        self.assertTrue(perturbed_date <= max_date)
        self.assertTrue(perturbed_date >= min_date)

    def test_deidentify_cryptohash(self):
        print(f"======== TEST CRYPTOHASH ========")
        config_filename = 'test/config/cryptohash.yaml'
        resource_filename = 'test/fhir/simple_patient.json'
        resource = read_resource_from_file(resource_filename)
        settings = Settings(config_filename)
        ret = perform_deidentification(resource, settings)
        # what if the target is a list ? (e.g. patient['name']) ----> for each elem in the list compute the hash;
        #                                                             if the elem is a dict, converts it to a string and hash it
        self.assertEqual(
            ret['name'][0], 'b7340931fb4ee512d5d5f68f6da7a027c5ba8dd8a8d5ea4705416f0b85e1b9ca')
        self.assertEqual(
            ret['name'][1], '6f4bae1f49ee29890cbfcf8ffb26eccc2520cb543fa30a28458e2952f40b7ea3')
        self.assertEqual(
            ret['name'][2], 'dad3235c168df9f3ad295af27f18866e09c4c41009ca555c7706d90474c02626')

    def test_deidentify_substitute(self):
        print(f"======== TEST SUBSTITUTE ========")
        config_filename = 'test/config/substitute.yaml'
        resource_filename = 'test/fhir/simple_patient.json'
        resource = read_resource_from_file(resource_filename)
        settings = Settings(config_filename)
        ret = perform_deidentification(resource, settings)
        self.assertEqual(ret['name'][0]['family'], 'foo')
        self.assertEqual(ret['name'][2]['family'], 'foo')

    # def test_pseudonymize_ttp(self):
    #     print(f"===== TEST PSEUDONYMISE TTP =====")
    #     config_filename = 'test/config/ttp.yaml'
    #     resource_filename = 'test/fhir/simple_patient.json'
    #     resource = read_resource_from_file(resource_filename)
    #     settings = Settings(config_filename)
    #     ret = perform_pseudonymization(resource, settings)
    #     # Under construction

    def test_pseudonymize_encrypt(self):
        print(f"=== TEST PSEUDONYMIZE/DEPSEUDONYMIZE ENCRYPT ===")
        config_filename = 'test/config/encrypt.yaml'
        resource_filename = 'test/fhir/simple_patient.json'
        resource = read_resource_from_file(resource_filename)
        settings = Settings(config_filename)
        original_resource = copy.deepcopy(resource)
        ret = perform_pseudonymization(resource, settings)
        #config_filename = 'test/config/encrypt.yaml'
        #settings = Settings(config_filename)
        ret2 = perform_depseudonymization(ret, settings)
        #dec_names = [ json.loads(rsa_decrypt(bytes.fromhex(name), settings.rules[0]['params']).decode('utf-8')) for name in resource['name']]
        self.assertEqual(ret2['name'][0], original_resource['name'][0])
        self.assertEqual(ret2['name'][1], original_resource['name'][1])
        self.assertEqual(ret2['name'][2], original_resource['name'][2])

    # def test_depseudonymize_decrypt(self):
    #     print(f"=== TEST DEPSEUDONYMISE DECRYPT ===")
    #     config_filename = 'test/config/decrypt.yaml'
    #     resource_filename = 'test/fhir/simple_patient.json'
    #     enc_resource_filename = 'test/fhir/enc_simple_patient.json'
    #     resource = read_resource_from_file(resource_filename)
    #     enc_resource = read_resource_from_file(enc_resource_filename)
    #     settings = Settings(config_filename)
    #     ret = perform_depseudonymization(enc_resource, settings)
    #     self.assertEqual(enc_resource['name'][0], resource['name'][0])
    #     self.assertEqual(enc_resource['name'][1], resource['name'][1])
    #     self.assertEqual(enc_resource['name'][2], resource['name'][2])

    def test_depseudonymize_decrypt(self):
        print(f"=== TEST SAFE HARBOUR REDACT ===")
        config_filename = 'test/config/safe_harbour_redact.yaml'
        resource_filename = 'test/fhir/patient_R5DB.json'
        resource = read_resource_from_file(resource_filename)
        settings = Settings(config_filename)
        ret = perform_deidentification(resource, settings)
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


if __name__ == '__main__':
    unittest.main()
