#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-09-28 11:28:37
# @Author  : Xinhuabu (Huabu.xin@fatritech.com)
# @Link    : ${link}
# @Version : $Id$

import os
from pyhive import hive


class Hive(object):

    def __init__(self, host, port, user, database, password=None,
                 config=None, kerberos_service_name=None,
                 auth=None, thrift_transport=None):
        """初始化mysql连接"""
        try:
            self._conn = hive.connect(host=host, port=int(port), username=user, password=passwd, database=database,
                                      config=configuration, auth=auth,
                                      kerberos_service_name=kerberos_service_name, thrift_transport=thrift_transport)
        except Exception as e:
            raise 'Cannot connect to server\n:hive://%s:%s/%s' % (host, port, database)
        self._cursor = self._conn.cursor()

    def fetch_logs(self):
        return self._cursor.fetch_logs()

    def exec(self, sql):
        """执行dml,ddl语句"""
        try:
            self._cursor.execute(sql)
            self._conn.commit()
            return 1
        except:
            self._conn.rollback()
            return 0

    def query(self, sql):
        """查询数据"""
        self._cursor.execute(sql)
        return self._cursor.fetchall()

    def table_rowcnt(self, table):
        """
        统计行数
        """
        self._cursor.execute('select count(*) from %s ' % (table))
        return self._cursor.fetchone()[0]

    def part_rowcnt(self, table, part_key, part_value):
        """
        统计行数
        """
        self._cursor.execute('select count(*) from %s where %s=%s' % (table, part_key, part_value))
        return self._cursor.fetchone()[0]

    def __del__(self):
        """ 关闭连接 """
        # self._conn.close()
        self._cursor.close()

    def close(self):
        """
        关闭连接
        :return:
        """
        self.__del__()

