#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# __author__ = 'kira@-築城院 真鍳

import sqlite3
from .endelog import EndeLog


class DataBase:

    def __init__(self):
        self.db = 'scripts/words.db'
        self.endelog = EndeLog()
        self.conn = sqlite3.connect(self.db)
        self.curr = self.conn.cursor()
        self._create()

    def _data(self, data):
        self.endelog._parse(data, self._fetch_all())
        self._add(self.endelog.nw)
        self._update(self.endelog.up)
        self.endelog._encode(self._fetch_all())
        self.conn.close()
        return self.endelog.re

    def _dec(self, task):
        deco = self.endelog._decode(task, self._fetch_all())
        self.conn.close()
        return deco

    def _create(self):
        self.curr.execute("""CREATE TABLE IF NOT EXISTS dict (word TEXT, id INTEGER PRIMARY KEY, rank INTEGER)""")
        self.conn.commit()

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

