""" 171203 Adel Liu

弃用http.require_POST和http.require_GET
将require_POST和require_params合二为一
把最终参数字典存储在request.d中
"""

import base64
import json
from functools import wraps

from django.db import models
from django.http import HttpRequest

from Base.common import deprint
from Base.error import Error
from Base.param import Param
from Base.response import Ret, error_response


def validate_params(r_param_valid_list, g_params):
    """ 验证参数

    [
        ('a', '[a-z]+'),
        'b',
        ('c', valid_c_func),
        ('d', valid_d_func, default_d_value)
        {
            "value": "e",
            "func": valid_e_func,
            "default": True,
            "default_value": default_e_value,
            "process": process_e_value (str to int)
        }
    ]
    """
    import re

    if not r_param_valid_list:
        return Ret()
    for r_param_valid in r_param_valid_list:
        # has_default_value = False
        # default_value = None  # 默认值
        valid_method = None  # 验证参数的方式（如果是字符串则为正则匹配，如果是函数则带入函数，否则忽略）
        process = None

        if isinstance(r_param_valid, str):  # 如果rpv只是个字符串，则符合例子中的'b'情况
            r_param = r_param_valid

        elif isinstance(r_param_valid, tuple):  # 如果rpv是tuple，则依次为变量名、验证方式、默认值
            if not r_param_valid:  # 忽略
                continue
            r_param = r_param_valid[0]  # 得到变量名
            if len(r_param_valid) > 1:
                valid_method = r_param_valid[1]  # 得到验证方式
                if len(r_param_valid) > 2:
                    # has_default_value = True
                    g_params.setdefault(r_param, r_param_valid[2])
        elif isinstance(r_param_valid, dict):  # 忽略
            r_param = r_param_valid.get('value', None)
            if r_param is None:
                continue
            valid_method = r_param_valid.get('func', None)
            default = r_param_valid.get('default', False)
            default_value = r_param_valid.get('default_value', None)
            if default:
                g_params.setdefault(r_param, default_value)
            process = r_param_valid.get('process', None)
        else:
            continue

        if r_param not in g_params:  # 如果传入数据中没有变量名
            return Ret(Error.REQUIRE_PARAM, append_msg=r_param)  # 报错

        req_value = g_params[r_param]

        if isinstance(valid_method, str):
            if re.match(valid_method, req_value) is None:
                return Ret(Error.ERROR_PARAM_FORMAT, append_msg=r_param)
        elif callable(valid_method):
            try:
                ret = valid_method(req_value)
                if ret.error is not Error.OK:
                    return ret
            except Exception as err:
                deprint(str(err))
                return Ret(Error.ERROR_VALIDATION_FUNC)
        if process is not None and callable(process):
            try:
                g_params[r_param] = process(req_value)
            except Exception as err:
                deprint(str(err))
                return Ret(Error.ERROR_PROCESS_FUNC)
    return Ret(Error.OK, g_params)


def field_validator(dict_, cls):
    """
    针对model的验证函数
    事先需要FIELD_LIST存放需要验证的属性
    需要L字典存放CharField类型字段的最大长度
    可选创建_valid_<param>函数进行自校验
    """
    field_list = getattr(cls, 'FIELD_LIST', None)
    if field_list is None:
        return Ret(Error.ERROR_VALIDATION_FUNC, append_msg='，不存在FIELD_LIST')
    _meta = getattr(cls, '_meta', None)
    if _meta is None:
        return Ret(Error.ERROR_VALIDATION_FUNC, append_msg='，不是Django的models类')
    len_list = getattr(cls, 'L', None)
    if len_list is None:
        return Ret(Error.ERROR_VALIDATION_FUNC, append_msg='，不存在长度字典L')

    for k in dict_.keys():
        if k in getattr(cls, 'FIELD_LIST'):
            if isinstance(_meta.get_field(k), models.CharField):
                try:
                    if len(dict_[k]) > len_list[k]:
                        return Ret(
                            Error.ERROR_PARAM_FORMAT,
                            append_msg='，%s的长度不应超过%s个字符' % (k, len_list[k])
                        )
                except TypeError as err:
                    deprint(str(err))
                    return Ret(Error.ERROR_PARAM_FORMAT, append_msg="，%s不是字符串" % k)

        tuple_name = '%s_TUPLE' % k.upper()
        tuple_ = getattr(cls, tuple_name, None)
        if tuple_ is not None and isinstance(tuple_, tuple):
            flag = False
            for item in tuple_:
                if not isinstance(item, tuple):
                    return Ret(Error.ERROR_TUPLE_FORMAT, append_msg='（%s）' % tuple_name)
                if dict_[k] == item[0]:
                    flag = True
            if not flag:
                return Ret(Error.ERROR_PARAM_FORMAT, append_msg='，%s的值应该在%s之中' % (k, tuple_name))
        valid_func = getattr(cls, '_valid_%s' % k, None)
        if valid_func is not None and callable(valid_func):
            # print('_valid_', k)
            ret = valid_func(dict_[k])
            if ret.error is not Error.OK:
                return ret
    return Ret()


def require_method(method, r_params=None, decode=True):
    """generate decorator, validate func with proper method and params"""
    def decorator(func):
        """decorator"""
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            """wrapper"""
            if not isinstance(request, HttpRequest):
                return error_response(Error.STRANGE)
            if request.method != method:
                return error_response(Error.ERROR_METHOD, append_msg='，需要%s请求' % method)
            if request.method == "GET":
                request.DICT = request.GET.dict()
            else:
                try:
                    request.DICT = json.loads(request.body.decode())
                except json.JSONDecodeError as err:
                    deprint(str(err))
                    request.DICT = {}
            if decode:
                for k in request.DICT.keys():
                    import binascii
                    try:
                        base64.decodebytes(bytes(request.DICT[k], encoding='utf8')).decode()
                    except binascii.Error as err:
                        deprint(str(err))
                        return error_response(Error.REQUIRE_BASE64)
            ret = validate_params(r_params, request.DICT)
            if ret.error is not Error.OK:
                return error_response(ret)
            request.d = Param(ret.body)
            return func(request, *args, **kwargs)

        return wrapper
    return decorator


def require_post(r_params=None, decode=False):
    """decorator, require post method"""
    return require_method('POST', r_params, decode)


def require_get(r_params=None, decode=False):
    """decorator, require get method"""
    return require_method('GET', r_params, decode)


def require_put(r_params=None, decode=False):
    """decorator, require put method"""
    return require_method('PUT', r_params, decode)


def require_delete(r_params=None, decode=False):
    """decorator, require delete method"""
    return require_method('DELETE', r_params, decode)


def require_json(func):
    """把request.body的内容反序列化为json"""
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        """wrapper"""
        if request.body:
            try:
                request.DICT = json.loads(request.body.decode())
            except json.JSONDecodeError as err:
                deprint(str(err))
            return func(request, *args, **kwargs)
        return error_response(Error.REQUIRE_JSON)
    return wrapper
