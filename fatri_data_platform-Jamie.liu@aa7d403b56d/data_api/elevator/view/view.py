from common.db.hbase.hbase_class import HBase
from data_api.elevator.view import elevator
from flask import request
import json
from elevator_manage import app
from data_api.utils.message import to_dict_msg


@elevator.route('/')
def index():
    return "Hello World !!!"


@elevator.route('/heatMap/')
def get_heat_map():
    """
    电梯实时热力图接口

    :param: limit       每页条数
    :param: start_row   开始的rowkey前缀
    :return: json
    """
    limit = int(request.args.get("limit") if request.args.get("limit") else 10)
    start_row = request.args.get("start_row")
    hbase = HBase(app.config.get("HBASE_HOST"))
    result = hbase.get_rows("ads:ELEVATOR_ELEVATOR_TTL_MAP", row_start=start_row, limit=limit)
    data = {
        "result": result,
        "total_count": len(result)
    }

    return json.dumps(to_dict_msg(200, data))

