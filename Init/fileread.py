import re

import os
import codecs

from SmartDjango import E, Hc

from Hiphop.settings import BASE_DIR


@E.register(id_processor=E.idp_cls_prefix())
class WorkerError:
    NOT_FOUND_PHONETIC = E('不是合法的拼音', hc=Hc.NotFound)


class Worker:
    def __init__(self):
        self.dictionary = dict()
        self.words = dict()
        self.phrases = list()
        self.groups = dict()
        self.clusters = dict()
        self.root_path = os.path.join(BASE_DIR, 'Init')

        self.read_word()
        self.read_phrase()
        self.read_group()
        self.read_cluster()

    @staticmethod
    def get_cluster(raw_cluster):
        cluster = list()
        raw_cluster = raw_cluster.split(';')
        for c in raw_cluster:
            group_list = c.split(',')
            cluster.append(group_list)
        return cluster

    def get_file(self, filename):
        return codecs.open(os.path.join(self.root_path, filename), 'r+', encoding='utf8')

    def read_word(self):
        for s in self.get_file('word'):
            if s[-1] == '\n':
                s = s[:-1]
            p, ws = re.split('\d+', s, 1)
            tune = s[len(p)]
            p = p.lower()
            if tune == '5':
                tune = '0'
            if p not in self.dictionary.keys():
                self.dictionary[p] = dict()
            self.dictionary[p][tune] = ws

            for w in ws:
                if w not in self.words.keys():
                    self.words[w] = list()
                self.words[w].append(dict(
                    p=p,
                    t=tune,
                ))

    def read_phrase(self):
        for s in self.get_file('phrase'):
            if s[-1] == '\n':
                s = s[:-1]
            self.phrases.append(s)

    def read_group(self):
        for s in open(os.path.join(self.root_path, 'group'), 'r+'):
            if s[-1] == '\n':
                s = s[:-1]
            g = s.lower().split(' ')
            # groups[g[0]] = g[1:]
            for p in g[1:]:
                self.groups[p] = g[0]

    def read_cluster(self):
        cluster_free = True
        cluster_name = ''
        for s in self.get_file('cluster'):
            if s[-1] == '\n':
                s = s[:-1]
            if cluster_free:
                match = re.search('\[CLUSTER-(.*?)\]', s)
                if match:
                    cluster_name = match.group(1).upper()
                    cluster_free = False
            else:
                cluster_free = True
                self.clusters[cluster_name] = self.get_cluster(s)

    def match(self, phonetics, cluster, min_max_match, phrase_len, cluster_type):
        """
        词语匹配
        :param cluster_type: cluster类型
        :param phrase_len: 匹配的词语长度 0 表示所有长度
        :param min_max_match: 最小匹配的最大长度 -1 表示所能达到的最大长度
        :param phonetics: 拼音列表 如羽毛球 则 qiu2 mao2 yu3
        :param cluster: 使用聚类名称 默认为 NORMAL 还有
        :return: Ret类 如果成功则返回匹配词典
        """
        if cluster_type == 'DEFAULT':
            if cluster in self.clusters.keys():
                cluster = self.clusters[cluster]
            else:
                cluster = self.clusters['NORMAL']
        else:
            cluster = self.get_cluster(cluster)

        result = dict()
        for phonetic in phonetics:
            if phonetic['p'] not in self.groups.keys():
                raise WorkerError.NOT_FOUND_PHONETIC

        if min_max_match > len(phonetics):
            min_max_match = len(phonetics)

        for _phrase in self.phrases:  # 遍历所有的词语进行匹配
            phrase = _phrase[::-1]  # 词语反转
            max_match = 0  # 当前词语的匹配度为 0

            if phrase_len != len(phrase) and phrase_len != 0:
                continue
            if min_max_match > len(phrase):
                continue

            for i in range(min(len(phrase), len(phonetics))):  # 开始匹配
                word = phrase[i]  # 匹配第i个字
                if word not in self.words:  # 不存在这个字
                    break
                single_match = False
                for phonetic in self.words[word]:  # 遍历这个字的所有拼音
                    if phonetics[i]['t'] != '' and phonetics[i]['t'] != phonetic['t']:
                        continue
                    g1 = self.groups[phonetics[i]['p']]  # 获取拼音所在组
                    # print(phonetic)
                    if phonetic['p'] not in self.groups.keys():
                        continue
                    g2 = self.groups[phonetic['p']]  # 获取当前字的拼音所在组
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
        return result


worker = Worker()
