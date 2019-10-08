from dao.botdao import CcsBotDao
from helper.servicehelper import handle_exception


class BotService:
    def __init__(self):
        self.dao = CcsBotDao()

    @handle_exception
    def get_bot(self, ccs_id):
        data = self.dao.get_bots(ccs_id)
        return {
            'status': 'success',
            'message': '',
            'bots': data
        }

    @handle_exception
    def add_bot(self, ccs_id, name, url, modules, app_id):
        bid = self.dao.add_bot(ccs_id, name, url, modules, app_id)
        return {
            'status': 'success',
            'message': '',
            'id': bid
        }

    @handle_exception
    def update_bot(self, ccs_id, bid, name, url, modules, app_id):
        bid = self.dao.update_bot(ccs_id, bid, name, url, modules, app_id)
        return {
            'status': 'success',
            'message': '',
            'id': bid
        }

    @handle_exception
    def delete_bot(self, ccs_id, bid):
        self.dao.delete_bot(ccs_id, bid)
        return {
            'status': 'success',
            'message': '',
        }
