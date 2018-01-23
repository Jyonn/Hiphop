""" Adel Liu 180111

函数返回、方法返回、错误返回类
"""

import json

from django.http import HttpResponse

from Base.common import deprint
from Base.error import Error


class Ret:
    """
    函数返回类
    """
    def __init__(self, error=Error.OK, body=None, append_msg=''):
        self.error = error
        self.body = body or []
        self.append_msg = append_msg


def response(code=0, msg="ok", body=None):
    """
    回复HTTP请求
    """
    resp = {
        "code": code,
        "msg": msg,
        "body": body or [],
    }

    http_resp = HttpResponse(
        json.dumps(resp, ensure_ascii=False),
        status=200,
        content_type="application/json; encoding=utf-8",
    )
    return http_resp


def error_response(error_id, append_msg=""):
    """
    回复一个错误
    171216 当error_id为Ret类时，自动转换
    """
    if isinstance(error_id, Ret):
        append_msg = error_id.append_msg
        error_id = error_id.error
    for error in Error.ERROR_DICT:
        if error_id == error[0]:
            return response(code=error_id, msg=error[1]+append_msg)
    deprint('Error Not Found: ', error_id)
    return error_response(Error.ERROR_NOT_FOUND)
