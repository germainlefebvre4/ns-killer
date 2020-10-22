#!/usr/bin/python3
import json
from datetime import datetime, timedelta, timezone
import os
import time
from ast import literal_eval
import yaml
import kubernetes
from pydash import has

# Initialize kubernetes api
from kubernetes.client import ApiClient
api = ApiClient()
kubernetes.config.load_kube_config()
k8s_api = kubernetes.client.CoreV1Api()

# Load config file
with open("config/ns-killer.conf", 'r') as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
# with open("/etc/config/ns-killer.conf", 'r') as ymlfile:
#     cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
# Fulfill config params with default values


# System namespaces exclude
NAMESPACE_EXCLUDE = ["default", "kube-node-lease", "kube-public", "kube-system"]

# Time divider units in dict
TIME_DIVIDER_UNITS = {
    'minutes': 60,
    'hours': 60 * 60,
    'days': 60 * 60 * 24,
    'weeks': 60 * 60 * 24 * 7,
    'months': 60 * 60 * 24 * 30
}

if "dryrun" in cfg['config']:
    DRYRUN = True if cfg['config']['dryrun'] == "enabled" else False
else:
    DRYRUN = False


def delete_ns(ns_name, ns_creationTimestamp_date):
    date_now = datetime.now(timezone.utc).strftime('%Y-%M-%d %H:%M:%S')
    ns_creation_ago = (datetime.now(timezone.utc) - ns_creationTimestamp_date)

    # Define the time unit and calculte the time divider
    time_divider_unit = TIME_DIVIDER_UNITS.get(cfg['config']['retention']['kind'])
    ns_creation_ago_time = divmod(ns_creation_ago.days * 86400 + ns_creation_ago.seconds, time_divider_unit)[0]
    config_retention_kind = cfg['config']['retention']['kind']
    if ns_creation_ago_time >= cfg['config']['retention']['time']:
        print(f"{date_now} | Killed namespace '{ns_name}' that lived for {ns_creation_ago_time} {config_retention_kind}")
        if not DRYRUN:
            os.system("kubectl delete namespace {}".format(ns_name))

def main():
    namespace_response = k8s_api.list_namespace()
    namespace_formatted = api.sanitize_for_serialization(namespace_response)
    namespace_list = [{"metadata": ns.get('metadata')} for ns in namespace_formatted.get('items') if ns.get('metadata').get('name') not in NAMESPACE_EXCLUDE]
    
    print(f"Dryrun mode: {DRYRUN}")
    print("Start iterating on namespaces")

    for ns in namespace_list:
        ns_name = ns.get('metadata').get('name')
        ns_creationTimestamp = ns.get('metadata').get('creationTimestamp')
        ns_creationTimestamp_date = datetime.strptime(ns_creationTimestamp, "%Y-%m-%dT%H:%M:%S%z")

        if  len(cfg['namespace']['only']) == 0:
            # Test if namespace is in exclude list
            if ns_name not in cfg['namespace']['exclude']:
                delete_ns(ns_name, ns_creationTimestamp_date)
        else:
            if ns_name in cfg['namespace']['only']:
                delete_ns(ns_name, ns_creationTimestamp_date)

if __name__ == "__main__":
    main()