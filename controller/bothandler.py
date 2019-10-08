# -*- coding: utf-8 -*-
import logging
from controller.basehandler import BaseHandler
from service.botservice import BotService
from helper.handlerhelper import parse_args, response_wrapper
from config.constants import MODULE_ROOT
from flask_restful import reqparse


def setup_route(api):
    """
        return map of endpoint and handler
    """
    api.add_resource(BotHandler, MODULE_ROOT + "/bot/<ccs_id>")


class BotHandler(BaseHandler):
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.service = BotService()

    @response_wrapper
    def get(self, ccs_id):
        res = self.service.get_bot(ccs_id)
        return res

    @response_wrapper
    def post(self, ccs_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name')
        parser.add_argument('url')
        parser.add_argument('app_id')
        parser.add_argument('modules', action='append')
        args = parser.parse_args()
        return self.service.add_bot(ccs_id, args['name'], args['url'], args['modules'], args['app_id'])

    @response_wrapper
    def put(self, ccs_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name')
        parser.add_argument('url')
        parser.add_argument('app_id')
        parser.add_argument('id')
        parser.add_argument('modules', action='append')
        args = parser.parse_args()
        return self.service.update_bot(ccs_id, args['id'], args['name'], args['url'], args['modules'], args['app_id'])

    @response_wrapper
    def delete(self, ccs_id):
        args = parse_args(['id'])
        return self.service.delete_bot(ccs_id, args['id'])
