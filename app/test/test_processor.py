import unittest
from config import Settings
from processor import process_data
from utils.util import read_resource_from_file
import dateutil.parser as parser
from datetime import timedelta
import copy
from rich import print


class TestProcessor(unittest.TestCase):
    """
    Testing settings applied to FHIR resources
    """

    def test_multiple_rules(self):
        print(f"======== TEST MULTIPLE RULES ========")
        config_filename = 'test/config/multi_rule.yaml'
        resource_filename = 'test/sample_fhir_data/patient_R5DB.json'
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
        print(f":thumbs_up:")
        # Perturb checks
        print(f"Checking perturb...\t\t", end="", flush=True)
        perturbed_date = parser.parse(ret['birthDate'])
        ref_date = parser.parse('1974-12-25')
        min_date = ref_date - timedelta(days=5)
        max_date = ref_date + timedelta(days=10)
        self.assertTrue(perturbed_date <= max_date)
        self.assertTrue(perturbed_date >= min_date)
        print(f":thumbs_up:")
        # Encrypt/Decrypt checks
        print(f"Checking encrypt/decrypt...\t", end="", flush=True)
        self.assertEqual(ret['address'][0], original_resource['address'][0])
        print(f":thumbs_up:")
        # Substitute checks
        print(f"Checking substitute...\t\t", end="", flush=True)
        self.assertEqual(ret['id'], 'foo')
        print(f":thumbs_up:")

    


if __name__ == '__main__':
    unittest.main()
