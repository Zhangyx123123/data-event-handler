# -*- coding: utf-8 -*-
import logging
import os
from contextlib import contextmanager

from sqlalchemy import text, create_engine
from sqlalchemy.orm import sessionmaker
from config import constants


Session = sessionmaker()


class DaoBase(object):
    db_engine_handler = None

    def __init__(self):
        self.db_retry = 1
        if DaoBase.db_engine_handler is None:
            self.db_engine = DaoBase.init_db()
        else:
            self.db_engine = DaoBase.db_engine_handler
        Session.configure(bind=self.db_engine)

    @contextmanager
    def get_session(self):
        session = Session()
        yield session
        session.close()

    @staticmethod
    def init_db():
        conn_fmt = "mysql+pymysql://{}:{}@{}/emoticcs?charset=utf8"
        user = os.environ.get(constants.ENV_DB_USER, constants.SQL_USER)
        password = os.environ.get(constants.ENV_DB_PASSWORD, constants.SQL_PASSWORD)
        addr = os.environ.get(constants.ENV_DB_SERVER, constants.SQL_ADDR)

        logging.info("mysql server ip:" + addr)

        conn_str = conn_fmt.format(user, password, addr)
        db_engine = create_engine(
            conn_str,
            max_overflow=10,
            pool_size=10,
            pool_timeout=15,
            pool_recycle=5,
            echo=False
        )
        DaoBase.db_engine_handler = db_engine
        return db_engine

    def execute_search(self, db, sql, args):
        if db is None:
            logging.error("DB hasn't init")
            return None

        retry_count = 0
        conn = None
        results = []

        while retry_count < self.db_retry:

            try:
                conn = db.connect()
                result = conn.execute(text(sql), args)
                if result is not None:
                    results = result.fetchall()
                    result.close()
                break
            except Exception as ex:
                template = "An exception of type {0} occurred when exec sql [{1}]. Arguments:{2!r}"
                message = template.format(type(ex).__name__, str(text(sql)), ex.args)
                logging.error(message)
            finally:
                if conn is not None:
                    conn.close()
                retry_count += 1

        return results

    @staticmethod
    def insert(db, sql, args):
        if db is None:
            logging.error("DB hasn't init")
            return None
        conn = None
        results = []

        try:
            conn = db.connect()
            result = conn.execute(text(sql), args)
            if result is not None:
                results = result
                result.close()
        except Exception as ex:
            template = "An exception of type {0} occurred when exec sql [{1}]. Arguments:{2!r}"
            message = template.format(type(ex).__name__, str(text(sql)), ex.args)
            logging.error(message)
        finally:
            if conn is not None:
                conn.close()

        return results

    @staticmethod
    def execute(db, sql, args):
        if db is None:
            logging.error("DB hasn't init")
            return None
        conn = None
        results = []

        try:
            conn = db.connect()
            result = conn.execute(text(sql), args)
            if result is not None:
                results = result
                result.close()

        finally:
            if conn is not None:
                conn.close()

        return results

    @staticmethod
    def raw_custom_data_to_dict(columns, data_structure, sql_raw):
        ret = {}
        if len(columns) == 0:
            for i in range(0, len(data_structure)):
                ret[data_structure[i]] = sql_raw[i]
        else:
            for i in range(0, len(columns)):
                if i < len(sql_raw):
                    ret[columns[i]] = sql_raw[i]
        return ret
