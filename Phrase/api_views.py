from SmartDjango import Analyse
from django.views import View

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
    def get(_):
        start = int(Config.get_value_by_key('start'))
        phrase = worker.phrases[start]
        return phrase

    @staticmethod
    @Analyse.r(b=[PhraseP.phrase, TagP.tag])
    def post(r):
        tags = r.d.tags

        start = Config.get_config_by_key('start').body

        if tags == 'BACK':
            start.value = str(int(start.value) - 1)
        elif tags == 'DELETE':
            start.value = str(int(start.value) + 1)
        else:
            Phrase.create(**r.d.dict())
            start.value = str(int(start.value) + 1)

        start.save()

        return 0
