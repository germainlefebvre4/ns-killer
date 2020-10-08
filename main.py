#!/usr/bin/python3
import json
import os
import yaml
from datetime import datetime, timedelta, timezone
from ast import literal_eval
from dotenv import load_dotenv
from deepmerge import Merger

# Load config
#with open("config/ns-killer.conf", 'r') as ymlfile:
with open("/etc/config/ns-killer.conf", 'r') as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
load_dotenv()
cfg_from_env_var = os.environ.get("config")
if(cfg_from_env_var != None):
    merger = Merger(
        [
            (list, ["append"]),
            (dict, ["merge"])
        ],
        ["override"],
        ["override"]
    )
    cfg = merger.merge(cfg, json.loads(cfg_from_env_var))

# Load cluster namespaces
#with open('namespaces.json', 'r') as outfile:
#    k8s_ns = json.load(outfile)
k8s_ns = literal_eval(os.popen('kubectl get namespaces -o json').read())
#print(k8s_ns)

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
        print("{} | Killed namespace '{}' that lived for {} {}".format(date_now, ns_name, ns_creation_ago_time, cfg['config']['retention']['kind']))

# Iterate on items
print("Start iterating on namespaces")
for i in k8s_ns.get('items'):
    ns_name = i.get('metadata').get('name')
    ns_creationTimestamp = i.get('metadata').get('creationTimestamp')
    ns_creationTimestamp_date = datetime.strptime(ns_creationTimestamp, "%Y-%m-%dT%H:%M:%S%z")
    if  len(cfg['namespace']['only']) == 0:
      # Test if namespace is in exclude list
      if ns_name not in cfg['namespace']['exclude']:
          delete_ns(ns_name, ns_creationTimestamp_date)
    else:
        if ns_name in cfg['namespace']['only']:
          delete_ns(ns_name, ns_creationTimestamp_date)