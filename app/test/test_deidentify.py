import unittest
from config import Settings
from cli import read_file
from config import Settings
from deidentify import perform_deidentification


class TestDeidentify(unittest.TestCase):
    def test_initial(self):
        # initial test case
        settings = Settings()
        resource = read_file('test/fhir/simple_patient.json')
        print("Resource loaded: ", resource)
        ret = perform_deidentification(resource, settings)
        print(ret)


if __name__ == '__main__':
    unittest.main()
