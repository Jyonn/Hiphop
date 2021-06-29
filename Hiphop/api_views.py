from SmartDjango import Analyse
from django.views import View
from smartify import P

from Init.fileread import worker


class MatchView(View):
    @staticmethod
    def cluster_type_processor(cluster_type):
        cluster_type = cluster_type.upper()
        if cluster_type not in ['DEFAULT', 'CUSTOMIZE']:
            cluster_type = 'DEFAULT'
        return cluster_type

    @staticmethod
    def phrase_processor(phrase):
        phonetics = phrase.split(' ')
        refined_phrase = list()
        for phonetic in phonetics:
            if phonetic[-1] in '01234':
                t = phonetic[-1]
                p = phonetic[:-1]
            else:
                t = ''
                p = phonetic
            refined_phrase.append(dict(t=t, p=p))
        refined_phrase.reverse()
        return phrase

    @staticmethod
    @Analyse.r(q=[
        P('phrase').process(phrase_processor),
        P('phrase_len').default(0).process(int),
        P('min_max_match').default(0).process(int),
        P('cluster').process(lambda x: x.upper()),
        P('cluster_type').process(cluster_type_processor),
    ])
    def get(r):
        return worker.match(**r.d.dict())
