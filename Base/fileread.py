import re

dictionary = dict()
words = dict()
phrases = list()
groups = dict()
clusters = list()

for s in open('word', 'r+'):
    if s[-1] == '\n':
        s = s[:-1]
    p, ws = re.split('\d+', s, 1)
    tune = s[len(p)]
    p = p.lower()
    if tune == '5':
        tune = '0'
    if p not in dictionary.keys():
        dictionary[p] = dict()
    dictionary[p][tune] = ws

    for w in ws:
        if w not in words.keys():
            words[w] = list()
        words[w].append(dict(
            p=p,
            t=tune,
        ))

for s in open('phrase', 'r+'):
    if s[-1] == '\n':
        s = s[:-1]
    phrases.append(s)

for s in open('group', 'r+'):
    if s[-1] == '\n':
        s = s[:-1]
    g = s.lower().split(' ')
    groups[g[0]] = g[1:]

for s in open('cluster', 'r+'):
    if s[-1] == '\n':
        s = s[:-1]


# print(dictionary)
# print(words)
# print(groups)
