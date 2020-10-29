#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-08-13 11:11:22
# @Author  : Xinhuabu
# @Link    : ${link}
# @Version : $Id$

import os


def dos2unix(file_):
    try:
        hql_file = open(file_, 'r+')
        lines = hql_file.readlines()
        hql_file.seek(0, 0)
        hql_file.truncate()
        for line in lines:
            line = line.replace('\r\n', '\n')
            hql_file.write(line)
    except Exception as e:
        raise e


# 生成建表语句
def create_write(create_path, create_list, fname='table'):
    create_file = '%s%s.create' % (create_path, fname)
    if not os.path.exists(create_path):
        os.makedirs(create_path)

        # 建表语句去重
    create_set = set(create_list)
    with open('%s' % (create_file), 'w') as create_table:
        for create_hql in create_set:
            try:
                # 这里生成文件 用覆盖的方式
                # create_table.write(create_hql)
                create_table.writelines(create_hql)
                log('<===file:%s ===>' % (create_path), 'info')
            except IOError:
                log('<===file:%s write error!===>' % (create_file), 'error')
                raise IOError
            except Exception as e:
                raise e

    dos2unix(create_file)


def sql_write(sql_path, v_table, v_sql, sql_type='hql'):
    sql_file = '%s%s.%s' % (sql_path, v_table.lower(), sql_type)

    try:
        if not os.path.exists(sql_path):
            os.makedirs(sql_path)

            # 这里生成文件 用覆盖的方式
        sql_file_ = open(sql_file, 'w')
        sql_file_.writelines(v_sql)
    except IOError:
        raise IOError
    except Exception as e:
        raise e
    finally:
        sql_file_.close()

    dos2unix(sql_file)


