import shlex
import subprocess
import time
import kubernetes
from kopf.testing import KopfRunner
from myrunner import myRunner

def test_namespace_withoutAnnotation():
    try:
        # Before testing
        subprocess.run("kubectl apply -f tests/samples/namespace_withoutAnnotation.yaml", shell=True, check=True)

        subprocess

        namespace_withoutAnnotation = [{"name": nsa.metadata.name, "metadata": nsa.metadata.annotations} for nsa in namespace_response.items if nsa.metadata.name == "test-without-annotation"]

        for ns in namespace_withoutAnnotation:
            assert not ns.get('metadata').get('annotations')
    
    finally:
        # After testing
        subprocess.run("kubectl delete -f tests/samples/namespace_withoutAnnotation.yaml", shell=True, check=True)

    assert runner.exit_code == 0
    assert runner.exception is None


def test_namespace_withAnnotationInclude():
    with KopfRunner(['run', '--verbose', 'handlers.py']) as runner:
        try:
            # Before testing
            subprocess.run("kubectl apply -f tests/samples/namespace_withAnnotationInclude.yaml", shell=True, check=True)

            api = kubernetes.client.CoreV1Api()
            namespace_response = api.list_namespace()

            namespace_withAnnotationInclude = [{"name": nsa.metadata.name, "metadata": nsa.metadata.annotations} for nsa in namespace_response.items if nsa.metadata.name == "test-with-annotation-include"]
            
            for ns in namespace_withAnnotationInclude:
                assert ns.get('metadata').get('annotations')
                assert ns.get('metadata').get('annotations').get('ns-killer/include')
                assert not ns.get('metadata').get('annotations').get('ns-killer/exclude')
        finally:
            # After testing
            subprocess.run("kubectl delete -f tests/samples/namespace_withAnnotationInclude.yaml", shell=True, check=True)

    assert runner.exit_code == 0
    assert runner.exception is None

def test_namespace_withAnnotationExclude():
    with KopfRunner(['run', '--verbose', 'handlers.py']) as runner:
        # Before testing
        subprocess.run("kubectl apply -f tests/samples/namespace_withAnnotationExclude.yaml", shell=True, check=True)

        api = kubernetes.client.CoreV1Api()
        namespace_response = api.list_namespace()

        namespace_withAnnotationExclude = [{"name": nsa.metadata.name, "metadata": nsa.metadata.annotations} for nsa in namespace_response.items if nsa.metadata.name == "test-with-annotation-exclude"]        
        
        for ns in namespace_withAnnotationExclude:
            assert ns.get('metadata').get('annotations')
            assert ns.get('metadata').get('annotations').get('ns-killer/exclude')
            assert not ns.get('metadata').get('annotations').get('ns-killer/include')
        
        # After testing
        subprocess.run("kubectl delete -f tests/samples/namespace_withAnnotationExclude.yaml", shell=True, check=True)

    assert runner.exit_code == 0
    assert runner.exception is None

def test_namespace_withAnnotationBoth():
    with KopfRunner(['run', '--verbose', 'handlers.py']) as runner:
        # Before testing
        subprocess.run("kubectl apply -f tests/samples/namespace_withAnnotationBoth.yaml", shell=True, check=True)

        api = kubernetes.client.CoreV1Api()
        namespace_response = api.list_namespace()

        namespace_withAnnotationBoth = [{"name": nsa.metadata.name, "metadata": nsa.metadata.annotations} for nsa in namespace_response.items if nsa.metadata.name == "test-with-annotation-both"]        
        
        for ns in namespace_withAnnotationBoth:
            assert ns.get('metadata').get('annotations')
            assert not ns.get('metadata').get('annotations').get('ns-killer/include')
            assert not ns.get('metadata').get('annotations').get('ns-killer/exclude')
        
        # After testing
        subprocess.run("kubectl delete -f tests/samples/namespace_withAnnotationBoth.yaml", shell=True, check=True)

    assert runner.exit_code == 0
    assert runner.exception is None
