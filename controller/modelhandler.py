# -*- coding: utf-8 -*-
import logging
from controller.basehandler import BaseHandler
from service.modelservice import ModelService
from helper.handlerhelper import parse_args, response_wrapper
from config.constants import MODULE_ROOT


def setup_route(api):
    """
        return map of endpoint and handler
    """
    api.add_resource(ModelHandler, MODULE_ROOT + "/model/<ccs_id>")


class ModelHandler(BaseHandler):
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.service = ModelService()

    @response_wrapper
    def get(self, ccs_id):
        res = self.service.get_model(ccs_id)
        return res

    @response_wrapper
    def post(self, ccs_id):
        args = parse_args(['name', 'url', 'method', 'category'])
        return self.service.add_model(ccs_id, args['name'], args['url'], args['method'], args['category'])

    @response_wrapper
    def put(self, ccs_id):
        args = parse_args(['id', 'name', 'url', 'method', 'category'])
        return self.service.update_model(ccs_id, args['id'], args['name'], args['url'], args['method'], args['category'])

    @response_wrapper
    def delete(self, ccs_id):
        args = parse_args(['id'])
        return self.service.delete_model(ccs_id, args['id'])
