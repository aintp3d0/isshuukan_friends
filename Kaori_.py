#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# __author__ = 'ames0k0'

import sqlite3
import logging
from os import system, rename
from sys import path
from random import choice
from os.path import exists, dirname
from datetime import datetime
from scripts.db import DataBase


"""
TIME        ->> [ 水曜日2017年11月29日/14時12分56秒 ]
ATR - 著者  ->> 藤宮 香織
TTL - 表題  ->> 学校の屋根の上
DSN - 説明  ->> 友人と一緒に昼食を持っていた「祐樹」、彼は卵のパンを食べました

----- [ NAME ] ---------- [ STR.LOW.IDX +1 ] -----
+ ContextManager            0.3
+ Dict Comprehension        0.4.9
+ DRY                       0.4.18
+ File Manipulation         0.6.9
+ Functional Programming    0.6.21
+ List Comprehension        0.12.9.19.20.3
+ List Slicing              0.12.9.19.20.9
+ Python Stack              0.16
--------------------------------------------------
"""


class CM:

    def __init__(self, fn, message, log):
        logging.basicConfig(filename=log, level=logging.INFO, format='%(message)s')
        self.fn = fn
        self.ins = None
        self.read = None
        self.write = None
        self.message = message

    def __enter__(self):
        self.read = open(self.fn, 'r')
        self.ins = self.read.read()
        self.write = open(self.fn, 'w')
        self.message += self.ins
        self.write.write(self.message)
        return logging

    def __exit__(self, *exp):
        self.read.close()
        self.write.close()


class ParseLog:

    def __init__(self, log, user, koma, dbk):
        self.log = log
        self.user = user
        self.koma = koma
        self.dbk = dbk

    def _all_logs(self):
        with open(self.log, 'r') as file:
            stc = [i for i in file.readlines()]
        return len(stc), stc

    def _log(self):
        stc = self._all_logs()
        for _ in range(stc[0]):
            line = stc[1].pop()
            time = line[:28].strip()
            line = line[28:].strip()
            line = DataBase()._dec(line)
            user = line.split(':>>')[0].strip()
            title = line.split(':>>')[1].split(':')[0].strip()
            description = line.split(':>>')[1].split(':')[1].strip()
            with open(self.dbk, 'a') as _up_file:
                _get_koma = self.koma.format(time, title, description, user)
                _up_file.write(_get_koma)


class DiaryBook:

    def __init__(self):
        self.db = DataBase()
        self.user = None
        self.config = 'user.txt'
        self.daylog = 'dk.log'
        self.daybook = 'daybook.txt'
        self.database = 'scripts/words.db'
        self.koma = "\n+-------------------{}\n|\n| -> {}\n| -> {}\n|\n"
        self.koma += "+-------------------------------------------------------------@{}"
        self.days = ['月曜日','火曜日','水曜日','木曜日','金曜日','土曜日','日曜日']

    def _get_input(self):
        _lambda = lambda x: x.strip().replace(':', '!') 
        _dtitle = input("\nTTL - 表題: ")
        _ddescription = input("DSN - 説明: ")
        title = _lambda(_dtitle or '@TTL-表題@')
        description = _lambda(_ddescription or '@DSN-説明@')
        return title, description

    def _generate_message(self):
        title, description = self._get_input()
        day = self.days[datetime.weekday(datetime.now())]
        time = datetime.today().strftime("[ {}%Y年%m月%d日/%H時%M分%S秒 ]".format(day))
        message = self.koma.format(time, title, description, self.user)
        system('clear')
        print(message+"\n")
        with CM(self.daybook, message, self.daylog) as conmen:
            log = "{} :>> {}: {}".format(self.user, title, description)
            conmen.info("{} {}".format(time, self.db._data(log)))

    def _get_user(self):
        with open(self.config, 'r') as file:
            self.user = file.read()

    def _check_user(self):
        _1st = ["Hajime", "Saki", "Shougo", "Kaori", "Yuuki" ]
        _2nd = ["九条", "山岸 沙希", "桐生 将吾", "藤宮 香織", "長谷 祐樹"]
        persons = {k: f'{k}@-{v}' for k, v in zip(_1st, _2nd)}
        if self.user:
            self._get_user()
        else:
            user = input("\nATR - 著者: ")
            gper = choice(_1st)
            self.user = user or persons[gper]
            with open(self.config, 'w') as file:
                file.write(self.user)

    def _check_exists(self):
        dk = exists(self.daybook)
        dl = exists(self.daylog)
        db = exists(self.database)
        self.user = exists(self.config)
        return dk, dl, db

    def main(self):
        dk, dl, db = self._check_exists()
        if not db:
            raise Exception('DataBase not exists')
        if not dk:
            touch = True
            if dl:
                touch = False
                if self.user:
                    self._get_user()
                    ParseLog(self.daylog, self.user, self.koma, self.daybook)._log()
                else:
                    ParseLog(self.daylog, None, self.koma, self.daybook)._log()
            if touch:
                fn = open(self.daybook, 'w')
                fn.close()
        self._check_user()
        self._generate_message()


if __name__ == '__main__':
    d = DiaryBook()
    d.main()
