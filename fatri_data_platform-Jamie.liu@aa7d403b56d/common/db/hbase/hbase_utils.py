#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-10-15
# @Author  : Happiless.zhang (Happiless.zhang@fatritech.com)
# @Version : v_1.0
# @note    : 操作HBase的工具模块
import happybase


HBASE_HOST = 'hadoop-master'
HBASE_PORT = 9090
HBASE_POOL_SIZE = 5
TIMEOUT = 3

__pool = happybase.ConnectionPool(size=HBASE_POOL_SIZE, host=HBASE_HOST, port=HBASE_PORT)


def delete_table(table_name):
    """
    删除指定的表
    :param table_name:      表名
    :return:                无返回
    """
    with __pool.connection(TIMEOUT) as conn:
        conn.delete_table(table_name, True)


def get_table(table_name, column_family, flag=True):
    """
    此方法用于获取table对象，如果flag为True表示创建表，默认为True
    :param table_name:        获取的表名
    :param column_family:     列族名
    :param flag:              是否创建表，默认为True
    :return: table            table对象，方便其他操作使用
    """
    with __pool.connection(TIMEOUT) as conn:
        print(conn)
        if flag:
            try:
                conn.create_table(table_name, {column_family: dict()})
                print("create table success")
            except Exception as e:
                print("table already exists, ", e)

        return conn.table(table_name)


def get_rows(table, row_keys=None):
    """
    用于查询hbase数据，row_keys为rowkey的集合，如果不传rowkey默认全表扫描
    :param table:       table对象
    :param row_keys:    rowkey的集合
    :return:            返回hbase数据记录
    """
    if row_keys:
        if len(row_keys) == 1:
            print(table.row(row_keys[0]))
            return table.row(row_keys[0])
        else:
            print(table.rows(row_keys))
            return table.rows(row_keys)
    else:
        for key, value in table.scan():
            print(key, value)
            return key, value


def put_row(table, column_family, row_key, value_map):
    """
    新增列
    :param table:           table对象
    :param column_family:   列族名
    :param row_key:         rowkey
    :param value_map:       列名和列值的dict
    :return:
    """
    column_value = {}
    for k, v in value_map.items():
        column_value[f"{column_family}:{k}"] = v
    table.put(row_key, column_value)
    print("put success")


def delete_row(table, row_key, column_family=None, keys=None):
    """
    删除列
    :param table:           table对象
    :param row_key:         rowkey
    :param column_family:   列族名
    :param keys:            列名
    :return:
    """
    if keys:
        key_list = [f'{column_family}:{key}' for key in keys]
        table.delete(row_key, key_list)
    else:
        table.delete(row_key)


if __name__ == '__main__':
    table1 = get_table("ods:ODS_S002_FATRI_DEVICE_STATUS", "info", False)
    # put_row(table1, "cf", "3", {"a": "2", "b": "3"})
    # get_rows(table1, row_keys=["3"])
    print(get_rows(table1))

