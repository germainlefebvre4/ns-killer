#!/usr/bin/python3
import json
from datetime import timedelta, timezone
import datetime
import os
import time
from ast import literal_eval

PYTHON_LOOP_FREQUENCY = int(os.environ.get('PYTHON_LOOP_FREQUENCY'))
NS_PATTERN = os.environ.get('NS_PATTERN')
NS_RENTENTION_KIND = os.environ.get('NS_RENTENTION_KIND')
NS_RENTENTION_TIME = int(os.environ.get('NS_RENTENTION_TIME'))

ns_exlude = ['kube-system']

while True:
    #k8s_ns = os.system('kubectl get namespaces -o json')
    k8s_ns = literal_eval(os.popen('kubectl get namespaces -o json').read())
    print(k8s_ns)
    print(type(k8s_ns))
    for i in k8s_ns.get('items'):
        ns_name = i.get('metadata').get('name')
        ns_creationTimestamp = i.get('metadata').get('creationTimestamp')
        ns_creationTimestamp_date = datetime.datetime.strptime(ns_creationTimestamp, "%Y-%m-%dT%H:%M:%S%z")
        if ns_name not in ns_exlude:
            date_now = datetime.datetime.now(timezone.utc).strftime('%Y-%M-%d %H:%M:%S')
            ns_creation_ago = (datetime.datetime.now(timezone.utc) - ns_creationTimestamp_date)
            ns_creation_ago_hours = divmod(ns_creation_ago.days * 86400 + ns_creation_ago.seconds, 60)[0]
            if ns_creation_ago_hours >= NS_RENTENTION_TIME:
                print("{} | Killed namespace '{}' that lived for {} hours".format(date_now, ns_name, ns_creation_ago_hours))
    time.sleep(PYTHON_LOOP_FREQUENCY)

