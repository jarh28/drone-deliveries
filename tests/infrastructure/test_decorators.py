import unittest
from infrastructure.decorators import sqlite_connection_handler
from sqlite3 import Connection, ProgrammingError
from config import DATABASE_CONNECTION_STRING

class SQLiteConnectionHandlerTestCase(unittest.TestCase):
    def setUp(self):
        @sqlite_connection_handler(DATABASE_CONNECTION_STRING)
        def query_medications(conn: Connection):
            output = conn.execute("SELECT * FROM medications").fetchall()
            return output, conn                
        self.query_medications = query_medications
    
    def test_sqlite_connection_handler(self):
        expected_output = [('6bf4e4b9-6406-4594-8030-87d7ec3c37e3', '30df78ec-0532-4067-855e-79644bfcc48f', 'Paracetamol', 200.0, 'XYZ_10450', None)]
        output, conn = self.query_medications()   
        if len(output) != 1:
            output = [output[0]]
        self.assertListEqual(output, expected_output)

        with self.assertRaises(ProgrammingError):
            conn.execute("SELECT * FROM medications")


if __name__ == '__main__':
    unittest.main()