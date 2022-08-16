import unittest
from config import Settings


class TestConfig(unittest.TestCase):
    def test_read(self):
        settings = Settings()
        self.assertIsNotNone(settings.rules)


if __name__ == '__main__':
    unittest.main()
