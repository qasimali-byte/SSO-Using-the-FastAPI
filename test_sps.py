import unittest
from db.session import SessionLocal, get_db
from sps_controller import SPSController

class TestSPS(unittest.TestCase):
    def setUp(self):
        db = SessionLocal()
        self.sps = SPSController(db)

    def test_get_sps(self):
        value = self.sps.get()
        self.assertEqual(type(value),list)