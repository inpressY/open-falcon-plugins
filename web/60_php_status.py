#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import requests
import time
import json
import os

timestamp = int(time.time())
url = 'http://127.0.0.1/php-status'
phpstatus = [0]
mlist = ["php.status.accept_conn","php.status.listen_queue","php.status.idle_process","php.status.active_process","php.status.total_process","php.status.max_children_reached","php.status.slow_requests","php.status.error"]
vlist = []
data = []


def create_record(i):
    record = {}
    record['endpoint'] = os.uname()[1]
    record['metric'] = mlist[i]
    record['timestamp'] = timestamp
    record['step'] = 60
    record['value'] = abs(float(phpstatus[i]))
    record['counterType'] = 'GAUGE'
    record['tags'] = 'service=webserver,status=php'

    data.append(record)

if __name__ == '__main__':
    try:
        response = requests.get(url)
        getcode = response.status_code
        content = response.content.split('\n')[4:][:-1]
        if 'accepted conn' in content[0]:
            for i in range(len(content)):
                value = content[i].split()[-1]
                vlist.append(value)
                phpstatus = [ vlist[i] for i in [0,1,4,5,6,8,9] ]
                for i in range(len(phpstatus)):
                    create_record(i)
    except requests.exceptions.RequestException as e:
        raise e

    if getcode == int(200):
        for i in range(len(phpstatus)):
            create_record(i)
            print json.dumps(data)
    elif getcode == int(404):
        print 404
    else:
        create_record(-1)
        print json.dumps(data[-1])
