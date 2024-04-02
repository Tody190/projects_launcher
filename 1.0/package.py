# -*- coding: utf-8 -*-

name = 'projects_launcher'

version = '1.0'

description = 'Project tools launcher, launcher from cgteamwork'

authors = ['YangTao']

requires = ['PySide2',
            'Qt.py',
            'rez_api',
            'cgtw_api']


def commands():
    env.PYTHONPATH.append('{this.root}/python')
    env.PATH.append('{this.root}/bin')

uuid = 'projects_launcher'