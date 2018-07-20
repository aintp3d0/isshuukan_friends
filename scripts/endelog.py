#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# __author__ = 'kira@-築城院 真鍳'

from os.path import exists #-------------#
from collections import Counter #--------#


class EndeLog:

    def __init__(self):
        self.parsed = None
        self.nw = None
        self.up = None
        self.re = None

    def _dct(self, dc):  return {k: v for k, v, r in dc}

    def _encode(self, all_words):
        dct = self._dct(all_words)
        encoded = []
        for i in self.parsed:
            try:
                encoded.append(dct[i])
            except KeyError:
                encoded.append(i)
        self.re = "".join(map(str, encoded))

    def _decode(self, data, dct):
        dec = {v: k for k, v, r in dct}
        itm = []
        for word in data.split('∴'):
            if word:
                itm.append(dec[int(word)])
        return " ".join(itm)

    def _parse(self, task, dct):
        nkn = []
        dct = self._dct(dct)
        words = task.split()
        result = []
        for n, i in enumerate(words):
            result.append(i)
            nkn.append(i)
            if n < len(words) - 1:
                result.append('∴')
        new_words = list(filter(bool, map(lambda x: x not in dct.keys() and (x, 1), nkn)))
        upd_rank = list((v, k) for k, v in Counter(map(lambda x: x not in new_words and x, nkn)).items())
        if new_words:
            self.nw = new_words
        if upd_rank:
            self.up = upd_rank
        self.parsed = result
