# from User.models import User


def deprint(*args):
    from Hiphop.settings import DEBUG
    if DEBUG:
        print(*args)


def save_session(request, key, value):
    request.session["saved_" + key] = value


def load_session(request, key, once_delete=True):
    value = request.session.get("saved_" + key)
    if value is None:
        return None
    if once_delete:
        del request.session["saved_" + key]
    return value


def login_to_session(request, o_user):
    """
    更新登录数据并添加到session
    :param request: HTTP请求
    :param o_user: 用户
    :return:
    """

    try:
        request.session.cycle_key()
    except:
        pass
    save_session(request, 'user', o_user.pk)
    return None


# def get_user_from_session(request):
#     try:
#         user_id = load_session(request, 'user', once_delete=False)
#         return User.objects.get(pk=user_id)
#     except:
#         pass
#     return None
