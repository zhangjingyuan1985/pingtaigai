#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/10/23 13:38
# @Author  : Jamie.liu
# @Email : Jamie.liu@fatritech.com
# @Version : v_1.0
# @note    : 测试代码
from common.db.hbase.hbase_class import HBase
from data_api.ai.view import ai
from flask import request
import json
from ai_manage import app
from data_api.utils.message import to_dict_msg

@ai.route('/')
def index():
    return "Hello World !!!"


@ai.route('/singleModelLog/')  #
def single_model_log():
    """
    电梯实时热力图接口

    :param: limit       每页条数
    :param: start_row   开始的rowkey前缀
    :return: json
    """
    request_id = request.args.get("requestId")
    request_id_list = []
    request_id_list.append(request_id)
    start_row = request.args.get("start_row")
    hbase = HBase(app.config.get("HBASE_HOST"))
    result = hbase.get_rows("al:al_s003_evt_model_log", row_keys=request_id_list, row_start=start_row)  #
    data = {
        "result": result,
        "total_count": len(result)
    }

    return json.dumps(to_dict_msg(200, data))


@ai.route('/multiModelLog/')
def multi_model_log():
    # startTime,endTime,requestId,subjectCode,modelCode,modelSuccess,isImage,sortField,sort,start_row,limit
    start_time = request.args.get("startTime")
    end_time = request.args.get("endTime")
    subject_id = request.args.get("subjectCode")
    model_id = request.args.get("modelCode")
    is_success = request.args.get("modelSuccess")
    is_image = request.args.get("isImage")
    start_row = request.args.get("start_row")     # 分页起始位置
    limit = request.args.get("limit")             # 分页大小

    table_name = 'al:s003_evt_model_log'
    hbase = HBase(app.config.get("HBASE_HOST"))
    table = hbase.conn.table(table_name)
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
    #     def scan(self, row_start=None, row_stop=None, row_prefix=None,
    #              columns=None, filter=None, timestamp=None,
    #              include_timestamp=False, batch_size=1000, scan_batching=None,
    #              limit=None, sorted_columns=False, reverse=False):
    result = table.scan()

    # result = hbase.get_rows(limit=limit)
    print("")

