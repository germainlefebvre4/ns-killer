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
    # cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
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


def delete_ns(ns_name, ns_creationTimestamp_date):
    date_now = datetime.now(timezone.utc).strftime('%Y-%M-%d %H:%M:%S')
    ns_creation_ago = (datetime.now(timezone.utc) - ns_creationTimestamp_date)
    # Define the time unit and calculte the time divider
    time_divider_unit = TIME_DIVIDER_UNITS.get(cfg['config']['retention']['kind'])
    ns_creation_ago_time = divmod(ns_creation_ago.days * 86400 + ns_creation_ago.seconds, time_divider_unit)[0]
    if ns_creation_ago_time >= cfg['config']['retention']['time']:
        #os.system("kubectl delete namespace {}".format(ns_name))
        print("{} | Killed namespace '{}' that lived for {} {}".format(date_now, ns_name, ns_creation_ago_time, cfg['config']['retention']['kind']))

def main():
    namespace_response = k8s_api.list_namespace()
    namespace_formatted = api.sanitize_for_serialization(namespace_response)
    namespace_list = [{"metadata": ns.get('metadata')} for ns in namespace_formatted.get('items') if ns.get('metadata').get('name') not in NAMESPACE_EXCLUDE]

    
    print("Start iterating on namespaces")
    for ns in namespace_list:
        # try:
            ns_name = ns.get('metadata').get('name')
            ns_creationTimestamp = ns.get('metadata').get('creationTimestamp')
            ns_creationTimestamp_date = datetime.strptime(ns_creationTimestamp, "%Y-%m-%dT%H:%M:%S%z")

            if has(ns, "metadata.annotations.ns-killer/include") or has(ns, "metadata.annotations.ns-killer/exclude"):
            # if True:
                ns_annotation_include = False
                ns_annotation_exclude = False
                if has(ns, "metadata.annotations.ns-killer/include"):
                    ns_annotation_include = ns.get('metadata').get('annotations').get('ns-killer/include')
                    if ns_annotation_include == "true":
                        # Test if namespace is in include list
                        delete_ns(ns_name, ns_creationTimestamp_date)

        # except:
        #     pass

if __name__ == "__main__":
    main()