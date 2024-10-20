import sqlite3


class DataBase:

    def __init__(self, filepath):
        self.conn = sqlite3.connect(filepath)
        self.curr = self.conn.cursor()
        self._create()

    def _create(self):
        self.curr.execute("""CREATE TABLE IF NOT EXISTS dict (word TEXT, id INTEGER PRIMARY KEY, rank INTEGER)""")
        self.curr.execute("""CREATE TABLE IF NOT EXISTS diary (id INTEGER PRIMARY KEY, message TEXT)""")
        self.conn.commit()

    def add_message(self, message):
        self.curr.execute(
            """INSERT INTO diary(message) VALUES (?)""",
            (message,)
        )
        self.conn.commit()

    def get_messages(self):
        fetched = self.curr.execute(
            """SELECT * FROM diary ORDER BY id DESC"""
        )
        for ft in fetched:
            yield ft

    def _add(self, data):
        if data:
            self.curr.executemany("""INSERT INTO dict(word, rank) VALUES (?, ?)""", data)
            self.conn.commit()

    def _update(self, data):
        self.curr.executemany("""UPDATE dict SET rank=rank+? WHERE word=?""", data)
        self.conn.commit()

    def _fetch_all(self):
        fetched = self.curr.execute("""SELECT * FROM dict""")
        for ft in fetched:
            yield ft

