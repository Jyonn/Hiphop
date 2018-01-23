""" 171203 Adel Liu """

DEBUG = True


def deprint(*args):
    """
    系统处于调试状态时输出数据
    """
    if DEBUG:
        print(*args)
