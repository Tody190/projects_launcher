#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/2/1 16:20
# @Author  : YangTao

import os


class EnvAction:
    def __init__(self, name):
        self.name = name

        self.value = os.getenv(name, None)
        if self.value:
            self.__values = [v for v in self.value.split(';')]
        else:
            self.__values = []

    def __append_env(self):
        os.environ[self.name] = ';'.join(self.__values)

    def append(self, value):
        if value in self.__values:
            self.__values.remove(value)

        self.__values.append(value)
        self.__append_env()

    def prepend(self, value):
        if value in self.__values:
            self.__values.remove(value)

        self.__values.insert(0, value)
        self.__append_env()

    def set(self, value):
        self.__values = [value]
        self.__append_env()

    def values(self):
        return self.__values


class EnvManager:
    def __getattr__(self, name):
        return EnvAction(name)


if __name__ == '__main__':
    # env = EnvManager()
    #
    # env.PYTHONPATH.set('/tmp')
    # print(env.PYTHONPATH.value)

    import os
    os.startfile(r'D:\temp\QTZqSR.bat')
