from dao.ccsconfdao import CcsConfigDao
from helper.servicehelper import handle_exception


class ConfigUnitService:
    def __init__(self):
        self.dao = CcsConfigDao()

    @handle_exception
    def get_ccs_configs(self, ccs_id, status):
        data = self.dao.get_ccs_configs(ccs_id, status)
        return {
            'status': 'success',
            'message': '',
            'configs': data
        }

    @handle_exception
    def add_ccs_config(self, ccs_id, name, conf_units, status):
        data = self.dao.add_ccs_config(ccs_id, name, conf_units, status)
        return {
            'status': 'success',
            'message': '',
            'id': data
        }

    @handle_exception
    def update_css_config(self, ccs_id, cid, name, conf_units, status):
        data = self.dao.update_ccs_config(ccs_id, cid, name, conf_units, status)
        return {
            'status': 'success',
            'message': '',
            'id': data
        }

    @handle_exception
    def delete_ccs_config(self, ccs_id, cid):
        self.dao.delete_ccs_config(ccs_id, cid)
        return {
            'status': 'success',
            'message': ''
        }

    @handle_exception
    def activate_ccs_config(self, ccs_id, cid):
        self.dao.activate_ccs_config(ccs_id, cid)
        return {
            'status': 'success',
            'message': ''
        }

    @handle_exception
    def all_ccs_config(self):
        data = self.dao.get_ccs_configs()
        return {
            'status': 'success',
            'message': '',
            'configs': data
        }
