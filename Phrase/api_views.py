from django.views import View

from Base.decorator import require_get, require_post
from Base.error import Error
from Base.response import response, error_response
from Config.models import Config
from Init.fileread import phrases
from Phrase.models import Tag, Phrase

START = Config.get_config_by_key('start').body
assert isinstance(START, Config)


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
        start = int(START.value)
        sub_phrases = phrases[start: start+10]
        return response(sub_phrases)

    @staticmethod
    @require_post(['phrase', 'tags'])
    def post(request):
        phrase = request.d.phrase
        tags = request.d.tags
        tags = str(tags)

        if tags != 'DELETE':
            ret = Phrase.create(phrase, tags)
            if ret.error is not Error.OK:
                return error_response(ret)

        start = int(START.value) + 1
        START.value = str(start)
        START.save()

        return response()
