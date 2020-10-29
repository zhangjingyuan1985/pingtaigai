#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-08-15 13:39:38
# @Author  : Xinhuabu (Huabu.xin@fatritech.com)
# @Link    : ${link}
# @Version : $Id$


# 读取配置文件
def conf_read(conf_file, separator=':='):
    table_map_dict = {}
    try:
        for line in open(conf_file):
            if line.find(separator) > 0:
                map_strs = line.replace('\n', '').split(separator)
                key = map_strs[0].strip()
                value = map_strs[1].strip()  # .encode('utf-8')
                table_map_dict[key] = value
    except Exception as e:
        raise e
    return table_map_dict


# 读取小文件
def small_file_read(file):
    file_str_ = ''
    try:
        f_ = open(file, 'r')
        file_str_ = f_.read()
    except Exception as e:
        raise e
    finally:
        f_.close()

    return file_str_


def json_read():
    pass


def csv_read():
    pass


if __name__ == '__main__':
    table_map_dict = conf_read("../../conf/s002/s002_hbase.conf").get("HBASE_HOST")
    print(table_map_dict)