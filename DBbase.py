import sqlite3
class DBbase:
    def __init__(self, db_name):
        self._db_name = db_name
        self.connect()

    def connect(self):
        self._conn = sqlite3.connect(self._db_name)
        self._cursor = self._conn.cursor()

    def execute_script(self, sql_string):
        self._cursor.executescript(sql_string)

    @property
    def get_connection(self):
        return self._conn
    
    @property
    def get_cursor(self):
        return self._cursor
    
    def reset_database(self):
        raise NotImplementedError("Must implement from the derived class")

    def close_db(self):
        self._conn.close()