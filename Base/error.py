""" 171203 Adel Liu

错误表，在编码时不断添加
"""


class Error:
    NOT_FOUND_PHONETIC = 2000
    
    ERROR_PROCESS_FUNC = 1011
    ERROR_TUPLE_FORMAT = 1010
    REQUIRE_ROOT = 1009
    ERROR_VALIDATION_FUNC = 1008
    ERROR_PARAM_FORMAT = 1007
    REQUIRE_BASE64 = 1006
    ERROR_METHOD = 1005
    STRANGE = 1004
    REQUIRE_LOGIN = 1003
    REQUIRE_JSON = 1002
    REQUIRE_PARAM = 1001
    ERROR_NOT_FOUND = 1000
    OK = 0

    ERROR_DICT = [
        (NOT_FOUND_PHONETIC, "不是合法的拼音"),

        (ERROR_PROCESS_FUNC, "参数预处理函数错误"),
        (ERROR_TUPLE_FORMAT, "属性元组格式错误"),
        (REQUIRE_ROOT, "需要管理员登录"),
        (ERROR_VALIDATION_FUNC, "错误的参数验证函数"),
        (ERROR_PARAM_FORMAT, "错误的参数格式"),
        (REQUIRE_BASE64, "参数需要base64编码"),
        (ERROR_METHOD, "错误的HTTP请求方法"),
        (STRANGE, "未知错误"),
        (REQUIRE_LOGIN, "需要登录"),
        (REQUIRE_JSON, "需要JSON数据"),
        (REQUIRE_PARAM, "缺少参数"),
        (ERROR_NOT_FOUND, "不存在的错误"),
        (OK, "没有错误"),
    ]
