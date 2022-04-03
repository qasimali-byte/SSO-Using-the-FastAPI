import unittest
from db.session import SessionLocal, get_db
from storesession import StoreSession

class TestStoreSession(unittest.TestCase):

    def test_store_session(self):
        db = SessionLocal()
        cronjob_controller = StoreSession(db)
        expected = cronjob_controller.set("faisal", "faisal")
        self.assertEqual(expected, "stored user session")
        expected = cronjob_controller.get("faisal")
        self.assertEqual(expected.user_id, "faisal")
        expected = cronjob_controller.delete("faisal")
        self.assertEqual(expected, "deleted user session")

    # def test_unique_session(self):
    #     db = SessionLocal()
    #     cronjob_controller = StoreSession(db)
    #     cronjob_controller.set("faisal", "faisal")
    #     expected = cronjob_controller.get("faisal")
    #     self.assertEqual(expected.user_id, "faisal")

    # def test_get_session(self):
    #     db = SessionLocal()
    #     cronjob_controller = StoreSession(db)
    #     expected = cronjob_controller.set("faisal", "faisal")
    #     expected = cronjob_controller.get("faisal")
    #     self.assertEqual(expected.user_id, "faisal")

    # def test_delete_session(self):
    #     db = SessionLocal()
    #     cronjob_controller = StoreSession(db)
    #     cronjob_controller.delete("faisal")
    #     expected = cronjob_controller.get("faisal")
    #     self.assertEqual(expected, None)

