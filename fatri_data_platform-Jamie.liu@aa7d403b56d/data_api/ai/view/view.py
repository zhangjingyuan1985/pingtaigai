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
