from django.db import models
from smartdjango import Error

from Config.validators import ConfigValidator, ConfigErrors


class Config(models.Model):
    vldt = ConfigValidator

    key = models.CharField(
        max_length=vldt.MAX_KEY_LENGTH,
        unique=True,
        validators=[vldt.key],
    )

    value = models.CharField(
        max_length=vldt.MAX_VALUE_LENGTH,
        validators=[vldt.value],
    )

    @classmethod
    def get_config_by_key(cls, key) -> 'Config':
        try:
            return cls.objects.get(key=key)
        except cls.DoesNotExist as err:
            raise ConfigErrors.NOT_FOUND(details=err)

    @classmethod
    def get_value_by_key(cls, key, default=None):
        try:
            return cls.get_config_by_key(key).value
        except Exception:
            return default

    @classmethod
    def update_value(cls, key, value):
        try:
            config = cls.get_config_by_key(key)
            config.value = value
            config.save()
        except Error as e:
            if e == ConfigErrors.NOT_FOUND:
                try:
                    config = cls(
                        key=key,
                        value=value,
                    )
                    config.save()
                except Exception as err:
                    raise ConfigErrors.CREATE(details=err)
            else:
                raise e
        except Exception as err:
            raise ConfigErrors.CREATE(details=err)


class ConfigInstance:
    pass


CI = ConfigInstance
