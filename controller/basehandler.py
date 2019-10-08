# -*- coding: utf-8 -*-
import json

from flask_restful import Resource
from flask import Response, request


class BaseHandler(Resource):
    def options(self):
        return self.get_response({}, 200)

    @staticmethod
    def check_cors(rsp):
        if 'HTTP_ORIGIN' in request.environ.keys():
            rsp.headers["Access-Control-Allow-Origin"] = request.environ['HTTP_ORIGIN']
            rsp.headers["Access-Control-Allow-Methods"] = "*"
            rsp.headers["Access-Control-Max-Age"] = "86400"
            rsp.headers["Access-Control-Allow-Headers"] = "Authorization,Origin,Content-Type,Accept"
        return rsp

    def get_response(self, json_obj, status):
        rsp = Response(json.dumps(json_obj), status=status, mimetype="application/json; encoding = utf8")
        rsp = self.check_CORS(rsp)
        return rsp
