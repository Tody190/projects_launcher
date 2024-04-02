#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/2/6 15:50
# @Author  : YangTao

import os

# icons
resource_path = os.path.join(os.path.dirname(__file__), 'resource')

# launcher bat folder
launchers_folder = os.path.join(os.path.expanduser('~'), '.launcher')

# Some tools will allow the user to customize the REZ extension package when they are launched
# For example, maya can configure rez packages in both Chinese and English
extend_packages_map = {
    'maya': {
        u'英文': {'checked': True, 'package_name': 'maya_language-en_US'},
        u'中文': {'package_name': 'maya_language-zh_CN'}
    }
}

# The name of the launcher that will be used to launch
pkg_launch_map = {'maya': 'maya -noAutoloadPlugins',
                  'nuke': 'nuke',
                  'houdini': 'houdini'}