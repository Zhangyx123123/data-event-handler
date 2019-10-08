from dao.basedao import DaoBase
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, TIMESTAMP
from helper.daohelper import extract_columns, extract_column
import json
from dao.configunitdao import ConfigUnitDao
from dao.modeldao import CcsModelDao
from dao.botdao import CcsBotDao
from helper.abstracthelper import get_abstract


Base = declarative_base()


class CcsConf(Base):
    __tablename__ = 'ccs_conf'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ccs_id = Column(String(64))
    name = Column(String(255))
    conf_units = Column(String(1024))
    status = Column(String(32))
    created_time = Column(TIMESTAMP)
    updated_time = Column(TIMESTAMP)


class CcsConfigDao(DaoBase):
    def __init__(self):
        super().__init__()
        self.config_unit_dao = ConfigUnitDao()
        self.model_dao = CcsModelDao()
        self.bot_dao = CcsBotDao()

    def get_ccs_configs(self, ccs_id=None, status=None):
        with self.get_session() as session:
            cols = [CcsConf.id, CcsConf.ccs_id, CcsConf.name, CcsConf.status, CcsConf.conf_units]
            if status:
                data = self.get_status_records(session, ccs_id, status)
            elif not ccs_id:
                data = self.get_all_active_records(session)
            else:
                data = self.get_records(session, ccs_id)

            all_config_units = self.config_unit_dao.get_all_config_unit()
            res = []
            for row in data:
                ccs_config = extract_columns(row, cols)
                config_units = []
                unit_ids = json.loads(extract_column(row, CcsConf.conf_units))
                for uid in unit_ids:
                    unit = next((x for x in all_config_units if x['id'] == uid), None)
                    if unit['category'] == 'model':
                        self.handle_model(unit)
                    if unit['category'] == 'bot':
                        self.handle_bot(unit)
                    if unit['category'] == 'dispatcher':
                        self.handle_dispatcher(unit)

                    config_units.append(unit)
                ccs_config['config_units'] = config_units
                res.append(ccs_config)
            return res

    def handle_dispatcher(self, unit):
        abstracts = []
        try:
            json_obj = json.loads(unit['content'])
            if 'dispatchers' in json_obj:
                dispatchers = json_obj['dispatchers']
                for d in dispatchers:
                    expr = d['filter']
                    abstract = get_abstract(expr)
                    abstracts.append(abstract)
                unit['abstract'] = abstracts
        except json.JSONDecodeError:
            pass

    def handle_bot(self, unit):
        bot_ids = json.loads(unit['content'])
        if isinstance(bot_ids, list) and len(bot_ids) and isinstance(bot_ids[0], int):
            del unit['content']
            bots = []
            for bid in bot_ids:
                bots.append(self.bot_dao.get_bot(bid))
            unit['bots'] = bots

    def handle_model(self, unit):
        model_ids = json.loads(unit['content'])
        del unit['content']
        models = []
        for mid in model_ids:
            models.append(self.model_dao.get_model(mid))
        unit['models'] = models

    @staticmethod
    def get_records(session, ccs_id):
        return session.query(CcsConf).filter_by(ccs_id=ccs_id)

    @staticmethod
    def get_status_records(session, ccs_id, status):
        return session.query(CcsConf).filter_by(ccs_id=ccs_id, status=status)

    @staticmethod
    def get_all_active_records(session):
        return session.query(CcsConf).filter_by(status='active')

    def add_ccs_config(self, ccs_id, name, conf_units: list, status):
        with self.get_session() as session:
            units = []
            categories = []
            for unit in conf_units:
                categories.append(unit['category'])
                if unit['category'] != 'model' and unit['category'] != 'bot':
                    units.append(self.config_unit_dao.add_config_unit(ccs_id, unit['name'], unit['category'], unit['content']))
                elif unit['category'] == 'model':
                    units.append(self.config_unit_dao.add_config_unit(
                        ccs_id, unit['name'], unit['category'], str(unit['models'])))
                else:
                    units.append(self.config_unit_dao.add_config_unit(
                        ccs_id, unit['name'], unit['category'], str(unit['bots'])))
            self.ensure_default_configs(categories, ccs_id, units)

            config = CcsConf(ccs_id=ccs_id, name=name, status=status, conf_units=str(units))
            session.add(config)
            session.commit()
            return config.id

    def ensure_default_configs(self, categories, ccs_id, units):
        if 'model' not in categories:
            units.append(self.config_unit_dao.add_config_unit(ccs_id, '', 'model', '[]'))
        if 'group' not in categories:
            units.append(self.config_unit_dao.add_config_unit(ccs_id, '', 'group', '[]'))
        if 'bot' not in categories:
            units.append(self.config_unit_dao.add_config_unit(ccs_id, '', 'bot', '[]'))
        if 'dispatcher' not in categories:
            units.append(self.config_unit_dao.add_config_unit(ccs_id, '', 'dispatcher', '{"dispatchers:[]"}'))
        if 'respond_rule' not in categories:
            units.append(self.config_unit_dao.add_config_unit(ccs_id, '', 'respond_rule', '[]'))
        if 'priority_rule' not in categories:
            units.append(self.config_unit_dao.add_config_unit(ccs_id, '', 'priority_rule', '[]'))
        if 'score_rule' not in categories:
            units.append(self.config_unit_dao.add_config_unit(ccs_id, '', 'score_rule', '[]'))

    def update_ccs_config(self, ccs_id, cid, name, conf_units: list, status):
        with self.get_session() as session:
            config = session.query(CcsConf).get(cid)
            assert config is not None
            assert config.ccs_id == ccs_id
            config.name = name
            config.status = status

            for unit in conf_units:
                if unit['category'] != 'model' and unit['category'] != 'bot':
                    self.config_unit_dao.update_config_unit(ccs_id, unit['id'], unit['name'],
                                                            unit['category'], unit['content'])
                elif unit['category'] == 'model':
                    self.config_unit_dao.update_config_unit(ccs_id, unit['id'], unit['name'],
                                                            unit['category'], str(unit['models']))
                else:
                    self.config_unit_dao.update_config_unit(ccs_id, unit['id'], unit['name'],
                                                            unit['category'], str(unit['bots']))
            session.commit()
            return config.id

    def delete_ccs_config(self, ccs_id, cid):
        with self.get_session() as session:
            config = session.query(CcsConf).get(cid)
            assert config is not None
            assert config.ccs_id == ccs_id
            unit_ids = json.loads(config.conf_units)
            units = []
            for uid in unit_ids:
                units.append(self.config_unit_dao.get_by_id(uid))
            for unit in units:
                self.config_unit_dao.delete_config_unit(ccs_id, unit['id'])
            session.delete(config)
            session.commit()

    def activate_ccs_config(self, ccs_id, cid):
        with self.get_session() as session:
            active_config = session.query(CcsConf).filter_by(ccs_id=ccs_id, status='active')
            for row in active_config:
                row.status = 'inactive'
            config = session.query(CcsConf).get(cid)
            assert config.ccs_id == ccs_id
            config.status = 'active'
            session.commit()
