from Base.decorator import require_get_params, Error
from Base.response import response, error_response
from Init.fileread import match


@require_get_params(['phrase', 'phrase_len', 'min_max_match', 'cluster', 'cluster_type'])
def match_phrase(request):
    phrase = request.GET['phrase']
    try:
        phrase_len = int(request.GET['phrase_len'])
    except:
        phrase_len = 0
    try:
        min_max_match = int(request.GET['min_max_match'])
    except:
        min_max_match = 0
    cluster_type = request.GET['cluster_type'].upper()
    if cluster_type not in ['DEFAULT', 'CUSTOMIZE']:
        cluster_type = 'DEFAULT'
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

    rtn = match(o_phrase, phrase_len=phrase_len, min_max_match=min_max_match, cluster_type=cluster_type, cluster=cluster)
    if rtn.error is not Error.OK:
        return error_response(rtn.error, append_msg=rtn.body)
    return response(body=rtn.body)
