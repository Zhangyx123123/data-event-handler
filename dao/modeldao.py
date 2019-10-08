from dao.basedao import DaoBase
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, TIMESTAMP
from helper.daohelper import extract_columns
import json
from dao.configunitdao import ConfigUnit


Base = declarative_base()


class CcsModel(Base):
    __tablename__ = 'ccs_model'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ccs_id = Column(String(64))
    name = Column(String(255))
    url = Column(String(1024))
    method = Column(String(32))
    category = Column(String(32))
    created_time = Column(TIMESTAMP)
    updated_time = Column(TIMESTAMP)


class CcsModelDao(DaoBase):
    def get_models(self, ccs_id):
        with self.get_session() as session:
            cols = [CcsModel.id, CcsModel.ccs_id, CcsModel.name, CcsModel.url, CcsModel.method, CcsModel.category]
            data = session.query(CcsModel).filter_by(ccs_id=ccs_id)
            conf = []
            for row in data:
                conf.append(extract_columns(row, cols))
            return conf

    def get_model(self, mid):
        with self.get_session() as session:
            cols = [CcsModel.id, CcsModel.ccs_id, CcsModel.name, CcsModel.url, CcsModel.method]
            mid = session.query(CcsModel).get(mid)
            return extract_columns(mid, cols)

    def add_model(self, ccs_id, name, url, method, category):
        with self.get_session() as session:
            model = CcsModel(ccs_id=ccs_id, name=name, url=url, method=method, category=category)
            session.add(model)
            session.commit()
            return model.id

    def update_model(self, ccs_id, mid, name, url, method, category):
        with self.get_session() as session:
            config = session.query(CcsModel).get(mid)
            assert config.ccs_id == ccs_id
            config.name = name
            config.url = url
            config.method = method
            config.category = category
            session.commit()
            return config.id

    def delete_model(self, ccs_id, mid):
        with self.get_session() as session:
            config = session.query(CcsModel).get(mid)
            assert config.ccs_id == ccs_id
            model_config_units = session.query(ConfigUnit).filter_by(ccs_id=ccs_id, category='model')
            for unit in model_config_units:
                content = json.loads(unit.content)
                if isinstance(content, list):
                    mid = int(mid)
                    if mid in content:
                        content.remove(mid)
                        unit.content = json.dumps(content)
            session.delete(config)
            session.commit()
