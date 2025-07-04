from diq import Dictify
from django.db import models

from Phrase.validators import PhraseErrors, TagErrors


class Phrase(models.Model, Dictify):
    phrase = models.CharField(
        max_length=20,
        unique=True,
    )

    tags = models.CharField(
        max_length=255,
        default=None,
    )

    @classmethod
    def get_phrase_by_phrase(cls, phrase):
        try:
            return cls.objects.get(phrase=phrase)
        except cls.DoesNotExist as err:
            raise PhraseErrors.NOT_FOUND(debug_message=err)

    @classmethod
    def create(cls, phrase, tags):
        phrase = cls.get_phrase_by_phrase(phrase)

        try:
            phrase = cls(
                phrase=phrase,
                tags=tags,
            )
            phrase.save()
        except Exception as err:
            raise PhraseErrors.CREATE(debug_message=err)
        return phrase

    def json(self):
        return self.dictify('tags', 'phrase')


class Tag(models.Model, Dictify):
    tag = models.CharField(
        max_length=10,
        unique=True,
    )

    @classmethod
    def get_by_id(cls, tag_id):
        try:
            return cls.objects.get(pk=tag_id)
        except cls.DoesNotExist as err:
            raise TagErrors.NOT_FOUND(details=err)

    @classmethod
    def get_by_tag(cls, tag):
        try:
            return cls.objects.get(tag=tag)
        except cls.DoesNotExist as err:
            raise TagErrors.NOT_FOUND(details=err)

    @classmethod
    def get_tag_dict(cls):
        tags = cls.objects.all()
        tag_dict = {}
        for tag in tags:
            tag_dict[str(tag.pk)] = dict(tag=tag.tag)
        return tag_dict

    @classmethod
    def create(cls, tag):
        try:
            tag = cls(tag=tag)
            tag.save()
        except Exception as err:
            raise TagErrors.CREATE(details=err)

        return tag

    def json(self):
        return self.dictify('pk->tid', 'tag')
