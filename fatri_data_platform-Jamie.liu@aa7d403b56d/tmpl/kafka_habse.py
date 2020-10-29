#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-10-15 11:45:01
# @Author  : Happiless.zhang (Happiless.zhang@fatritech.com)
# @Version : v_1.0
# @note    : 读取Kafka数据并写入HBase模板
from common.channel.kafka_utils import read_kafka
from common.db.hbase.hbase_utils import get_table, put_row
import json


CONSUMER_TOPIC = "example"
PRODUCER_TOPIC = "ODS-S002-FATRI-DEVICE-STATUS"
SOURCE_TABLE_NAME = "fatri_device_status"
TARGET_TABLE_NAME = "ods:ODS_S002_FATRI_DEVICE_STATUS"
COLUMN_FAMILY = "info"
ROW_KEY = "StatusId"


def main():


    # 1.获取table对象
    table = get_table(TARGET_TABLE_NAME, COLUMN_FAMILY)
    # 2.读取kafka
    consumer = read_kafka(topic=CONSUMER_TOPIC)
    for message in consumer:
        data = json.loads(message.value)
        if data['table'] == SOURCE_TABLE_NAME:
            obj = data['data'][0]
            row_key = obj[ROW_KEY]
            # 2.写入hbase
            put_row(table, COLUMN_FAMILY, row_key, dict(obj))


if __name__ == '__main__':
    main()


