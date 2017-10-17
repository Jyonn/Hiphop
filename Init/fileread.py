import re

import os

from Base.error import Error
from Base.response import Ret
from Hiphop.settings import BASE_DIR

dictionary = dict()
words = dict()
phrases = list()
groups = dict()
clusters = dict()
CRT_PATH = os.path.join(BASE_DIR, 'Init')

for s in open(os.path.join(CRT_PATH, 'word'), 'r+'):
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

for s in open(os.path.join(CRT_PATH, 'phrase'), 'r+'):
    if s[-1] == '\n':
        s = s[:-1]
    phrases.append(s)

for s in open(os.path.join(CRT_PATH, 'group'), 'r+'):
    if s[-1] == '\n':
        s = s[:-1]
    g = s.lower().split(' ')
    # groups[g[0]] = g[1:]
    for p in g[1:]:
        groups[p] = g[0]

cluster_free = True
cluster_name = ''
for s in open(os.path.join(CRT_PATH, 'cluster'), 'r+'):
    if s[-1] == '\n':
        s = s[:-1]
    if cluster_free:
        match = re.search('\[CLUSTER-(.*?)\]', s)
        if match:
            cluster_name = match.group(1).upper()
            cluster_free = False
    else:
        cluster_free = True
        clusters[cluster_name] = list()
        cluster = s.split(';')
        for c in cluster:
            group_list = c.split(',')
            clusters[cluster_name].append(group_list)


def match(o_phrase, cluster=clusters['NORMAL'], min_max_match=0, phrase_len=0):
    """
    词语匹配
    :param phrase_len: 匹配的词语长度 0 表示所有长度
    :param min_max_match: 最小匹配的最大长度 -1 表示所能达到的最大长度
    :param o_phrase: 拼音列表 如羽毛球 则 qiu2 mao2 yu3
    :param cluster: 使用聚类名称 默认为 NORMAL 还有
    :return: Ret类 如果成功则返回匹配词典
    """
    result = dict()
    for phonetic in o_phrase:
        if phonetic['p'] not in groups.keys():
            return Ret(Error.NOT_FOUND_PHONETIC, phonetic['p'])

    if min_max_match > len(o_phrase):
        min_max_match = len(o_phrase)

    for _phrase in phrases:  # 遍历所有的词语进行匹配
        phrase = _phrase[::-1]  # 词语反转
        max_match = 0  # 当前词语的匹配度为 0

        if phrase_len != len(phrase) and phrase_len != 0:
            continue
        if min_max_match > len(phrase):
            continue

        for i in range(min(len(phrase), len(o_phrase))):  # 开始匹配
            word = phrase[i]  # 匹配第i个字
            if word not in words:  # 不存在这个字
                break
            single_match = False
            for phonetic in words[word]:  # 遍历这个字的所有拼音
                if o_phrase[i]['t'] != '' and o_phrase[i]['t'] != phonetic['t']:
                    continue
                g1 = groups[o_phrase[i]['p']]  # 获取拼音所在组
                # print(phonetic)
                if phonetic['p'] not in groups.keys():
                    continue
                g2 = groups[phonetic['p']]  # 获取当前字的拼音所在组
                # 判断 g1 和 g2 是否在一个cluster
                for c in cluster:
                    if g1 in c and g2 in c:
                        single_match = True
                        break
                if single_match:
                    break
            if single_match:
                max_match += 1
            else:  # 当前字无法匹配，匹配终止
                break
        if min_max_match > max_match or max_match < 1:
            continue

        max_match = str(max_match)
        if max_match not in result.keys():
            result[max_match] = list()
        result[max_match].append(_phrase)
    return Ret(Error.OK, result)
