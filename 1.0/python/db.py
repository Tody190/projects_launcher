#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/2/27 12:17
# @Author  : YangTao


class CGTW_DB:
    def __init__(self):
        import cgtw2

        self.t_tw = cgtw2.tw()

    @property
    def project_name(self):
        return self.t_tw.client.get_database()

    @property
    def module(self):
        return self.t_tw.client.get_module()

    @property
    def module_type(self):
        return self.t_tw.client.get_module_type()

    @property
    def id_list(self):
        return self.t_tw.client.get_id()

    @property
    def id(self):
        return self.id_list[0]

    @property
    def task_info(self, id_list=None):
        # the information template returned by cgtw
        info_tmp = {'type': '',  # asset or shot
                    'asset_type': '',  # chr
                    'asset_name': '',  # xiaoming
                    'asset_name_cn': '',  # 小明
                    'sequence': '',
                    'shot': '',
                    'step': '',
                    'task':''}

        if self.module_type != 'task':
            return info_tmp

        if self.module == 'asset':
            info_tmp['type'] = 'asset'

            info = self.t_tw.task.get(db=self.project_name,
                                      module=self.module,
                                      id_list=[self.id],
                                      field_sign_list=['asset.entity',
                                                       'asset.cn_name',
                                                       'asset_type.entity',
                                                       'pipeline.entity',
                                                       'task.entity'
                                                       ])

            if info:
                info_tmp['asset_name'] = info[0]['asset.entity']
                info_tmp['asset_type'] = info[0]['asset_type.entity']
                info_tmp['asset_name_cn'] = info[0]['asset.cn_name']
                info_tmp['step'] = info[0]['pipeline.entity']
                info_tmp['task'] = info[0]['task.entity']

        if self.module == 'shot':
            info = self.t_tw.task.get(db=self.project_name,
                                      module=self.module,
                                      id_list=[self.id],
                                      field_sign_list=['seq.entity',
                                                       'shot.entity',
                                                       'pipeline.entity',
                                                       'task.entity'
                                                       ])

            if info:
                info_tmp['type'] = 'shot'
                info_tmp['sequence'] = info[0]['seq.entity']
                info_tmp['shot'] = info[0]['shot.entity']
                info_tmp['step'] = info[0]['pipeline.entity']
                info_tmp['task'] = info[0]['task.entity']

        return info_tmp


if __name__ == '__main__':
    cgtw_db = CGTW_DB()
    a = cgtw_db.task_info
    print(a)
    print(cgtw_db.module_type)
    # print(cgtw_db.type_name)