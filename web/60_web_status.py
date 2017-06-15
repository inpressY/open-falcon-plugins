#!/data/service/python2.7/bin/python
#

import time
import json
import os
import requests

timestamp = int(time.time())
url = 'http://127.0.0.1/web-status'
webstatus = [0]
mlist = ["web.status.read","web.status.write","web.status.wait","web.status.error"]
data = []


def create_record(i):
    record = {}
    record['endpoint'] = os.uname()[1]
    record['metric'] = mlist[i]
    record['timestamp'] = timestamp
    record['step'] = 60
    record['value'] = abs(float(webstatus[i]))
    record['counterType'] = 'GAUGE'
    record['tags'] = 'service=webserver,status=web'

    data.append(record)

if __name__ == '__main__':
    try:
        response = requests.get(url)
        getcode = response.status_code
        content = response.content
        if content.find("Active connections") != -1:
            webstatus = [ content.split('\n')[3].split().pop(i) for i in [1,3,5] ]
    except requests.exceptions.RequestException as e:
        raise e

    if getcode == int(200):
        for i in range(len(webstatus)):
            create_record(i)
            print json.dumps(data)
    else:
        create_record(-1)
        print json.dumps(data[-1])
