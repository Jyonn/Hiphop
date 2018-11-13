""" Adel Liu 180111

函数返回、方法返回、错误返回类
"""

import json

from django.http import HttpResponse

from Base.common import deprint, DEBUG
from Base.error import Error, E


class Ret:
    """
    函数返回类
    """
    def __init__(self, error=Error.OK, body=None, append_msg=''):
        if not isinstance(error, E):
            body = error
            error = Error.OK
        self.error = error
        self.body = body or []
        self.append_msg = append_msg


def response(e=Error.OK, msg=Error.OK.msg, body=None, allow=False):
    """
    回复HTTP请求
    """
    if not isinstance(e, E):
        body = e
        e = Error.OK
        msg = Error.OK.msg

    resp = {
        "status": 'debug' if DEBUG else 'release',
        "code": e.eid,
        "msg": msg,
        "body": body or [],
    }

    http_resp = HttpResponse(
        json.dumps(resp, ensure_ascii=False),
        status=200,
        content_type="application/json; encoding=utf-8",
    )
    if allow and isinstance(body, dict):
        allow_method_list = []
        for item in body:
            allow_method_list.append(item)
        http_resp['Allow'] = ', '.join(allow_method_list)
    return http_resp


def error_response(e, append_msg=""):
    """
    回复一个错误
    171216 当error_id为Ret类时，自动转换
    """
    if isinstance(e, Ret):
        append_msg = e.append_msg
        e = e.error
    if not isinstance(e, E):
        deprint(str(e))
        return error_response(Error.STRANGE, append_msg='error_response error_id not E')
    return response(e=e, msg=e.msg + append_msg)
