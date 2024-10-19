#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# __author__ = "ames0k0"

import argparse
from random import choice
from pathlib import Path
from datetime import datetime

from scripts.db import DataBase


DATA_DIR = Path('data')

WEEKDAY_NAME = [
    '月曜日', '火曜日', '水曜日', '木曜日', '金曜日', '土曜日', '日曜日'
]
DATETIME_FMT = (
    "[ {}%Y年%m月%d日 / %H時%M分%S秒 ]".format(
        WEEKDAY_NAME[
            datetime.now().weekday()
        ]
    )
)

FIRST_NAME = ["Hajime", "Saki", "Shougo", "Kaori", "Yuuki"]
FULL_NAME = ["九条", "山岸 沙希", "桐生 将吾", "藤宮 香織", "長谷 祐樹"]

CHARACTERS = {
    k: f'{k}@-{v}' for k, v in zip(FIRST_NAME, FULL_NAME)
}


class CM:

    def __init__(self, fn, message):
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

    def __exit__(self, *exp):
        self.read.close()
        self.write.close()


class Koma:
    MESSAGE = ""

    def add_time(self, time):
        self.MESSAGE += f"\n+-------------------{time}\n|\n"

    def add_title(self, title):
        self.MESSAGE += f"| -> {title}\n"

    def add_multiline_descriptions(
            self, multiline_descriptions, new_line_symbol: str = "\n"
    ):
        for idx, description in enumerate(multiline_descriptions):
            if not idx:
                self.MESSAGE += f"| -> {description}\n"
                continue
            if description == new_line_symbol:
                self.MESSAGE += f"|\n"
                continue
            self.MESSAGE += f"|    {description}\n"

    def add_user(self, user):
        self.MESSAGE += f"|\n+-------------------------------------------------------------@{user}\n"

    def get_message(self):
        return self.MESSAGE


class DiaryBook:
    __slots__ = (
        "user", "config",
        "daybook", "database",
        "koma", "db"
    )

    def __init__(self, user):
        self.user = user
        self.config = DATA_DIR / 'user.txt'
        self.daybook = Path('daybook.txt')
        self.db = DataBase(DATA_DIR / 'words.db')
        self.koma = Koma()

    @staticmethod
    def replace_symbols(target: str) -> str:
        return target.strip().replace(':', '!')

    def get_multiline_description(self, new_line_symbol: str = "\n"):
        """Multiline description
        """
        multiline = []
        break_in_count = 3

        while True:
            description = input("DSN - 説明: ")
            if description:
                description = self.replace_symbols(description)
                break_in_count = 3
            else:
                description = new_line_symbol
                break_in_count -= 1
            if not break_in_count:
                break
            multiline.append(description)

        # pop right
        while True:
            if not multiline:
                break
            if multiline[0] != new_line_symbol:
                break
            multiline.pop(0)

        # pop left
        while True:
            if not multiline:
                break
            if multiline[-1] != new_line_symbol:
                break
            multiline.pop()

        return multiline

    def get_user_input(self):
        """Getting the user input
        """
        title = input("\nTTL - 表題: ")
        title = self.replace_symbols(title)
        if not title:
            title = "@TTL-表題@"

        multiline_descriptions = self.get_multiline_description()
        if not multiline_descriptions:
            multiline_descriptions = ["@DSN-説明@"]

        return title, multiline_descriptions

    def generate_message(self):
        title, multiline_descriptions = self.get_user_input()
        time = datetime.today().strftime(DATETIME_FMT)

        self.koma.add_time(time)
        self.koma.add_title(title)
        self.koma.add_multiline_descriptions(multiline_descriptions)
        self.koma.add_user(self.user)

        message = self.koma.get_message()

        print(message)

        with CM(self.daybook, message):
            return None

    def _get_user(self):
        with open(self.config, 'r') as file:
            self.user = file.read()

    def _set_user(self):
        with open(self.config, 'w') as file:
            file.write(self.user)

    def _check_user(self):
        # TODO: make `user` as setter
        if self.user:
            self._get_user()
            return None

        user = input("\nATR - 著者: ")
        user = user.strip()
        if user:
            self.user = user
            self._set_user()
            return None

        self.user = CHARACTERS[
            choice(FIRST_NAME)
        ]
        self._set_user()

    def _check_exists(self):
        dk = self.daybook.exists()
        # passed via argument
        if self.user:
            self._set_user()
        else:
            self.user = self.config.exists()
        return dk

    def main(self):
        dk = self._check_exists()
        if not dk:
            self.daybook.touch()
        self._check_user()
        self.generate_message()


if __name__ == '__main__':
    if not DATA_DIR.exists():
        DATA_DIR.mkdir()

    parser = argparse.ArgumentParser(description='Set a new ATR (Author)')
    parser.add_argument('--atr', help='Set new ATR')

    args = parser.parse_args()

    d = DiaryBook(args.atr)
    try:
        d.main()
    except KeyboardInterrupt:
        pass
