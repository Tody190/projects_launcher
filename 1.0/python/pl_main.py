#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/2/2 10:03
# @Author  : YangTao
import os
import sys

from Qt import QtWidgets
from Qt import QtCore
from Qt import QtGui

import utils
import config
import db

SETTING = QtCore.QSettings('tools', 'projects_launcher')


class ToolSetting(QtWidgets.QWidget):
    check_box_state_changed = QtCore.Signal()
    def __init__(self, pkg_name, items_data):
        super().__init__()
        setting_layout = QtWidgets.QVBoxLayout()
        self.pkg_name = pkg_name

        # items_data -->
        # {
        #     'en_US': {'checked': True, 'package_name': 'maya_language-en_US'},
        #     'zh_CN': {'package_name': 'maya_language-zh_CN'}
        # }

        self.items_data = items_data

        for item_name in self.items_data.keys():
            item_layout = QtWidgets.QHBoxLayout()

            # ui
            label = QtWidgets.QLabel(item_name)
            item_layout.addWidget(label)
            item_check_box = QtWidgets.QCheckBox()
            item_check_box.__name = item_name
            item_layout.addWidget(item_check_box)
            setting_layout.addLayout(item_layout)

            # connect
            item_check_box.stateChanged.connect(self.on_check_box_changed)

            # setting
            _name = self.pkg_name + '-' + item_name
            checked_value = SETTING.value(_name, None)
            if checked_value is None:
                if 'checked' in self.items_data[item_name]:
                    checked_value = self.items_data[item_name]['checked']
                else:
                    checked_value = False
            item_check_box.setChecked(checked_value)

        setting_layout.addStretch()

        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.main_layout.addLayout(setting_layout)

    def on_check_box_changed(self, state):
        _name =  self.pkg_name + '-' + self.sender().__name
        SETTING.setValue(_name, state)

        self.check_box_state_changed.emit()


class ToolItem(QtWidgets.QListWidgetItem):
    def __init__(self, name, version=''):
        super().__init__()
        self.name = name
        self.version = version

        icon_file = utils.icon_file(name)
        self.setIcon(QtGui.QIcon(icon_file))
        self.setText(name + ' - ' + version)

        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(15)
        self.setFont(font)

        self.setToolTip(u'双击启动')


class MainUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__(parent=None)

        self.cgtw_db = db.CGTW_DB()
        self.task_info = self.cgtw_db.task_info

        self._setup_ui()

    def _setup_ui(self):
        self.setWindowTitle(u'启动器')
        self.setWindowIcon(QtGui.QIcon(utils.icon_file('launcher')))

        # info
        self.project_info_label = QtWidgets.QLabel()
        font = QtGui.QFont()
        font.setBold(True)
        self.setFont(font)
        self.project_info_label.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)

        self.project_info_layout = QtWidgets.QVBoxLayout()
        self.project_info_layout.addWidget(self.project_info_label)
        self.project_info_layout.addStretch()

        # list widget
        self.tools_list_widget = QtWidgets.QListWidget()
        self.tools_list_widget.setStyleSheet(
            "QListWidget::item:selected{background-color: lightgreen;color: darkblue;}"
        )
        # add data
        for n, ver in self.get_tools_data():
            t_item = ToolItem(n, ver)
            self.tools_list_widget.addItem(t_item)
            self.tools_list_widget.setIconSize(QtCore.QSize(35, 35))

        self.tools_list_widget_layout = QtWidgets.QHBoxLayout()
        self.tools_list_widget_layout.addWidget(self.tools_list_widget)
        self.tools_list_widget.itemDoubleClicked.connect(self.launch_tool_and_close_ui)

        # rez command widget
        self.rez_command_widget = QtWidgets.QLineEdit()
        self.rez_command_widget.setText('rez-python')
        self.rez_launch_button = QtWidgets.QPushButton(u'启动')

        self.rez_command_layout = QtWidgets.QHBoxLayout()
        self.rez_command_layout.addWidget(self.rez_command_widget)
        self.rez_command_layout.addWidget(self.rez_launch_button)

        # tools_layout
        self.tools_layout = QtWidgets.QHBoxLayout()
        self.tools_layout.addLayout(self.project_info_layout)
        self.tools_layout.addLayout(self.tools_list_widget_layout)

        # main layout
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.addLayout(self.tools_layout)
        self.main_layout.addLayout(self.rez_command_layout)

        # connect
        self.tools_list_widget.itemClicked.connect(self.show_item_setting)
        self.tools_list_widget.itemClicked.connect(self.set_rez_command)
        self.rez_launch_button.clicked.connect(self.launch_tool)

        self.__setting_widget = []

        # add project info
        self.project_info_label.setText(self.get_project_show_info())

    def get_tools_data(self):
        # add list items
        tools_data = []
        tools_info = utils.get_project_tools(self.cgtw_db.project_name)
        for item in tools_info:
            # ['Maya', '2023'] or ['Maya', '2023|2014']
            t_name = item[0]  # Maya
            t_ver = item[1]  # 2023 or 2023|2024

            if '|' in t_ver:
                t_ver_list = [v for v in t_ver.split('|')]
            else:
                t_ver_list = [t_ver]

            for ver in t_ver_list:
                tools_data.append((t_name, ver))

        return tools_data

    def get_project_show_info(self):
        info = u'项目：%s\n' % self.cgtw_db.project_name
        if self.task_info:
            type = self.task_info.get('type', '')
            if type == 'shot':
                info += u'场次：%s\n' % self.task_info.get('sequence', '')
                info += u'镜头：%s\n' % self.task_info.get('shot', '')
            if type == 'asset':
                info += u'资产类型：%s\n' % self.task_info.get('asset_type', '')
                info += u'资产名称：%s\n' % self.task_info.get('asset_name', '')
                info += u'资产中文：%s\n' % self.task_info.get('asset_name_cn', '')

            info += u'阶段：%s\n' % self.task_info.get('step', '')
            info += u'任务：%s' % self.task_info.get('task', '')

        return info


    def show_item_setting(self, list_item):
        for w in self.__setting_widget:
            try:
                self.tools_list_widget_layout.removeWidget(w)
                w.deleteLater()
            except:
                pass

        # [{'name': show_name, 'package_name': package_name}], ...]
        extend_packages_map = config.extend_packages_map.get(list_item.name, None)
        if extend_packages_map:
            # setting_name_list = [w['name'] for w in extend_packages_list]
            ts = ToolSetting(list_item.name, extend_packages_map)
            ts.check_box_state_changed.connect(self.set_rez_command)
            self.tools_list_widget_layout.addWidget(ts)
            self.__setting_widget.append(ts)

    def set_env(self):
        # Set some global environment variables
        # The DCC software can be obtained after starting

        os.environ['PROJECT_DATABASE'] = self.cgtw_db.project_name
        if self.task_info:
            type = self.task_info.get('type', '')
            os.environ['PROJECT_TYPE'] = type
            if type == 'shot':
                os.environ['PROJECT_SEQUENCE'] = self.task_info.get('sequence', '')
                os.environ['PROJECT_SHOT'] = self.task_info.get('shot', '')
            if type == 'asset':
                os.environ['PROJECT_ASSET_TYPE'] = self.task_info.get('asset_type', '')
                os.environ['PROJECT_ASSET_NAME'] = self.task_info.get('asset_name', '')
                os.environ['PROJECT_ASSET_NAME_CN'] = self.task_info.get('asset_name_cn', '')

            os.environ['PROJECT_STEP'] = self.task_info.get('step', '')
            os.environ['PROJECT_TASK'] = self.task_info.get('task', '')

    def set_rez_command(self):
        self.set_env()

        select_item = self.tools_list_widget.currentItem()
        # rez-env proj_as24y_stun
        rez_command = 'rez-env ' + self.cgtw_db.project_name
        # rez-env proj_as24y_stun maya-2023
        rez_command += ' {}-{}'.format(select_item.name, select_item.version)

        # add extend package
        setting_data = config.extend_packages_map.get(select_item.name, None)
        if setting_data:
            for s_name, s_info in setting_data.items():
                # s_name: en_US
                _name = select_item.name + '-' + s_name  # maya-en_US
                checked_value = SETTING.value(_name, None)
                if checked_value:
                    rez_command += ' ' + config.extend_packages_map[select_item.name][s_name]['package_name']

        # add tool name
        # get package launch name
        package_launch_name = config.pkg_launch_map.get(select_item.name.lower(), None)
        if not package_launch_name:
            package_launch_name = select_item.name.lower()

        rez_command += ' -- ' + package_launch_name

        self.rez_command_widget.setText(rez_command)

    def launch_tool(self):
        rez_command = self.rez_command_widget.text()
        select_item = self.tools_list_widget.currentItem()
        name = '{}_{}_{}'.format(self.cgtw_db.project_name,
                                 select_item.name,
                                 select_item.version)  # maya_2023
        bat_file = utils.build_new_bat_file(command=rez_command,
                                            name=name)
        print(bat_file)
        os.startfile(bat_file)

    def launch_tool_and_close_ui(self):
        self.launch_tool()
        self.close()


def show_ui():
    app = QtWidgets.QApplication(sys.argv)
    m_ui = MainUI()
    m_ui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    show_ui()