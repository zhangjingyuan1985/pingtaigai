#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-08-13 13:23:29
# @Author  : Xinhuabu
# @Link    : ${link}
# @Version : $Id$

import os
import pymysql


class Mysql(object):

    def __init__(self, host, port, user, passwd, database, charset='utf8'):
        """初始化mysql连接"""
        try:
            self._conn = pymysql.connect(host, user, passwd, database, int(port))
        except pymysql.Error as e:
            errormsg = 'Cannot connect to server\nERROR(%s):%s' % (e.args[0], e.args[1])
            print(errormsg)
        self._cursor = self._conn.cursor()

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

    def select(self, table, column='*', condition=''):
        """
        查询数据库方法
        :param table: 库里面的表
        :param column: 列字段
        :param condition: 条件语句 （where id=1）
        :return:
        """
        condition = ' where ' + condition if condition else None
        if condition:
            v_sql_ = "select %s from %s %s" % (column, table, condition)
            # print(sql)
        else:
            v_sql_ = "select %s from %s" % (column, table)
            # print(sql)
        self.query(v_sql_)
        return self._cursor.fetchall()

    def insert(self, table, tdict, type_='replace'):
        """
        插入数据库方法，replace去重插入  insert不去重插入
        :param table: 表名
        :param tdict: 要插入的字典
        :return:
        """
        column = ''
        value = ''
        for key in tdict:
            column += ',' + key
            value += "','" + tdict[key]
        column = column[1:]
        value = value[2:] + "'"
        # replace去重 insert不去重
        v_sql_ = "replace into %s(%s) values(%s)" % (
        table, column, value) if type_ == 'replace' else "insert into %s(%s) values(%s)" % (table, column, value)

        self.exec(v_sql_)
        return self._cursor.lastrowid, self.affected_num()

    def update(self, table, tdict, condition=''):
        """
        更新数据库方法
        :param table: 表名
        :param tdict: 更新数据库数据字典
        :param condition: 条件语句 （where id=1）
        :return:
        """
        value = ''
        if not condition:
            exit()
        else:
            condition = 'where ' + condition

        for key in tdict:
            value += ",%s='%s'" % (key, tdict[key])

        # value = value[1:]
        v_sql_ = "update %s set %s %s" % (table, value[1:], condition)
        # print(sql)
        self._cursor.execute(v_sql_)
        self._conn.commit()
        return self.affected_num()

    def delete(self, table, condition=''):
        """
        删除方法
        :param table: 表名
        :param condition: 条件语句 （where id=1）
        :return:
        """
        condition = ' where ' + condition if condition else None
        v_sql_ = "delete from %s %s" % (table, condition)
        self._cursor.execute(v_sql_)
        self._conn.commit()
        return self.affected_num()

    def affected_rows(self):
        """
        受影响的条数
        :return:
        """
        return self._cursor.rowcount

    def __del__(self):
        """ 关闭mysql连接 """
        self._conn.close()
        self._cursor.close()

    def close(self):
        """
        关闭连接
        :return:
        """
        self.__del__()