#!/usr/bin/python3
import json
from datetime import timedelta, timezone
import datetime
import os
import time
from ast import literal_eval
import yaml

# Load config file
#with open("ns-killer.conf", 'r') as ymlfile:
with open("/etc/config/ns-killer.conf", 'r') as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
# Fulfill config params with default values

# Load cluster namespaces
#with open('namespaces.json', 'r') as outfile:
#    k8s_ns = json.load(outfile)
k8s_ns = literal_eval(os.popen('kubectl get namespaces -o json').read())
#print(k8s_ns)

# Iterate on items
for i in k8s_ns.get('items'):
    ns_name = i.get('metadata').get('name')
    ns_creationTimestamp = i.get('metadata').get('creationTimestamp')
    ns_creationTimestamp_date = datetime.datetime.strptime(ns_creationTimestamp, "%Y-%m-%dT%H:%M:%S%z")
    # Test if namespace is in exclude list
    if ns_name not in cfg['namespace']['exclude']:
        date_now = datetime.datetime.now(timezone.utc).strftime('%Y-%M-%d %H:%M:%S')
        ns_creation_ago = (datetime.datetime.now(timezone.utc) - ns_creationTimestamp_date)
        if cfg['config']['retention']['kind'] == "hours":
            ns_creation_ago_hours = divmod(ns_creation_ago.days * 86400 + ns_creation_ago.seconds, 60)[0]
            if ns_creation_ago_hours >= cfg['config']['retention']['time']:
                print("{} | Killed namespace '{}' that lived for {} hours".format(date_now, ns_name, ns_creation_ago_hours))
        elif cfg['config']['retention']['kind'] == "days":
            ns_creation_ago_hours = divmod(ns_creation_ago.days * 86400 + ns_creation_ago.seconds, 60*24)[0]
            if ns_creation_ago_hours >= cfg['config']['retention']['time']:
                print("{} | Killed namespace '{}' that lived for {} days".format(date_now, ns_name, ns_creation_ago_hours))
        elif cfg['config']['retention']['kind'] == "weeks":
            ns_creation_ago_hours = divmod(ns_creation_ago.days * 86400 + ns_creation_ago.seconds, 60*24*7)[0]
            if ns_creation_ago_hours >= cfg['config']['retention']['time']:
                print("{} | Killed namespace '{}' that lived for {} weeks".format(date_now, ns_name, ns_creation_ago_hours))
        elif cfg['config']['retention']['kind'] == "months":
            ns_creation_ago_hours = divmod(ns_creation_ago.days * 86400 + ns_creation_ago.seconds, 60*24*30)[0]
            if ns_creation_ago_hours >= cfg['config']['retention']['time']:
                print("{} | Killed namespace '{}' that lived for {} months".format(date_now, ns_name, ns_creation_ago_hours))

