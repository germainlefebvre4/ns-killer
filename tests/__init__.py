import os
import subprocess
import kubernetes

TEST_KUBERNETES_CONTEXT = os.getenv("TEST_KUBERNETES_CONTEXT", "minikube")

def setup_module(module):
    # Change Kubernetes current context to minikube
    subprocess.run(f"kubectl config use-context {TEST_KUBERNETES_CONTEXT}", shell=True, check=True)
    kubernetes.config.load_kube_config()
