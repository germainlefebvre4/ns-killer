#!/usr/bin/python3
import json
from datetime import datetime, timedelta, timezone
import os
import time
from ast import literal_eval
from kubernetes import client, config
import yaml

# Load config file
#with open("config/ns-killer.conf", 'r') as ymlfile:
with open("/etc/config/ns-killer.conf", 'r') as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
# Fulfill config params with default values


# Load cluster config based on service account mapped by k8s
config.load_incluster_config()

k8s_core_v1_api = client.CoreV1Api()

k8s_ns = k8s_core_v1_api.list_namespace(watch=False)

# Time divider units in dict
time_divider_units = {
    'minutes': 60,
    'hours': 60 * 60,
    'days': 60 * 60 * 24,
    'weeks': 60 * 60 * 24 * 7,
    'months': 60 * 60 * 24 * 30
}

def delete_ns(ns_name, ns_creationTimestamp_date):
    date_now = datetime.now(timezone.utc).strftime('%Y-%M-%d %H:%M:%S')
    print(datetime.now(timezone.utc), ns_creationTimestamp_date)
    ns_creation_ago = (datetime.now(timezone.utc) - ns_creationTimestamp_date)
    # Define the time unit and calculte the time divider
    time_divider_unit = time_divider_units.get(cfg['config']['retention']['kind'])
    ns_creation_ago_time = divmod(ns_creation_ago.days * 86400 + ns_creation_ago.seconds, time_divider_unit)[0]
    if ns_creation_ago_time >= cfg['config']['retention']['time']:
        #k8s_core_v1_api.delete_namespace(ns_name)
        print("{} | Killed namespace '{}' that lived for {} {}".format(date_now, ns_name, ns_creation_ago_time, cfg['config']['retention']['kind']))


# Iterate on items
print("Start iterating on namespaces")
for i in k8s_ns.items:
    ns_name = i.metadata.name
    ns_creationTimestamp = i.metadata.creation_timestamp

    if  len(cfg['namespace']['only']) == 0:
      # Test if namespace is in exclude list
      if ns_name not in cfg['namespace']['exclude']:
          delete_ns(ns_name, ns_creationTimestamp)
    else:
        if ns_name in cfg['namespace']['only']:
          delete_ns(ns_name, ns_creationTimestamp)

