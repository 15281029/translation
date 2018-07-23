# -*- coding: utf-8 -*-
from flask import Flask, request, make_response
import requests
import json
from core import Translation, RequestJson, PBMT
from bean import log


app = Flask(__name__)


def buildResponse(code, msg):
    json_data = dict()
    json_data['code'] = code
    json_data['message'] = msg
    response = make_response(json.dumps(json_data, sort_keys=True))
    response.headers['Content-type'] = 'application/json; charset=utf-8'
    return response


'''
    =================翻译=====================
    method:     POST
    headers:    Authorization: [your api key]
    type:       json
                {
                    "text":[text],
                    "taget":[target language]
                }
    return:     json
                {
                    "code":[status code],
                    "message":[translation text]
                }
'''


@app.route('/languages/api/translate', methods=['GET', 'POST'])
def translate():
    ip = request.remote_addr
    if request.method != 'POST':
        return buildResponse(403, "Method Not Allowed. ")
    else:
        try:
            token = request.headers['Authorization']
        except Exception:
            return buildResponse(403, "API key not valid. Please pass a valid API key. ")
        tobj = Translation(token)
        jsondict = request.get_json()
        try:
            rjson = RequestJson(**jsondict)
        except Exception:
            log.writelogs(token, ip, '[Failed] Required field error. ')
            return buildResponse(400, "Required field error. ")
        rlist = tobj.translate(text=rjson.text, target=rjson.target)
        if rlist[0] == 200:
            log.writelogs(token, ip, '[Succeed]')
        else:
            log.writelogs(token, ip, '[Failed] '+rlist[1])
        return buildResponse(code=rlist[0], msg=rlist[1])


'''
    =================日志=====================
    method:     GET
    headers:    Authorization: [your api key]
    type:       NULL
    return:     json
                {
                    "code":[status code],
                    "message":[calling log]
                }
'''


@app.route('/languages/api/logs', methods=['GET', 'POST'])
def getlog():
    if request.method != 'GET':
        return buildResponse(403, "Method Not Allowed. ")
    else:
        try:
            token = request.headers['Authorization']
            logs = log.getlogs(token)
            if logs:
                logs = [(str(lo[0]), lo[1], lo[2], lo[3]) for lo in logs]
                return buildResponse(200, logs)
            elif logs == []:
                return buildResponse(200, [])
            elif logs is None:
                return buildResponse(403, "API key not valid. Please pass a valid API key. ")
        except Exception:
            return buildResponse(500, "Query log exception. ")


@app.route('/languages/support', methods=['GET', 'POST'])
def support_languages():
    if request.method != 'GET':
        return buildResponse(403, "Method Not Allowed. ")
    else:
        return buildResponse(200, PBMT)


if __name__ == '__main__':
    app.run('0.0.0.0', 81, debug=True)
