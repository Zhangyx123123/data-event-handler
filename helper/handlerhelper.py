import logging
import json
from flask_restful import reqparse
from flask import Response


def parse_args(arg_names):
    parser = reqparse.RequestParser()
    for arg in arg_names:
        parser.add_argument(arg)
    return parser.parse_args()


def response_wrapper(func):
    def wrapper(*args, **kwargs):
        try:
            # logging.info("request {} [HttpMethod:{}]: Path: {} Body: {}"
            #              .format(str(func), func.__name__.upper(), request.path, request.data.decode('utf-8')))
            res = func(*args, **kwargs)
            if not res:
                status = 500
            elif res['status'] == 'success':
                status = 200
            elif res['status'] == 'fail':
                status = 500
            else:
                status = 400
        except Exception as e:
            message = str(e)
            status = 500
            res = {'status': 'fail', 'message': message}
            logging.error("exception in {}.{}: {}".format(str(func), func.__name__, message))
        return Response(json.dumps(res), mimetype="application/json", status=status)

    return wrapper
