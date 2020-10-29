#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-10-20
# @Author  : Happiless.zhang (Happiless.zhang@fatritech.com)
# @Version : v_1.0
# @note    : 操作es的工具模块
import elasticsearch as es


class ElasticSearch(object):

    def __init__(self, ip="8.129.43.47", index_name="test", index_type="text"):
        '''

                :param index_name: 索引名称
                :param index_type: 索引类型
                '''
        self.index_name = index_name
        self.index_type = index_type
        # 无用户名密码状态
        # self.es = Elasticsearch([ip])
        # 用户名密码状态
        self.es = es.Elasticsearch([ip], http_auth=('elastic', 'password'), port=9200)

    def get_data_id(self, id):
        res = self.es.get(index=self.index_name, doc_type=self.index_type, id=id)
        print(res['_source'])


if __name__ == '__main__':
    ElasticSearch().get_data_id("1")

