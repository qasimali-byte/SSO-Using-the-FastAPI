import unittest
from src.apis.v1.db.session import SessionLocal
from sps_controller import SPSController

class TestSPS(unittest.TestCase):
    def setUp(self):
        db = SessionLocal()
        self.sps = SPSController(db)

    def test_get_sps(self):
        value = self.sps.get()
        self.assertEqual(type(value),list)