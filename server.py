# -*- coding: utf-8 -*-
from flask import Flask
import flask_restful
import TravelInsurance_API
import log

conf={}
conf['verbose'] = 'DEBUG'
conf['log_path'] = '/tmp/'
log.setup_logging(conf)
api = Flask(__name__)
restful_set = flask_restful.Api(api)
TravelInsurance_API.setup_route(restful_set)

if __name__ == "__main__":
    api.run(host='0.0.0.0', port= 5008)