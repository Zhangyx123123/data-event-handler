# -*- coding: utf-8 -*-
import logging

from controller.basehandler import BaseHandler
from service.configunitservice import ConfigUnitService
from helper.handlerhelper import parse_args, response_wrapper
from config.constants import MODULE_ROOT


def setup_route(api):
    """
        return map of endpoint and handler
    """
    api.add_resource(ConfigUnitHandler, MODULE_ROOT + "/confunit/<ccs_id>")


class ConfigUnitHandler(BaseHandler):
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.service = ConfigUnitService()

    @response_wrapper
    def get(self, ccs_id):
        args = parse_args(['category'])
        if args['category']:
            res = self.service.get_by_category(ccs_id, args['category'])
        else:
            res = self.service.get_config_unit(ccs_id)
        return res

    @response_wrapper
    def post(self, ccs_id):
        args = parse_args(['name', 'category', 'content'])
        return self.service.add_config_unit(ccs_id, args['name'], args['category'], args['content'])

    @response_wrapper
    def delete(self, ccs_id):
        args = parse_args(['id'])
        return self.service.delete_config_unit(args['id'], ccs_id)

    @response_wrapper
    def put(self, ccs_id):
        args = parse_args(['id', 'name', 'category', 'content'])
        return self.service.update_config_unit(ccs_id, args['id'], args['name'], args['category'], args['content'])


