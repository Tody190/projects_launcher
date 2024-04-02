#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/2/21 14:34
# @Author  : YangTao

import os
import random
import string

import rez.package_search as rez_package_search

import config


def icon_file(name):
    f_name = name.lower() + '.ico'
    f = os.path.join(config.resource_path, 'icons', f_name).replace('\\', '/')
    if not os.path.isfile(f):
        return f.replace(f_name, 'no_icon.ico')
    return f


# def get_current_database_name():
#     import cgtw2
#     t_tw = cgtw2.tw()
#     db = t_tw.client.get_database()
#
#     return db


def get_project_tools(project_pkg_name):
    pkg = rez_package_search.get_latest_package(project_pkg_name)

    # _launcher_tools = (
    #     ('maya', '2023'),
    #     ('nuke', '12.2v9|13.2v8'),
    #     ('houdini', '19.5.493')
    # )
    #            ↓
    return pkg._launcher_tools


def get_and_clean_bat_file():
    l_f = config.launchers_folder
    if not os.path.exists(l_f):
        os.makedirs(l_f)

    # clean old bat
    for f in os.listdir(l_f):
        if f.endswith('.bat'):
            try:
                os.remove(os.path.join(l_f, f))
            except:
                pass

    random_name_bat = ''.join(random.sample(string.ascii_letters, 6)) + '.bat'

    return os.path.join(l_f, random_name_bat)


def build_bat_file(command, bat_file):
    # Get all the current environment variables and hit it into bat
    with open(bat_file, 'w') as f:
        f.write('@echo off\n\n')
        for key, value in os.environ.items():
            f.write('set %s=%s\n' % (key, value))

        f.write('\n' + command + '\n')


def build_new_bat_file(command, name=None):
    if name is None:
        bat_file = get_current_database_name()
    else:
        l_f = config.launchers_folder
        if not os.path.exists(l_f):
            os.makedirs(l_f)
        bat_file = os.path.join(l_f, name + '.bat')

    build_bat_file(command, bat_file)

    return bat_file


if __name__ == '__main__':
    import cgtw2

    t_tw = cgtw2.tw()
    db = t_tw.client.get_database()
    print(db)

    # command = 'rez-env proj_as24y_stun maya-2023 maya_language-en_US -- maya'
    # bat_file = 'D:/temp/launcher.bat'
    # build_bat(command, bat_file)
    # home_dir = os.path.expanduser('~')
    # print(home_dir)