import json

from django.db import models

from Base.common import deprint
from Base.decorator import field_validator
from Base.error import Error
from Base.response import Ret


class Phrase(models.Model):
    L = {
        'phrase': 20,
        'tags': 255,
    }

    phrase = models.CharField(
        max_length=L['phrase'],
        unique=True,
    )

    tags = models.CharField(
        max_length=L['tags'],
        default=None,
    )

    FIELD_LIST = ['phrase', 'tags']

    @classmethod
    def _validate(cls, dict_):
        """验证传入参数是否合法"""
        return field_validator(dict_, cls)

    @classmethod
    def get_phrase_by_phrase(cls, phrase):
        ret = cls._validate(locals())
        if ret.error is not Error.OK:
            return ret

        try:
            o_phrase = cls.objects.get(phrase=phrase)
        except cls.DoesNotExist as err:
            deprint(str(err))
            return Ret(Error.NOT_FOUND_PHRASE)
        return Ret(o_phrase)

    @classmethod
    def create(cls, phrase, tags):
        ret = cls._validate(locals())
        if ret.error is not Error.OK:
            return ret

        ret = cls.get_phrase_by_phrase(phrase)
        if ret.error is Error.OK:
            return ret

        try:
            o_phrase = cls(
                phrase=phrase,
                tags=tags,
            )
            o_phrase.save()
        except Exception as err:
            deprint(str(err))
            return Ret(Error.ERROR_CREATE_PHRASE, append_msg=str(err))
        return Ret(o_phrase)

    def to_dict(self):
        return dict(
            tags=self.tags,
            phrase=self.phrase,
        )


class Tag(models.Model):
    L = {
        'tag': 10,
    }

    tag = models.CharField(
        max_length=L['tag'],
        unique=True,
    )

    FIELD_LIST = ['tag']

    @classmethod
    def _validate(cls, dict_):
        """验证传入参数是否合法"""
        return field_validator(dict_, cls)

    @classmethod
    def get_tag_by_id(cls, tag_id):
        try:
            o_tag = cls.objects.get(pk=tag_id)
        except cls.DoesNotExist as err:
            deprint(str(err))
            return Ret(Error.NOT_FOUND_TAG)
        return Ret(o_tag)

    @classmethod
    def get_tag_by_tag(cls, tag):
        try:
            o_tag = cls.objects.get(tag=tag)
        except cls.DoesNotExist as err:
            deprint(str(err))
            return Ret(Error.NOT_FOUND_TAG)
        return Ret(o_tag)

    @classmethod
    def get_tag_dict(cls):
        tags = cls.objects.all()
        tag_dict = {}
        for o_tag in tags:
            tag_dict[str(o_tag.pk)] = o_tag.tag
        return tag_dict

    @classmethod
    def create(cls, tag):
        ret = cls._validate(locals())
        if ret.error is not Error.OK:
            return ret

        ret = cls.get_tag_by_tag(tag)
        if ret.error is Error.OK:
            return ret

        try:
            o_tag = cls(
                tag=tag,
            )
        except Exception as err:
            deprint(str(err))
            return Ret(Error.ERROR_CREATE_TAG)

        return Ret(o_tag)

    def to_dict(self):
        return dict(
            tid=self.pk,
            tag=self.tag,
        )

