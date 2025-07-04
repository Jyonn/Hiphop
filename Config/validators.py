from smartdjango import Error, Code


@Error.register
class ConfigErrors:
    CREATE = Error("更新配置错误", code=Code.InternalServerError)
    NOT_FOUND = Error("不存在的配置", code=Code.NotFound)
    KEY_TOO_LONG = Error("配置键过长，最大长度为 {key_length}", code=Code.BadRequest)
    VALUE_TOO_LONG = Error("配置值过长，最大长度为 {value_length}", code=Code.BadRequest)


class ConfigValidator:
    MAX_KEY_LENGTH = 100
    MAX_VALUE_LENGTH = 255

    @classmethod
    def key(cls, value):
        if len(value) > cls.MAX_KEY_LENGTH:
            raise ConfigErrors.KEY_TOO_LONG(key_length=cls.MAX_KEY_LENGTH)

    @classmethod
    def value(cls, value):
        if len(value) > cls.MAX_VALUE_LENGTH:
            raise ConfigErrors.VALUE_TOO_LONG(value_length=cls.MAX_VALUE_LENGTH)

