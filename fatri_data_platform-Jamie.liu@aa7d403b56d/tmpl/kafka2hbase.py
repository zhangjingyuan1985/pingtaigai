import json
from common.channel.kafka_class import Kafka
from common.db.hbase.hbase_class import HBase

CONSUMER_TOPIC = "DP-S003-EVT-MODEL-LOG-R1P1"
SINGLE_TARGET_TABLE_NAME = "al:s003_evt_model_log"
INDEX_TARGET_TABLE_NAME = "al:s003_evt_model_log_index"
STATS_TARGET_TABLE_NAME = "al:s003_evt_model_log_stats"
COLUMN_FAMILY = "info"

SINGLE_ROW_KEY = "requestId"
STATS_ROW_KEY_MODEL_CODE = "modelCode"
# STATS_ROW_KEY_MODEL_ID = "modelId"
STATS_ROW_KEY_TIMESTAMP = "timestamp"
# STATS_ROW_KEY_SUBJECT_ID = "subjectId"
STATS_ROW_KEY_SUBJECT_CODE = "subjectCode"


def main():
    # 1.获取Kafka对象
    kafka = Kafka(group_id='DP3')
    print('1')
    # 2.读取Kafka数据
    consumer = kafka.read_kafka(CONSUMER_TOPIC)

    # 3.获取HBase对象
    hbase = HBase()
    # 4.创建HBase表
    hbase.get_create_table(SINGLE_TARGET_TABLE_NAME, COLUMN_FAMILY)
    hbase.get_create_table(INDEX_TARGET_TABLE_NAME, COLUMN_FAMILY)
    hbase.get_create_table(STATS_TARGET_TABLE_NAME, COLUMN_FAMILY)

    # modelSuccess 改成 isSuccess。内容要转义  True->1 ,False->0
    for msg in consumer:
        try:
            data = json.loads(msg.value)
            # modelSuccess 改成 isSuccess
            data["isSuccess"] = '1' if data["modelSuccess"] else '0'
            del data["modelSuccess"]

            print('2')

            row_key_model_code = data[STATS_ROW_KEY_MODEL_CODE]
            row_key_timestamp = data[STATS_ROW_KEY_TIMESTAMP]
            row_key_subject_code = data[STATS_ROW_KEY_SUBJECT_CODE]
            log_time_cost = data["timeCost"]  # 响应时长

            row_key_model_code = row_key_model_code[::-1]

            row_key_single = data[SINGLE_ROW_KEY]
            # 模型编码5+用户标识符18+时间戳13=36位
            row_kwy_stats = row_key_model_code + row_key_subject_code + row_key_timestamp

            result = hbase.get_rows(STATS_TARGET_TABLE_NAME, row_prefix=row_key_model_code + row_key_subject_code)
            print('3')
            if result:
                # 表中已有记录
                print('4')
                tmp_data = result[len(result) - 1]
                # 更新callDate、callTimes、successTimes、sumTime
                tmp_data["callDate"], tmp_data["callTimes"], tmp_data["successTimes"], tmp_data["sumTime"] = \
                    row_key_timestamp, \
                    str(int(tmp_data["callTimes"]) + 1), \
                    str(int(tmp_data["successTimes"]) + 1) if int(data["isSuccess"]) else tmp_data["successTimes"], \
                    str(int(tmp_data["sumTime"]) + log_time_cost)
                print("tmp_data: ", tmp_data)
                hbase.put_row(STATS_TARGET_TABLE_NAME, COLUMN_FAMILY, row_kwy_stats, tmp_data)
                print('5')
            else:
                # 表中没有记录，日志统计表数据初始化
                print('6')
                tmp_data = {"callDate": row_key_timestamp,
                            "subjectCode": row_key_subject_code,
                            "subjectName": data["subjectName"],
                            "subjectType": data["subjectType"],
                            "modelCode": row_key_model_code,
                            "modelName": data["modelName"],
                            "callTimes": '0',
                            "successTimes": '0',
                            "sumTime": '0'}
                hbase.put_row(STATS_TARGET_TABLE_NAME, COLUMN_FAMILY, row_kwy_stats, tmp_data)
                print('7')

        except Exception as e:
            print(e)
            continue
        # 5.写入HBase
        # STEP1: 全部数据写进hbase al:s003_evt_model_log表中
        hbase.put_row(SINGLE_TARGET_TABLE_NAME, COLUMN_FAMILY, row_key_single, data)
        kafka.update_offset(msg)
        print('8')


if __name__ == '__main__':
    main()
