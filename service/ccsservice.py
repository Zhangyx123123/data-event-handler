from dao.ccsdao import CcsDao


class CcsService:
    def __init__(self):
        self.dao = CcsDao()

    def get_ccs(self, ccs_id):
        try:
            data = self.dao.get_ccs(ccs_id)
            return {
                'status': 'success',
                'message': '',
                'ccs': data
            }
        except Exception as e:
            return {
                'status': 'fail',
                'message': 'Other Error: %s' % str(e),
            }
