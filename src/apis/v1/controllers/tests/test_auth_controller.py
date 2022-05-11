import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator
import sqlalchemy

t_list = [
    {
        "cookie_id": "f9a8705b-d09c-4a37-9ad4-6f5d7c6b2798",
        "user_id": "dasd1"
    }
]
class TestController(unittest.TestCase):
    def setUp(self):
        """ setup test fixtures """
        from controllers import SessionStore
        from local_config import Settings
        SQLALCHEMY_DATABASE_URL = Settings.DATABASE_URL
        self.engine = create_engine(SQLALCHEMY_DATABASE_URL)
        session_ = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.db = session_()
        self.store = SessionStore(self.db)
        self.cookie_id = "f8a8705b-d09c-4a37-9ad4-6f5d7c6b2798"
        self.user_id = "dasd"

    def test_table_exsist(self):
        """ test table exsist """
        # The recommended way to check for existence
        test_table = sqlalchemy.inspect(self.engine).has_table("users_session")
        self.assertEqual(test_table, True)
        
    def test_usersession_serializer(self):
        """ test usersession serializer """
        from controllers import SessionController
        expected = SessionController.serialize_usersession(self.cookie_id,self.user_id)
        self.assertEqual(expected[1], True) 

    def test_01_insert(self):
        """ test insert """
        expected = self.store.set(self.cookie_id,self.user_id)
        self.assertEqual(expected, "stored user session")
        expected = self.store.set(self.cookie_id,self.user_id)
        self.assertEqual(expected, "User already has a session")

    def test_02_mulitple_insert(self):
        """ test multiple insert """
        expected = self.store.set(t_list[0]['cookie_id'],t_list[0]['user_id'])
        self.assertEqual(expected, "stored user session")
    
    def test_03_get(self):
        """ test get """
        expected = self.store.get("user_id",self.user_id)
        self.assertEqual(expected.user_id, self.user_id)
        self.assertEqual(expected.id,0) ### test auto incrementing id
        expected = self.store.get("cookie_id_invalid",self.cookie_id)
        self.assertEqual(expected, "Invalid filter key")

    def test_04_update(self):
        """ test update """
        expected = self.store.update("user_id",self.user_id,"cookie_id","f9a8705b-d09c-4a37-9ad4-6f5d7c6b2718")
        self.assertEqual(expected, "updated user session")

    def test_05_delete(self):
        """ test delete """
        expected = self.store.delete("user_id",self.user_id)
        self.assertEqual(expected, "deleted user session")
        expected = self.store.delete("user_id",t_list[0]['user_id'])
        self.assertEqual(expected, "deleted user session")
    
    def tearDown(self):
        self.db.close()


if __name__ == "__main__":
    unittest.main()