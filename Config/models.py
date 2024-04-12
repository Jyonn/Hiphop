from SmartDjango import models, E, Hc


@E.register(id_processor=E.idp_cls_prefix())
class ConfigError:
    CREATE = E("更新配置错误", hc=Hc.InternalServerError)
    NOT_FOUND = E("不存在的配置", hc=Hc.NotFound)


class Config(models.Model):
    key = models.CharField(
        max_length=100,
        unique=True,
    )

    value = models.CharField(
        max_length=255,
    )

    @classmethod
    def get_config_by_key(cls, key):
        cls.validator(locals())

        try:
            return cls.objects.get(key=key)
        except cls.DoesNotExist as err:
            raise ConfigError.NOT_FOUND(debug_message=err)

    @classmethod
    def get_value_by_key(cls, key, default=None):
        try:
            return cls.get_config_by_key(key).value
        except Exception:
            return default

    @classmethod
    def update_value(cls, key, value):
        cls.validator(locals())

        try:
            config = cls.get_config_by_key(key)
            config.value = value
            config.save()
        except E as e:
            if e == ConfigError.NOT_FOUND:
                try:
                    config = cls(
                        key=key,
                        value=value,
                    )
                    config.save()
                except Exception as err:
                    raise ConfigError.CREATE(debug_message=err)
            else:
                raise e
        except Exception as err:
            raise ConfigError.CREATE(debug_message=err)


class ConfigInstance:
    pass


CI = ConfigInstance
