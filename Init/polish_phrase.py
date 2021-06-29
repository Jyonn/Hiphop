import codecs
import os

import pypinyin

from Hiphop.settings import BASE_DIR

CRT_PATH = os.path.join(BASE_DIR, 'Init')

with codecs.open(os.path.join(CRT_PATH, 'phrase_raw'), 'r+', encoding='utf8') as f:
    phrases = f.readlines()
    phrases = list(map(lambda x: x[:-1], phrases))
    phrases = list(filter(lambda x: x, phrases))
    phrases.sort()


    def py_func(phrase):
        py = pypinyin.pinyin(phrase, style=pypinyin.Style.NORMAL, errors='ignore')
        count = 0
        for c in phrase:
            if c in '，“”・…、':
                count += 1
        return len(py) + count == len(phrase)
    phrases = list(filter(py_func, phrases))

last = None
with open(os.path.join(CRT_PATH, 'phrase'), 'wb+') as f:
    for s in phrases:
        if s == last:
            continue
        last = s
        f.write((s+'\n').encode())

