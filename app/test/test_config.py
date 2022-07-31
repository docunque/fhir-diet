import unittest
from main import read_config


class TestConfig(unittest.TestCase):
    def test_read(self):
        data = read_config()
        self.assertIsNotNone(data)
        #self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")


if __name__ == '__main__':
    unittest.main()
