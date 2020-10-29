import json

from flask import request

from common.channel.kafka_class import Kafka
from data_api.common.view import common
from data_api.utils.message import to_dict_msg


@common.route('/writeKafka/')
def write_kafka():
    topic = request.args.get("topic")
    message = request.args.get("message")
    if not topic or not message:
        return to_dict_msg(status=200, msg="write kafka failed, topic and message can not empty")
    try:
        kafka = Kafka()
        kafka.write_kafka(topic, json.loads(message))
        return to_dict_msg(status=200, msg="write kafka success")
    except Exception as e:
        print(e)
        return to_dict_msg(status=500)