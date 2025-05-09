import kopf
import kubernetes
import os

@kopf.on.create('', 'v1', 'services')
def create_ingress(spec, name, namespace, **kwargs):
    ports = spec.get("ports")
    if not ports:
        return

    cluster_name = os.getenv("CLUSTER_NAME", "cluster-1")
    datacenter_name = os.getenv("DATACENTER_NAME", "datacenter-1")

    k8s = kubernetes.client.NetworkingV1Api()

    for port in ports:
        host = f"{name}-{port['port']}.{namespace}.{cluster_name}.{datacenter_name}.internal"
        ingress_manifest = {
            "apiVersion": "networking.k8s.io/v1",
            "kind": "Ingress",
            "metadata": {
                "name": f"{name}-{port['port']}",
                "namespace": namespace
            },
            "spec": {
                "ingressClassName": "nginx",
                "rules": [{
                    "host": host,
                    "http": {
                        "paths": [{
                            "path": "/",
                            "pathType": "Prefix",
                            "backend": {
                                "service": {
                                    "name": name,
                                    "port": {
                                        "number": port['port']
                                    }
                                }
                            }
                        }]
                    }
                }]
            }
        }

        try:
            k8s.create_namespaced_ingress(namespace=namespace, body=ingress_manifest)
        except kubernetes.client.exceptions.ApiException as e:
            if e.status != 409:
                raise

@kopf.on.delete('', 'v1', 'services')
def delete_ingress(spec, name, namespace, **kwargs):
    ports = spec.get("ports")
    if not ports:
        return

    k8s = kubernetes.client.NetworkingV1Api()

    for port in ports:
        ingress_name = f"{name}-{port['port']}"
        try:
            k8s.delete_namespaced_ingress(name=ingress_name, namespace=namespace)
        except kubernetes.client.exceptions.ApiException as e:
            if e.status != 404:
                raise