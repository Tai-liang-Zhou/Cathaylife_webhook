# -*- coding: utf-8 -*-
from flask import Response
from flask import request
from flask_restful import Resource
from dateutil.parser import parse
from langconv import Converter
from datetime import datetime
import json
import re
import requests
import constants
import logging
LOG = logging.getLogger(__name__)

def setup_route(api):
    """
        return map of endpoint and handler
    """
    # Cathaylife TravelInsurance API
    api.add_resource(doTravelInsuranceCalculate, '/rest/doTravelInsuranceCalculate')
    
def encapsule_rtn_format(update_kv_map, remove_kv_map):
    rtn_obj = {
                "status_code": 0,
                "msg_response": {}
            }
    if update_kv_map is not None:
        rtn_obj['msg_response']['update'] = update_kv_map
    if remove_kv_map is not None:
        rtn_obj['msg_response']['remove'] = remove_kv_map
    return rtn_obj

class doTravelInsuranceCalculate(Resource):
    def post(self):
        json_from_request = json.loads(Converter('zh-hant').convert(request.stream.read().decode('utf-8')))
        LOG.debug('In doTravelInsuranceCalculate, data received from TE: %s' % json.dumps(json_from_request, ensure_ascii=False, indent=4))
        payload = {
                "DAY": 10,
                "HD_FACE_AMT":1000000,
                "MR_FACE_AMT":100000,
                "OHS_FACE_AMT":100000
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded','X-Requested-With': 'XMLHttpRequest'}
        url = constants.CATHAYLIFE_URL + 'SYL0_M030/doTravelInsuranceCalculate'
        LOG.debug('request cathaylife travel insurance caculate API: %s' % url)
        LOG.debug('payload: %s' % json.dumps(payload, ensure_ascii=False, indent=4))
        r = requests.post(
            url,
            json=payload,
            timeout=float(constants.REQUEST_TIMEOUT),
            headers = headers
        )
        r_obj = r.json()
        LOG.debug('response: %s' % json.dumps(r_obj, ensure_ascii=False, indent=4))
        r_obj =  eval(r_obj['msg_response']['update']['content'])
        res = r_obj['text'].replace("<br>","")
        update_kv_map = {"response" : res}
        ret = encapsule_rtn_format(update_kv_map, None)
        return Response(json.dumps(ret), status=200)