from smartdjango import Params, Validator

from Phrase.models import Phrase, Tag


class PhraseParams(metaclass=Params):
    model_class = Phrase

    phrase: Validator
    tags: Validator


class TagParams(metaclass=Params):
    model_class = Tag

    tag: Validator
