status_msg = {
    200: 'Success',
    500: 'Server internal error',
    404: '404 Not found error'
}


def to_dict_msg(status=200, data=None, msg=None):
    return {
        'status': status,
        'data': data,
        'msg': msg if msg else status_msg.get(status)
    }
