from dao.modeldao import CcsModelDao
from helper.servicehelper import handle_exception


class ModelService:
    def __init__(self):
        self.dao = CcsModelDao()

    @handle_exception
    def get_model(self, ccs_id):
        data = self.dao.get_models(ccs_id)
        return {
            'status': 'success',
            'message': '',
            'models': data
        }

    @handle_exception
    def add_model(self, ccs_id, name, url, method, category):
        mid = self.dao.add_model(ccs_id, name, url, method, category)
        return {
            'status': 'success',
            'message': '',
            'id': mid
        }

    @handle_exception
    def update_model(self, ccs_id, mid, name, url, method, category):
        mid = self.dao.update_model(ccs_id, mid, name, url, method, category)
        return {
            'status': 'success',
            'message': '',
            'id': mid
        }

    @handle_exception
    def delete_model(self, ccs_id, mid):
        self.dao.delete_model(ccs_id, mid)
        return {
            'status': 'success',
            'message': '',
        }
