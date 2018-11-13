from django.views import View

from Base.decorator import require_get, require_post
from Base.error import Error
from Base.response import response
from Phrase.models import Tag


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
        o_tag = ret.body
        return response(o_tag.to_dict())


# class PhraseView:
#     @staticmethod
#     @require_get()
#     def get(request):
#