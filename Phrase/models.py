from SmartDjango import models, E, Hc


@E.register(id_processor=E.idp_cls_prefix())
class PhraseError:
    NOT_FOUND = E("不存在的词语", hc=Hc.NotFound)
    CREATE = E("创建词语错误", hc=Hc.BadRequest)


@E.register(id_processor=E.idp_cls_prefix())
class TagError:
    NOT_FOUND = E("不存在的标签", hc=Hc.NotFound)
    CREATE = E("创建标签错误", hc=Hc.BadRequest)


class Phrase(models.Model):
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
            raise PhraseError.NOT_FOUND(debug_message=err)

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
            raise PhraseError.CREATE(debug_message=err)
        return phrase

    def d(self):
        return self.dictify('tags', 'phrase')


class Tag(models.Model):
    tag = models.CharField(
        max_length=10,
        unique=True,
    )

    @classmethod
    def get_by_id(cls, tag_id):
        try:
            return cls.objects.get(pk=tag_id)
        except cls.DoesNotExist as err:
            raise TagError.NOT_FOUND(debug_message=err)

    @classmethod
    def get_by_tag(cls, tag):
        try:
            return cls.objects.get(tag=tag)
        except cls.DoesNotExist as err:
            raise TagError.NOT_FOUND(debug_message=err)

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
            tag = cls(
                tag=tag,
            )
            tag.save()
        except Exception as err:
            raise TagError.CREATE(debug_message=err)

        return tag

    def d(self):
        return self.dictify('pk->tid', 'tag')


class PhraseP:
    phrase, tags = Phrase.get_params('phrase', 'tags')


class TagP:
    tag, = Tag.get_params('tag')
    tag.process(str, begin=True)
