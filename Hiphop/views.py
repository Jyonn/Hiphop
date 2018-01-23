from Base.decorator import require_get
from Base.error import Error
from Base.response import response, error_response
from Init.fileread import match


def process_cluster_type(cluster_type):
    cluster_type = cluster_type.upper()
    if cluster_type not in ['DEFAULT', 'CUSTOMIZE']:
        cluster_type = 'DEFAULT'
    return cluster_type


@require_get([
    'phrase',
    {
        "value": 'phrase_len',
        "default": True,
        "default_value": 0,
        "process": int,
    },
    {
        "value": 'min_max_match',
        "default": True,
        "default_value": 0,
        "process": int,
    },
    'cluster',
    {
        "value": 'cluster_type',
        "process": process_cluster_type,
    }
])
def match_phrase(request):
    phrase = request.d.phrase
    phrase_len = request.d.phrase_len
    min_max_match = request.d.min_max_match
    cluster_type = request.d.cluster_type
    cluster = request.GET['cluster'].upper()

    phonetics = phrase.split(' ')
    o_phrase = list()
    for phonetic in phonetics:
        if phonetic[-1] in '01234':
            t = phonetic[-1]
            p = phonetic[:-1]
        else:
            t = ''
            p = phonetic
        o_phrase.append(dict(t=t, p=p))
    o_phrase.reverse()

    ret = match(
        o_phrase=o_phrase,
        phrase_len=phrase_len,
        min_max_match=min_max_match,
        cluster_type=cluster_type,
        cluster=cluster
    )
    if ret.error is not Error.OK:
        return error_response(ret)
    return response(body=ret.body)
