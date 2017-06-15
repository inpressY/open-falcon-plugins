#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import time
import json
import os
import requests

timestamp = int(time.time())
mlist = ["we.node.cpu","we.node.mem"]
data = []


def create_record(pid,cvalue,mvalue):
    record = {}
    record['endpoint'] = os.uname()[1]
    record['metric'] = "we.node.cpu"
    record['timestamp'] = timestamp
    record['step'] = 60
    record['value'] = abs(float(cvalue))
    record['counterType'] = 'GAUGE'
    record['tags'] = 'node.pid=%s' % pid

    data.append(record)

    record = {}
    record['endpoint'] = os.uname()[1]
    record['metric'] = "we.node.mem"
    record['timestamp'] = timestamp
    record['step'] = 60
    record['value'] = abs(float(mvalue))
    record['counterType'] = 'GAUGE'
    record['tags'] = 'node.pid=%s' % pid

    data.append(record)

if __name__ == '__main__':
    cmd = subprocess.Popen('ps -eo pid,ppid,cmd,%cpu,%mem --sort=-%cpu | grep -v grep | grep /data/we/web/app',shell=True,stdout=subprocess.PIPE).communicate()[0].split('\n')
    for i in cmd:
        if len(i):
            value = i.split()
            create_record(value[0],value[4],value[5])
    if data:
        print json.dumps(data)
