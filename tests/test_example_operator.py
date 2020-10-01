import shlex
import subprocess
import time
import kubernetes
from kopf.testing import KopfRunner

def test_operator():
    with KopfRunner(['run', '--verbose', 'handlers.py']) as runner:
        # do something while the operator is running.

        subprocess.run("kubectl apply -f tests/samples/namespace_annotations.yaml", shell=True, check=True)

        api = kubernetes.client.CoreV1Api()
        namespace_response = api.list_namespace()


        namespace_withAnnotationInclude = [{"name": nsa.metadata.name, "metadata": nsa.metadata.annotations} for nsa in namespace_response.items if nsa.metadata.name == "test-with-annotation-include"]
        namespace_withAnnotationExclude = [{"name": nsa.metadata.name, "metadata": nsa.metadata.annotations} for nsa in namespace_response.items if nsa.metadata.name == "test-with-annotation-exclude"]
        namespace_withAnnotationBoth = [{"name": nsa.metadata.name, "metadata": nsa.metadata.annotations} for nsa in namespace_response.items if nsa.metadata.name == "test-with-annotation-both"]
        namespace_withoutAnnotation = [{"name": nsa.metadata.name, "metadata": nsa.metadata.annotations} for nsa in namespace_response.items if nsa.metadata.name == "test-without-annotation"]
        
        
        for ns in namespace_withoutAnnotation:
            print(ns)
            print(ns.get('metadata').get('annotations'))
            assert not ns.get('metadata').get('annotations')
            # assert "ns-killer" not in ns.get('metadata').get('annotations')
        
        subprocess.run("kubectl delete -f tests/samples/namespace_annotations.yaml", shell=True, check=True)

    assert runner.exit_code == 0
    assert runner.exception is None