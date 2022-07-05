import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator
import sqlalchemy
from src.apis.v1.controllers.user_controller import UsersController
from src.apis.v1.core.project_settings import Settings

# {
#     "firstname": "string",
#     "lastname": "string",
#     "email": "user@example.com",
#     "dr_iq_gender_id":1,
#     "type_of_user": "internal",
#     "is_active":false,
#     "apps": [
#         {
#         "id": 7,
#         "practices": [],
#         "role": {
#                 "id": 1,
#                 "sub_role": null
#             }
            
#         },
#         {
#         "id": 3,
#         "practices": [
#                 {
#                 "id": 337
#                 },
#                 {
#                 "id": 338
#                 },
#                 {
#                 "id": 366
#                 },
#                 {
#                 "id": 374
#                 },
#                 {
#                 "id": 375
#                 },
#                 {
#                 "id": 376
#                 }
#             ],
#         "role": 
#                 {
#                 "id": 4,
#                 "sub_role": 3
#                 }
            
#         }
#     ]
# }
class TestController(unittest.TestCase):
    def setUp(self):
        """ setup test fixtures """
        from controllers import SessionStore
        SQLALCHEMY_DATABASE_URL = Settings.DATABASE_URL
        self.engine = create_engine(SQLALCHEMY_DATABASE_URL)
        session_ = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.db = session_()

    def test_table_exsist(self):
        """ test table exsist """
        # The recommended way to check for existence
        test_table = sqlalchemy.inspect(self.engine).has_table("idp_users")
        self.assertEqual(test_table, True)

    # def test_01_insert(self):
    #     """ test insert """
    #     expected = self.store.set(self.cookie_id,self.user_id)
    #     self.assertEqual(expected, "stored user session")
    #     expected = self.store.set(self.cookie_id,self.user_id)
    #     self.assertEqual(expected, "User already has a session")

    # def test_02_mulitple_insert(self):
    #     """ test multiple insert """
    #     expected = self.store.set(t_list[0]['cookie_id'],t_list[0]['user_id'])
    #     self.assertEqual(expected, "stored user session")
    
    def test_01_get(self):
        """ test get """
        expected_status = UsersController(self.db).get_all_users()
        self.assertEqual(expected_status,200)

    
    def tearDown(self):
        self.db.close()


if __name__ == "__main__":
    unittest.main()