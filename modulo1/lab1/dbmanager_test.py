# https://www.psycopg.org/docs/extensions.html#connection-status-constants
# python -m unittest dbmanager_test.py
import unittest
from dbmanager import DBManager

class DBManagerTest(unittest.TestCase):
    def test_an_object_instanced_from_dbmanager (self):
        m_dbmanager = DBManager()
        expected = 'insights_python' 
        self.assertEqual(m_dbmanager.db.dbname, expected)