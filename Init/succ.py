import codecs
import pypinyin

with codecs.open('phrase', 'r', encoding='utf8') as f:
    phrases = f.readlines()
    phrases = list(map(lambda x: x[:-1], phrases))
    phrases = list(filter(lambda x: len(x) >= 3, phrases))
    phrases = list(map(lambda s: ''.join(filter(lambda c: c not in '，“”・…、', s)), phrases))
    phrases.sort(key=len)


def py_func(phrase):
    py = pypinyin.pinyin(phrase, style=pypinyin.Style.NORMAL, errors='ignore')
    if len(py) < len(phrase):
        return None
    return list(map(lambda x: x[0], py))


pys = list(map(py_func, phrases))
#
# with open('result', 'wb+') as f:
#     for i in range(len(phrases)):
#         if not pys[i]:
#             continue
#         if i % 200 == 0:
#             print(i, len(phrases))
#         for j in range(i+1, len(phrases)):
#             if pys[j] and pys[i][-1] == pys[j][1] and pys[i][-2] == pys[j][0]:
#                 f.write(('%s %s\n' % (phrases[i], phrases[j])).encode())

flags = [False] * len(phrases)

with open('same_char', 'wb+') as f:
    for i in range(len(phrases)):
        if i % 200 == 0:
            print('%s/%s' % (i, len(phrases)))

        if flags[i]:
            continue

        title = phrases[i]
        fit = ''
        find = False

        for j in range(i+1, len(phrases)):
            if phrases[i][-2:] == phrases[j][-2:]:
                flags[j] = True
                find = True
                title += ' ' + phrases[j]
            if phrases[i][-2:] == phrases[j][:2]:
                fit += ' ' + phrases[j]

        if fit and not find:
            f.write((title+'\n').encode())
            f.write((fit[1:]+'\n\n').encode())
