#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-10-15
# @Author  : Happiless.zhang (Happiless.zhang@fatritech.com)
# @Version : v_1.0
# @note    : 操作HBase的工具模块
import happybase
from conf.config import Config


class HBase(object):

    def __init__(self, host=Config().get_conf("HBase", "hbase.host"),
                 port=int(Config().get_conf("HBase", "hbase.port"))):
        self.conn = happybase.Connection(host=host, port=port)

    def delete_table(self, table_name):
        """
        删除指定的表
        :param table_name:      表名
        :return:                无返回
        """
        self.conn.delete_table(table_name, True)

    def get_all_tables(self):
        tables = self.conn.tables()
        for i in range(len(tables)):
            tables[i] = tables[i].decode("utf-8")
        return tables

    def get_create_table(self, table_name, column_family):
        """
        此方法用于获取table对象，如果flag为True表示创建表，默认为True
        :param table_name:        获取的表名
        :param column_family:     列族名
        :return: table            table对象，方便其他操作使用
        """
        try:
            self.conn.create_table(table_name, {column_family: dict()})
            print("create table success")
        except Exception as e:
            print("table already exists, ", e)

    def get_rows(self, table_name, row_keys=None, row_start=None, row_stop=None, row_prefix=None, limit=10):
        """
        用于查询hbase数据，row_keys为rowkey的集合，如果不传rowkey默认全表扫描
        :param table_name:  获取的表名
        :param row_keys:    rowkey的集合
        :param row_start:   起始的rowkey
        :param row_stop:    结束的rowkey
        :param row_prefix:  rowkey前缀
        :param limit:       分页条数
        :return:            返回hbase数据记录
        """
        result = []
        table = self.conn.table(table_name)
        if row_keys:
            if len(row_keys) == 1:
                row = table.row(row_keys[0])
                data = {}
                for k, v in row.items():
                    field = k.decode("utf-8").split(":")
                    data[field[1]] = str(v.decode("utf-8"))
                result.append(data)
            else:
                rows = table.rows(row_keys)
                for row in rows:
                    data = {"rowkey": row[0].decode("utf-8")}
                    for k, v in row[1].items():
                        field = k.decode("utf-8").split(":")
                        data[field[1]] = str(v.decode("utf-8"))
                    result.append(data)
        else:
            for key, value in table.scan(row_start=row_start, row_stop=row_stop, row_prefix=row_prefix, limit=limit):
                data = {"rowkey": key.decode("utf-8")}
                for k, v in value.items():
                    field = k.decode("utf-8").split(":")
                    data[field[1]] = str(v.decode("utf-8"))
                result.append(data)
        return result

    def put_row(self, table_name, column_family, row_key, value_map):
        """
        新增列
        :param table_name:      获取的表名
        :param column_family:   列族名
        :param row_key:         rowkey
        :param value_map:       列名和列值的dict
        :return:
        """
        column_value = {}
        table = self.conn.table(table_name)
        for k, v in value_map.items():
            column_value[f"{column_family}:{k}"] = str(v)
        table.put(row_key, column_value)
        print("put success")

    def delete_row(self, table_name, row_key, column_family=None, keys=None):
        """
        删除列
        :param table_name:      获取的表名
        :param row_key:         rowkey
        :param column_family:   列族名
        :param keys:            列名
        :return:
        """
        table = self.conn.table(table_name)
        if keys:
            key_list = [f'{column_family}:{key}' for key in keys]
            table.delete(row_key, key_list)
        else:
            table.delete(row_key)

    def close(self):
        self.conn.close()


if __name__ == '__main__':
    HBASE_HOST = 'hadoop-master'
    hbase = HBase()
    # hbase.get_create_table("ods:ODS_S002_FATRI_DEVICE_STATUS", "info")
    # put_row(table1, "cf", "3", {"a": "2", "b": "3"})
    # get_rows(table1, row_keys=["3"])
    print(hbase.get_all_tables())
    hbase.close()
