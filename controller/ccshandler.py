# -*- coding: utf-8 -*-
import logging

from controller.basehandler import BaseHandler
from service.ccsservice import CcsService


MODULE_ROOT = "/ccsDal"


def setup_route(api):
    """
        return map of endpoint and handler
    """
    api.add_resource(CcsHandler, MODULE_ROOT + "/ccs/<ccs_id>")


class CcsHandler(BaseHandler):
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.service = CcsService()

    def get(self, ccs_id):
        return self.service.get_ccs(ccs_id)

    def post(self, ccs_id):
        pass

    def delete(self, ccs_id):
        pass

    def put(self, ccs_id):
        pass
