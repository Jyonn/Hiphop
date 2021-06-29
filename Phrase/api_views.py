from SmartDjango import Analyse
from django.views import View

from Base.decorator import require_get, require_post
from Base.error import Error
from Base.response import response, error_response
from Config.models import Config
from Init.fileread import worker
from Phrase.models import Tag, Phrase, TagP, PhraseP


class TagView(View):
    @staticmethod
    def get(_):
        return Tag.get_tag_dict()

    @staticmethod
    @Analyse.r(b=[TagP.tag])
    def post(r):
        return Tag.create(r.d.tag).get_tag_dict()


class PhraseView(View):
    @staticmethod
    @require_get()
    def get(_):
        start = int(Config.get_value_by_key('start'))
        phrase = worker.phrases[start]
        return phrase

    @staticmethod
    @require_post([PhraseP.phrase, TagP.tag])
    def post(r):
        phrase = r.d.phrase
        tags = r.d.tags
        tags = str(tags)

        start = Config.get_config_by_key('start').body

        if tags == 'BACK':
            start.value = str(int(start.value) - 1)
        elif tags == 'DELETE':
            start.value = str(int(start.value) + 1)
        else:
            ret = Phrase.create(phrase, tags)
            if ret.error is not Error.OK:
                return error_response(ret)
            start.value = str(int(start.value) + 1)

        start.save()

        return response()
