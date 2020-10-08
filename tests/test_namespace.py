import shlex
import subprocess
import time
from kubernetes import client

import main

def test_namespace_withoutAnnotation():
    try:
        # Before testing
        subprocess.run("kubectl apply -f tests/samples/namespace_withoutAnnotation.yaml", shell=True, check=True)

        # 
        api = client.CoreV1Api()
        namespaces_before = [{"name": ns.metadata.name, "metadata": ns.metadata.annotations} for ns in api.list_namespace().items if ns.metadata.name == "test-without-annotation"]

        assert "test-without-annotation" in [x['name'] for x in namespaces_before]
        assert len([x["metadata"]["annotations"] for x in namespaces_before if "annotations" in x["metadata"]]) == 0
        for ns in namespaces_before:
            assert not ns.get('metadata').get('annotations')
        
        # Run main function
        main.main()

        namespaces_after = [{"name": ns.metadata.name, "metadata": ns.metadata.annotations} for ns in api.list_namespace().items if ns.metadata.name == "test-without-annotation"]

        assert "test-without-annotation" not in namespaces_after

        namespace_response = api.list_namespace()
        namespace_withoutAnnotation = [{"name": ns.metadata.name, "metadata": ns.metadata.annotations} for ns in namespace_response.items if ns.metadata.name == "test-without-annotation"]

    
    finally:
        # After testing
        subprocess.run("kubectl delete -f tests/samples/namespace_withoutAnnotation.yaml", shell=True, check=True)
