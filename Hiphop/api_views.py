from django.views import View
from smartdjango import analyse, Validator

from Init.fileread import worker


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
    return refined_phrase


def cluster_type_processor(cluster_type):
    cluster_type = cluster_type.upper()
    if cluster_type not in ['DEFAULT', 'CUSTOMIZE']:
        cluster_type = 'DEFAULT'
    return cluster_type


class MatchView(View):
    @analyse.query(
        Validator('phrase', final_name='phonetics').to(phrase_processor),
        Validator('phrase_len').default(0).to(int),
        Validator('min_max_match').default(0).to(int),
        Validator('cluster').to(lambda x: x.upper()),
        Validator('cluster_type').to(cluster_type_processor),
    )
    def get(self, requests):
        return worker.match(requests.query())
