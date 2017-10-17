import json

from django.http import HttpResponse

from Base.error import Error


class Ret:
    """
    函数返回类
    """
    def __init__(self, error=Error.OK, body=None):
        self.error = error
        self.body = body or []


def response(code=0, msg="ok", body=None):
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
    for error in Error.ERROR_DICT:
        if error_id == error[0]:
            return response(code=error_id, msg=error[1]+append_msg)
    return error_response(Error.NOT_FOUND_ERROR)
