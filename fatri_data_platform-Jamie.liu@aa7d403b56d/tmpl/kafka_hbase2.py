#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-10-15 11:45:01
# @Author  : Happiless.zhang (Happiless.zhang@fatritech.com)
# @Version : v_1.0
# @note    : 读取Kafka数据并写入HBase模板
from common.channel.kafka_class import Kafka
from common.db.hbase.hbase_class import HBase
import json

CONSUMER_TOPIC = "ODS-S002-FATRI-DEVICE-STATUS"
PRODUCER_TOPIC = "ODS-S002-FATRI-DEVICE-STATUS"
SOURCE_TABLE_NAME = "fatri_device_status"
TARGET_TABLE_NAME = "ods:ODS_S002_FATRI_DEVICE_STATUS"
COLUMN_FAMILY = "info"
ROW_KEY = "StatusId"


def main():
    # 1.获取Kafka对象
    kafka = Kafka()
    # 2.读取Kafka数据
    consumer = kafka.read_kafka(CONSUMER_TOPIC)
    # 3.获取HBase对象
    hbase = HBase()
    # 4.创建HBase表
    hbase.get_create_table(TARGET_TABLE_NAME, COLUMN_FAMILY)

    for message in consumer:
        try:
            data = json.loads(message.value)
            print(data)
        except Exception as e:
            print(e)
            continue
        # obj = data[TARGET_TABLE_NAME][0]
        # row_key = obj[ROW_KEY]
        # 5.写入HBase
        # hbase.put_row(TARGET_TABLE_NAME, COLUMN_FAMILY, row_key, dict(obj))
        # 6.写入Kafka
        # message = json.dumps({TARGET_TABLE_NAME: obj})
        # kafka.write_kafka(PRODUCER_TOPIC, message)
        kafka.update_offset(message)

    hbase.close()


if __name__ == '__main__':
    main()


