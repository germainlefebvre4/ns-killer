#!/usr/bin/python3
import os
from datetime import datetime, timezone
import yaml
from kubernetes import client


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


# Configure kubernetes api
configuration = client.Configuration()
configuration.host = "https://kubernetes.default.svc"
configuration.ssl_ca_cert = '/var/run/secrets/kubernetes.io/serviceaccount/ca.crt'
configuration.api_key_prefix['authorization'] = 'Bearer'
with open("/var/run/secrets/kubernetes.io/serviceaccount/token", "r") as content:
    configuration.api_key['authorization'] = content.read()

api = client.ApiClient(configuration)
v1 = client.CoreV1Api(api)


# Retrieve nskiller configuration
with open("/etc/config/ns-killer.conf", 'r') as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

# DryRun assessment
DRYRUN = False
if "dryrun" in cfg['config']:
    DRYRUN = True if cfg['config']['dryrun'] == "enabled" else False


def delete_ns(ns_name, ns_creation_timestamp_date):
    date_now = datetime.now(timezone.utc).strftime('%Y-%M-%d %H:%M:%S')
    ns_creation_ago = (datetime.now(timezone.utc) - ns_creation_timestamp_date)

    # Define the time unit and calculte the time divider
    config_retention_kind = cfg['config']['retention']['kind']
    time_divider_unit = TIME_DIVIDER_UNITS.get(config_retention_kind)
    ns_creation_ago_time = divmod(ns_creation_ago.days * 86400 + ns_creation_ago.seconds, time_divider_unit)[0]
    # Check namespace rentention time
    if ns_creation_ago_time >= cfg['config']['retention']['time']:
        print(f"{date_now} | Killed namespace '{ns_name}' that lived for {ns_creation_ago_time} {config_retention_kind}")
        # Apply delete if not in DryRun
        if not DRYRUN:
            os.system("kubectl delete namespace {}".format(ns_name))


def main():
    # Retrieve list of namespaces and filtered with the excluded one
    namespace_response = v1.list_namespace()
    namespace_formatted = api.sanitize_for_serialization(namespace_response)
    namespace_list = [
        {"metadata": namespace.get('metadata')}
        for namespace in namespace_formatted.get('items')
        if namespace.get('metadata').get('name') not in NAMESPACE_EXCLUDE
    ]

    print(f"Dryrun mode: {DRYRUN}")
    print("Start iterating on namespaces")

    for namespace in namespace_list:
        ns_name = namespace.get('metadata').get('name')
        ns_creation_timestamp = namespace.get('metadata').get('creationTimestamp')
        ns_creation_timestamp_date = datetime.strptime(ns_creation_timestamp, "%Y-%m-%dT%H:%M:%S%z")

        if len(cfg['namespace']['only']) == 0:
            # Test if namespace is in exclude list
            if ns_name not in cfg['namespace']['exclude']:
                delete_ns(ns_name, ns_creation_timestamp_date)
        else:
            if ns_name in cfg['namespace']['only']:
                delete_ns(ns_name, ns_creation_timestamp_date)


if __name__ == "__main__":
    main()
