import unittest
from config import Settings
from processor import process_data
from cli import read_resource_from_file
import dateutil.parser as parser
from datetime import timedelta
import copy
import os


class TestProcessor(unittest.TestCase):

    def assertIsFile(self, path):
        if not os.path.isfile(path):
            raise AssertionError("File does not exist: %s" % str(path))

    """
    Testing settings applied to FHIR resources
    """

    def test_multiple_rules(self):
        print(f"======== TEST MULTIPLE RULES ========")
        config_filename = 'test/config/multi_rule.yaml'
        resource_filename = 'test/fhir/patient_R5DB.json'
        resource = read_resource_from_file(resource_filename)
        settings = Settings(config_filename)
        original_resource = copy.deepcopy(resource)
        ret = process_data(resource, settings)
        # Crypto hash checks
        print(f"Checking cryptohash...\t\t", end="", flush=True)
        self.assertEqual(
            ret['name'][0], 'c045ec1db0c14a237341851f8fae21edb1c7d4f36f1e7d49027b9c7a7e06c790')
        self.assertEqual(
            ret['name'][1], '6f4bae1f49ee29890cbfcf8ffb26eccc2520cb543fa30a28458e2952f40b7ea3')
        self.assertEqual(
            ret['name'][2], '96da330ddea4d222d7ae4b074da307520fb8ec00140682831b4b073a6110b8c0')
        print(f"OK")
        # Perturb checks
        print(f"Checking perturb...\t\t", end="", flush=True)
        perturbed_date = parser.parse(ret['birthDate'])
        ref_date = parser.parse('1974-12-25')
        min_date = ref_date - timedelta(days=5)
        max_date = ref_date + timedelta(days=10)
        self.assertTrue(perturbed_date <= max_date)
        self.assertTrue(perturbed_date >= min_date)
        print(f"OK")
        # Encrypt/Decrypt checks
        print(f"Checking encrypt/decrypt...\t", end="", flush=True)
        self.assertEqual(ret['address'][0], original_resource['address'][0])
        print(f"OK")
        # Substitute checks
        print(f"Checking substitute...\t\t", end="", flush=True)
        self.assertEqual(ret['id'], 'foo')
        print(f"OK")

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


if __name__ == '__main__':
    unittest.main()
