""" Adel Liu 180111

字典转为对象，用于request.body
"""


class Param(object):
    """对象类，把字典类的key转换为对象的属性"""
    def __init__(self, d):
        if not isinstance(d, dict):
            return
        for k in d.keys():
            self.__setattr__(k, d[k])
