#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-10-15 11:45:01
# @Author  : Happiless.zhang (Happiless.zhang@fatritech.com)
# @Version : v_1.0
# @note    : 读取Kafka数据并写入HBase模板
from common.channel.kafka_class import Kafka

CONSUMER_TOPIC = "test123"
PRODUCER_TOPIC = "ODS-S002-FATRI-DEVICE-STATUS"
SOURCE_TABLE_NAME = "fatri_device_status"
TARGET_TABLE_NAME = "ods:ODS_S002_FATRI_DEVICE_STATUS"
COLUMN_FAMILY = "info"
ROW_KEY = "StatusId"


def main():
    # 1.获取Kafka对象
    kafka = Kafka(group_id="DP1")
    # 2.读取Kafka数据
    # consumer = kafka.read_kafka(CONSUMER_TOPIC)
    for i in range(100):
        print(i)
        kafka.write_kafka(CONSUMER_TOPIC, f"message_{i}")
    print("end")
    # 3.获取HBase对象
    # hbase = HBase()
    # # 4.创建HBase表
    # hbase.get_create_table(TARGET_TABLE_NAME, COLUMN_FAMILY)
    #
    # for message in consumer:
    #     try:
    #         data = json.loads(message.value)
    #         # if data['table'] != SOURCE_TABLE_NAME:
    #         #     continue
    #         print(data)
    #         # kafka.update_offset(message)
    #     except Exception as e:
    #         print(e)
    #         continue
        # if data['table'] == SOURCE_TABLE_NAME:
        #     obj = data['data'][0]
        #     row_key = obj[ROW_KEY]
        #     # 5.写入HBase
        #     hbase.put_row(TARGET_TABLE_NAME, COLUMN_FAMILY, row_key, dict(obj))
        #     # 6.写入Kafka
        #     message = json.dumps({TARGET_TABLE_NAME: obj})
        #     kafka.write_kafka(PRODUCER_TOPIC, message)

    # hbase.close()


if __name__ == '__main__':
    main()


