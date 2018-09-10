import codecs
import os

from Hiphop.settings import BASE_DIR

CRT_PATH = os.path.join(BASE_DIR, 'Init')

with open(os.path.join(CRT_PATH, 'phrase'), 'wb+') as f:
    for s in codecs.open(os.path.join(CRT_PATH, 'phrase_raw'), 'r+', encoding='utf8'):
        if s[-1] == '\n':
            s = s[:-1]
        flag = True
        for c in s:
            if c.upper() in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()~{}[]`1234567890-=_+?<>,.;:\"\'':
                flag = False
        if flag:
            f.write((s+'\n').encode())
