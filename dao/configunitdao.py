from dao.basedao import DaoBase
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, TIMESTAMP, TEXT
from helper.daohelper import extract_columns


Base = declarative_base()


class ConfigUnit(Base):
    __tablename__ = 'conf_unit'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ccs_id = Column(String(64))
    name = Column(String(255))
    category = Column(String(32))
    content = Column(TEXT)
    created_time = Column(TIMESTAMP)
    updated_time = Column(TIMESTAMP)


class ConfigUnitDao(DaoBase):
    def get_by_category(self, ccs_id, category):
        cols = [ConfigUnit.ccs_id, ConfigUnit.name, ConfigUnit.category, ConfigUnit.content]
        with self.get_session() as session:
            data = session.query(ConfigUnit).filter_by(ccs_id=ccs_id, category=category)
            conf = []
            for row in data:
                conf.append(extract_columns(row, cols))
            return conf

    def get_all_config_unit(self):
        with self.get_session() as session:
            cols = [ConfigUnit.id, ConfigUnit.ccs_id, ConfigUnit.name, ConfigUnit.category, ConfigUnit.content]
            data = session.query(ConfigUnit).all()
            conf = []
            for row in data:
                conf.append(extract_columns(row, cols))
            return conf

    def get_config_unit(self, ccs_id):
        with self.get_session() as session:
            cols = [ConfigUnit.ccs_id, ConfigUnit.name, ConfigUnit.category, ConfigUnit.content]
            data = session.query(ConfigUnit).filter_by(ccs_id=ccs_id)
            conf = []
            for row in data:
                conf.append(extract_columns(row, cols))
            return conf

    def add_config_unit(self, ccs_id, name, category, content):
        with self.get_session() as session:
            config = ConfigUnit(ccs_id=ccs_id, name=name, category=category, content=content)
            session.add(config)
            session.commit()
            return config.id

    def update_config_unit(self, ccs_id, cid, name, category, content):
        with self.get_session() as session:
            config = session.query(ConfigUnit).get(cid)
            assert config is not None
            assert config.ccs_id == ccs_id
            config.name = name
            config.category = category
            config.content = content
            session.commit()
            return config.id

    def delete_config_unit(self, ccs_id, cid):
        with self.get_session() as session:
            config = session.query(ConfigUnit).get(cid)
            assert config is not None
            assert config.ccs_id == ccs_id
            session.delete(config)
            session.commit()

    def get_by_id(self, uid):
        with self.get_session() as session:
            cols = [ConfigUnit.id, ConfigUnit.name, ConfigUnit.category, ConfigUnit.content]
            config = session.query(ConfigUnit).get(uid)
            return extract_columns(config, cols)
