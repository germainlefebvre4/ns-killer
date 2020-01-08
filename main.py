#!/usr/bin/python3
import json
from datetime import timedelta, timezone
import datetime
import os
import time
from ast import literal_eval
import yaml

# Load config file
#with open("config/ns-killer.conf", 'r') as ymlfile:
with open("/etc/config/ns-killer.conf", 'r') as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
# Fulfill config params with default values

# Load cluster namespaces
#with open('namespaces.json', 'r') as outfile:
#    k8s_ns = json.load(outfile)
k8s_ns = literal_eval(os.popen('kubectl get namespaces -o json').read())
#print(k8s_ns)

# Iterate on items
print("Start iterating on namespaces")
for i in k8s_ns.get('items'):
    ns_name = i.get('metadata').get('name')
    ns_creationTimestamp = i.get('metadata').get('creationTimestamp')
    ns_creationTimestamp_date = datetime.datetime.strptime(ns_creationTimestamp, "%Y-%m-%dT%H:%M:%S%z")

    if  len(cfg['namespace']['only']) == 0:
      # Test if namespace is in exclude list
      if ns_name not in cfg['namespace']['exclude']:
          date_now = datetime.datetime.now(timezone.utc).strftime('%Y-%M-%d %H:%M:%S')
          ns_creation_ago = (datetime.datetime.now(timezone.utc) - ns_creationTimestamp_date)
  
          # Define the time unit and calculte the time divider
          if cfg['config']['retention']['kind'] == "minutes":
              time_divider_unit = 60
          elif cfg['config']['retention']['kind'] == "hours":
              time_divider_unit = 60*60
          elif cfg['config']['retention']['kind'] == "days":
              time_divider_unit = 60*60*24
          elif cfg['config']['retention']['kind'] == "weeks":
              time_divider_unit = 60*60*24*7
          elif cfg['config']['retention']['kind'] == "months":
              time_divider_unit = 60*62*24*30
  
          ns_creation_ago_time = divmod(ns_creation_ago.days * 86400 + ns_creation_ago.seconds, time_divider_unit)[0]
          if ns_creation_ago_time >= cfg['config']['retention']['time']:
              os.system("kubectl delete namespace {}".format(ns_name))
              print("{} | Killed namespace '{}' that lived for {} {}".format(date_now, ns_name, ns_creation_ago_time, cfg['config']['retention']['kind']))
    else:
        if ns_name in cfg['namespace']['only']:
          date_now = datetime.datetime.now(timezone.utc).strftime('%Y-%M-%d %H:%M:%S')
          ns_creation_ago = (datetime.datetime.now(timezone.utc) - ns_creationTimestamp_date)

          # Define the time unit and calculte the time divider
          if cfg['config']['retention']['kind'] == "minutes":
              time_divider_unit = 60
          elif cfg['config']['retention']['kind'] == "hours":
              time_divider_unit = 60*60
          elif cfg['config']['retention']['kind'] == "days":
              time_divider_unit = 60*60*24
          elif cfg['config']['retention']['kind'] == "weeks":
              time_divider_unit = 60*60*24*7
          elif cfg['config']['retention']['kind'] == "months":
              time_divider_unit = 60*62*24*30

          ns_creation_ago_time = divmod(ns_creation_ago.days * 86400 + ns_creation_ago.seconds, time_divider_unit)[0]
          if ns_creation_ago_time >= cfg['config']['retention']['time']:
              os.system("kubectl delete namespace {}".format(ns_name))
              print("{} | Killed namespace '{}' that lived for {} {}".format(date_now, ns_name, ns_creation_ago_time, cfg['config']['retention']['kind']))

