# -*- coding: utf-8 -*-
import logging.handlers
import flask_restful
from flask import Flask

from controller import ccshandler, configunithandler, ccsconfhandler, modelhandler, bothandler


def init_logging():
    # setup logger
    FORMAT = "[%(asctime)s][%(process)d][%(threadName)10.10s][%(levelname).1s][%(filename)s:%(funcName)s:%(lineno)s] : %(message)s"
    level = {
        'CRITICAL': logging.CRITICAL,
        'ERROR': logging.ERROR,
        'WARNING': logging.WARNING,
        'INFO': logging.INFO,
        'DEBUG': logging.DEBUG,
    }.get('INFO', logging.INFO)
    logging.basicConfig(filename='/tmp/bfb.log',
                        level=level, format=FORMAT)
    # set up logging to console
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # set a format which is simpler for console use
    console.setFormatter(logging.Formatter(FORMAT))
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)

    handler = logging.handlers.RotatingFileHandler('/tmp/bfb.log', backupCount=10, maxBytes=10240000)
    logging.getLogger('').addHandler(handler)
    logging.info("LOG LEVEL %s", level)


def init_restful(app):
    restful_set = flask_restful.Api(app)

    # setup api controller
    ccshandler.setup_route(restful_set)
    configunithandler.setup_route(restful_set)
    ccsconfhandler.setup_route(restful_set)
    modelhandler.setup_route(restful_set)
    bothandler.setup_route(restful_set)


api = Flask(__name__)
init_logging()
init_restful(api)

if __name__ == '__main__':
    api.run(debug=True)
