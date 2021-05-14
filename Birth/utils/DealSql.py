import sqlite3 as sql


class SqlOp:

    def __init__(self, db):
        self.db = db
        self.conn = None
        self.c = None

    def connect(self):
        self.conn = sql.connect(self.db)
        self.c = self.conn.cursor()

    def closeDB(self):
        self.conn.close()
        self.conn = None
        self.c = None

    def execQuery(self, query):
        result = self.c.execute(query).fetchall()
        return result

    def execNonQuery(self, nonQuery):
        self.c.execute(nonQuery)
        self.conn.commit()

