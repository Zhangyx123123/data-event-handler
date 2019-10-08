# -*- coding: utf-8 -*-
import logging
from controller.basehandler import BaseHandler
from service.ccsconfservice import ConfigUnitService
from helper.handlerhelper import parse_args, response_wrapper
from config.constants import MODULE_ROOT
from flask_restful import reqparse


def setup_route(api):
    """
        return map of endpoint and handler
    """
    api.add_resource(AllCcsConfigHandler, MODULE_ROOT + "/ccsconf")
    api.add_resource(CcsConfigHandler, MODULE_ROOT + "/ccsconf/<ccs_id>")
    api.add_resource(CcsConfigActivateHandler, MODULE_ROOT + "/ccsconf/<ccs_id>/activate")


class CcsConfigHandler(BaseHandler):
    def __init__(self):
        self.service = ConfigUnitService()

    @response_wrapper
    def get(self, ccs_id):
        args = parse_args(['status'])
        res = self.service.get_ccs_configs(ccs_id, args['status'])
        return res

    @response_wrapper
    def post(self, ccs_id):
        parser = reqparse.RequestParser()
        parser.add_argument('config_units', type=dict, action="append")
        parser.add_argument('name')
        parser.add_argument('status')
        args = parser.parse_args()
        return self.service.add_ccs_config(ccs_id, args['name'], args['config_units'], args['status'])

    @response_wrapper
    def put(self, ccs_id):
        parser = reqparse.RequestParser()
        parser.add_argument('config_units', type=dict, action="append")
        parser.add_argument('name')
        parser.add_argument('status')
        parser.add_argument('id')
        args = parser.parse_args()
        return self.service.update_css_config(ccs_id, args['id'], args['name'], args['config_units'], args['status'])

    @response_wrapper
    def delete(self, ccs_id):
        args = parse_args(['id'])
        return self.service.delete_ccs_config(ccs_id, args['id'])


class CcsConfigActivateHandler(BaseHandler):
    def __init__(self):
        self.service = ConfigUnitService()

    @response_wrapper
    def post(self, ccs_id):
        args = parse_args(['id'])
        return self.service.activate_ccs_config(ccs_id, args['id'])


class AllCcsConfigHandler(BaseHandler):
    def __init__(self):
        self.service = ConfigUnitService()

    @response_wrapper
    def get(self):
        return self.service.all_ccs_config()
