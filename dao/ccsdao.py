from dao.basedao import DaoBase


class CcsDao(DaoBase):
    def get_ccs(self, ccs_id):
        statement = "select uuid, name, user_id from ccs where uuid='{}'".format(ccs_id)
        results = self.execute_search(self.db_engine, statement, {})
        rs_data = []
        for row in results:
            item = {
                "id": row["uuid"],
                "name": row["name"],
                "user_id": row["user_id"],
            }
            rs_data.append(item)
        return rs_data
