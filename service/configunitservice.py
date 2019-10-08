from dao.configunitdao import ConfigUnitDao
from helper.servicehelper import handle_exception


class ConfigUnitService:
    def __init__(self):
        self.dao = ConfigUnitDao()

    @handle_exception
    def get_config_unit(self, ccs_id):
        data = self.dao.get_config_unit(ccs_id)
        return {
            'status': 'success',
            'message': '',
            'config_units': data
        }

    @handle_exception
    def get_by_category(self, ccs_id, category):
        data = self.dao.get_by_category(ccs_id, category)
        return {
            'status': 'success',
            'message': '',
            'config_units': data
        }

    @handle_exception
    def add_config_unit(self, ccs_id, name, category, content):
        cid = self.dao.add_config_unit(ccs_id, name, category, content)
        return {
            'status': 'success',
            'message': '',
            'config_unit_id': cid
        }

    @handle_exception
    def update_config_unit(self, ccs_id, cid, name, category, content):
        cid = self.dao.update_config_unit(ccs_id, cid, name, category, content)
        return {
            'status': 'success',
            'message': '',
            'config_unit_id': cid
        }

    @handle_exception
    def delete_config_unit(self, cid, ccs_id):
        self.dao.delete_config_unit(cid, ccs_id)
        return {
            'status': 'success',
            'message': '',
        }
