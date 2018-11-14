from django.views import View

from Base.decorator import require_get, require_post
from Base.error import Error
from Base.response import response, error_response
from Config.models import Config
from Init.fileread import phrases
from Phrase.models import Tag, Phrase


class TagView(View):
    @staticmethod
    @require_get()
    def get(request):
        return response(Tag.get_tag_dict())

    @staticmethod
    @require_post(['tag'])
    def post(request):
        tag = request.d.tag
        ret = Tag.create(tag)
        if ret.error is not Error.OK:
            return ret
        return response(Tag.get_tag_dict())


class PhraseView(View):
    @staticmethod
    @require_get()
    def get(request):
        start = int(Config.get_config_by_key('start').body.value)
        phrase = phrases[start]
        return response(phrase)

    @staticmethod
    @require_post(['phrase', 'tags'])
    def post(request):
        phrase = request.d.phrase
        tags = request.d.tags
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
