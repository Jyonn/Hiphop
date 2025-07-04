from django.views import View
from smartdjango import analyse

from Config.models import Config
from Init.fileread import worker
from Phrase.models import Tag, Phrase
from Phrase.params import TagParams, PhraseParams


class TagView(View):
    def get(self, request):
        return Tag.get_tag_dict()

    @analyse.body(TagParams.tag)
    def post(self, request):
        return Tag.create(request.body.tag).get_tag_dict()


class PhraseView(View):
    def get(self, request):
        start = int(Config.get_value_by_key('start'))
        phrase = worker.phrases[start]
        return phrase

    @analyse.body(PhraseParams.phrase, TagParams.tag)
    def post(self, request):
        tags = request.body.tags

        start = Config.get_config_by_key('start')

        if tags == 'BACK':
            start.value = str(int(start.value) - 1)
        elif tags == 'DELETE':
            start.value = str(int(start.value) + 1)
        else:
            Phrase.create(**request.body())
            start.value = str(int(start.value) + 1)

        start.save()

        return 0
