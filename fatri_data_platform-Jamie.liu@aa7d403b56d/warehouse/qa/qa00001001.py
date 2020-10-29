#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-09-24 14:27:28
# @Author  : Xinhuabu (Huabu.xin@fatritech.com)
# @Link    : ${link}
# @Version : $Id$
# @example : python qa00001001.py 20201001

import os, sys, datetime, logging

from common.db.mysql.mysql_class import Mysql
from common.os.time_utils import get_time
from common.log.log import log

end_time = utime = datetime.datetime.now()
udate = datetime.date.today()

__test_case_note = """
稽核规则：001001 逻辑校验--数据一致性校验
数据流向：mysql.fatri_community -> hive.ods.s002_biz_fatri_community_d
比对方式：mysql源表统计行数，hive统计hdfs数据文件行数（统计文件行数很快，hive的聚合统计很慢）
其他说明：目前日志是打印到日志文件里的，以后要改成写入数据库
"""

__test_case_dict = {
    "test_case_id": "qa00001001",  # 测试用例ID,现状是没有测试用例ID，那就用调度任务ID吧
    "module_name": "fatri_data_platform-warehouse-ods",  # 一级模块-二级子模块-三级模块-四级模块
    "test_case_title": "梯联网小区信息表数据一致性校验",  # 用例名称
    "test_case_level": "1",  # 用例等级
    "pre_condition": "ods层s002_biz_fatri_community_d表当前日期分区加载完成",  # 预置条件
    "operate_step": "1、获取mysql源表数据量 2、获取ods层hdfs数据文件当前分区行数 3、比对1和2的结果",  # 操作步骤
    "expected_res": "相等"  # 预期结果
}


def main():
    '''
    :step:
        1、环境初始化
        2、预置条件实现
        3、用例操作
        4、结果比对
    '''

    res1 = 'sudo -u %s hadoop fs -cat %s%s.db/%s/%s=%s/* |wc -l' % (
        sudoer_, hive_warehouse_path_, target_db_, target_table_.lower(), partition_key_, partition_value_)
    mysql_query = mysql_ins.query('select count(*) from %s;' % (source_table.lower()))
    res2 = mysql_query[0][0]

    if res1 == res2:
        status_dict_['STEP_STATUS'], status_dict_['OUTPUT'], status_dict_['END_TIME'], status_dict_['DURING'] = \
            '999', "Finish!" % (log_file), end_time, dur_time
        mysql_log.insert(log_table, status_dict_, 'insert')
    else:
        status_dict_['STEP_STATUS'], status_dict_['OUTPUT'] = '-1', '数据量不一致！'
        mysql_log.insert(log_table, status_dict_, 'insert')


if __name__ == '__main__':
    ##########环境初始化###########
    yesterday = datetime.date.today() + datetime.timedelta(-1)
    # partition_value = sys.argv[1] if sys.argv[1] else yesterday.replace('-', '')
    partition_value = yesterday  # .replace('-','')

    log_table = 't_qa_log'  # 还没建表
    log_file = '/Fatri/warehouse/logs/%s_%s.log' % (sys.argv[0][:-3], utime)
    logging.basicConfig(level=logging.INFO,  # 控制台打印的日志级别
                        filename=log_file,
                        filemode='w',  # 模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志 a是追加模式，默认如果不写的话，就是追加模式
                        format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'  # 日志格式
                        )

    ##########用例信息初始化##############
    # mysql环境参数
    db_host = '172.16.8.11'
    db_port = 3306
    db_user = 'data_platform'
    db_passwd = 'data#platform'
    db_dbname = 'data_platform'
    db_charset = 'utf-8'

    # 实例化mysql连接
    mysql_ins = Mysql(db_host, db_port, db_user, db_passwd, db_dbname, db_charset)

    # 大数据环境初始化
    sudoer_ = 'hdfs'
    partition_key_ = 'day_id'
    hive_warehouse_path_ = '/user/hive/warehouse/'
    source_db_ = db_dbname
    source_table_ = 'fatri_community'
    target_db_ = 'ods'
    target_table_ = 's002_biz_fatri_community_d'

    # 状态信息 写入日志
    status_dict_ = {'DATE_ID': partition_value,
                    'QA_ID': __test_case_dict['test_case_id'],
                    'PROC_FILE': os.path.basename(__file__),
                    'TARGET_DB': target_db_.upper(),
                    'TARGET_TABLE': target_table_.upper(),
                    'STEP_STATUS': '0',
                    'START_TIME': utime,
                    'END_TIME': end_time,
                    'DURING': '0',
                    'OUTPUT': 'initialize success!',
                    'CREATE_BY': 'FU1098',
                    'CREATE_TIME': end_time}

    # 插入日志
    mysql_log.insert(log_table, status_dict_, 'insert')

    log('<===qa00001001.py begin at %s===>' % (utime))

    try:
        main()
    except:
        err_detail(log_file)
        status_dict_['STEP_STATUS'], status_dict_['OUTPUT'], status_dict_['END_TIME'], status_dict_['DURING'] = \
            '-1', "ERROR: message in %s " % (log_file), end_time, dur_time
        mysql_log.insert(log_table, status_dict_, 'insert')

    end_time, dur_time = get_time(utime)
    log('<===qa00001001.py end at %s===>' % (end_time))