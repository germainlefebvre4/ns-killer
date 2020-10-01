import shlex
import subprocess
import time
import kubernetes
from kopf.testing import KopfRunner

global runner

def setup_module(module):
    """ setup any state specific to the execution of the given module."""
    global runner
    print("---")
    with KopfRunner(['run', '--verbose', 'handlers.py']) as runner:
        print(runner._thread)
        print(runner._thread.is_alive())


def test_dummy():
    global runner
    # api = kubernetes.client.CoreV1Api()
    # namespace_response = api.list_namespace()
    # print(dir(runner))
    # print(runner._thread)
    # print(dir(runner._thread))
    print(type(runner))
    print(type(runner._thread))
    print(runner._thread.is_alive())

    # ps = subprocess.run("ls -la", shell=True, check=True)
    # print(type(ps))
    # print(dir(ps))



def teardown_module(module):
    """ teardown any state that was previously setup with a setup_module
    method."""
