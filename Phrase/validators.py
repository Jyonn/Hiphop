from smartdjango import Error, Code


@Error.register
class PhraseErrors:
    NOT_FOUND = Error("不存在的词语", code=Code.NotFound)
    CREATE = Error("创建词语错误", code=Code.BadRequest)


@Error.register
class TagErrors:
    NOT_FOUND = Error("不存在的标签", code=Code.NotFound)
    CREATE = Error("创建标签错误", code=Code.BadRequest)
