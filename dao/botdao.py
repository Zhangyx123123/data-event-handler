from dao.basedao import DaoBase
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, TIMESTAMP
from helper.daohelper import extract_columns
from dao.configunitdao import ConfigUnit
import json


Base = declarative_base()


class CcsBot(Base):
    __tablename__ = 'ccs_bot'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ccs_id = Column(String(64))
    name = Column(String(255))
    url = Column(String(1024))
    app_id = Column(String(64))
    modules = Column(String(255))
    created_time = Column(TIMESTAMP)
    updated_time = Column(TIMESTAMP)


class CcsBotDao(DaoBase):
    def get_bots(self, ccs_id):
        with self.get_session() as session:
            cols = [CcsBot.id, CcsBot.ccs_id, CcsBot.name, CcsBot.url, CcsBot.modules, CcsBot.app_id]
            data = session.query(CcsBot).filter_by(ccs_id=ccs_id)
            conf = []
            for row in data:
                bot = extract_columns(row, cols)
                if bot['modules']:
                    bot['modules'] = json.loads(bot['modules'])
                else:
                    del bot['modules']
                conf.append(bot)
            return conf

    def get_bot(self, bid):
        with self.get_session() as session:
            cols = [CcsBot.id, CcsBot.ccs_id, CcsBot.name, CcsBot.url, CcsBot.app_id, CcsBot.modules]
            bid = session.query(CcsBot).get(bid)
            bot = extract_columns(bid, cols)
            if bot['modules']:
                bot['modules'] = json.loads(bot['modules'])
            else:
                del bot['modules']
            return bot

    def add_bot(self, ccs_id, name, url, modules, app_id):
        if not modules:
            modules = []
        with self.get_session() as session:
            bot = CcsBot(ccs_id=ccs_id, name=name, url=url, app_id=app_id, modules=json.dumps(modules))
            session.add(bot)
            session.commit()
            return bot.id

    def update_bot(self, ccs_id, bid, name, url, modules, app_id):
        if not modules:
            modules = []
        with self.get_session() as session:
            config = session.query(CcsBot).get(bid)
            assert config.ccs_id == ccs_id
            if name != config.name:
                self.update_group(session, ccs_id, config.name, name)
            config.name = name
            config.url = url
            config.app_id = app_id
            config.modules = json.dumps(modules)
            session.commit()
            return config.id

    def update_group(self, session, ccs_id, old_name, new_name):
        group_config_units = session.query(ConfigUnit).filter_by(ccs_id=ccs_id, category='group')
        for group_config_unit in group_config_units:
            content = json.loads(group_config_unit.content)
            for group in content:
                bots = group['bots']
                if isinstance(bots[0], str):
                    if old_name in bots:
                        bots.remove(old_name)
                        bots.append(new_name)
                if isinstance(bots[0], dict):
                    for bot in bots:
                        if 'name' in bot and bot['name'] == old_name:
                            bot['name'] = new_name
            group_config_unit.content = json.dumps(content, ensure_ascii=False)
        session.commit()

    def delete_bot(self, ccs_id, bid):
        with self.get_session() as session:
            config = session.query(CcsBot).get(bid)
            assert config.ccs_id == ccs_id
            bot_config_units = session.query(ConfigUnit).filter_by(ccs_id=ccs_id, category='bot')
            for unit in bot_config_units:
                content = json.loads(unit.content)
                if isinstance(content, list):
                    bid = int(bid)
                    if bid in content:
                        content.remove(bid)
                        unit.content = json.dumps(content)
            session.delete(config)
            session.commit()
