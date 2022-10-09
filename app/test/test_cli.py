import unittest
from config import Settings


class TestCli(unittest.TestCase):
    """
    Testing the Command Line Interface
    """
    def test_deidentify1(self):
        #resource = read_file("fhir/config/deidentify1.yml")
        #settings = config.Settings()
        #ret = perform_deidentification(resource, settings)
        #print(ret)
        #self.assertIsNotNone(settings.rules)
        from cli import read_resource_from_file
        print("ciao")


if __name__ == '__main__':
    unittest.main()