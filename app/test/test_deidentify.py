import unittest
from config import Settings
from cli import read_file
from config import Settings
from deidentify import perform_deidentification
import copy


class TestDeidentify(unittest.TestCase):
    def test_redact(self):
        # initial test case
        settings = Settings()
        settings.rules = [
            {'match': "TODO-SELECT-PATIENT-NAME",
             'action': 'redact'}
        ]
        resource = read_file('test/fhir/simple_patient.json')
        print("Resource loaded: ", resource)
        expected = copy.copy(resource)
        del expected['name']  # redact the name attribute
        result = perform_deidentification(resource, settings)
        print(result)
        self.assertDictEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
