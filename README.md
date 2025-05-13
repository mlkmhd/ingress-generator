# Kubernetes Ingress Generator

This project is used to automatically generate ingress resources based on your access to Kubernetes services.

Let's suppose you have a Kubernetes service at `myservice.mynamespace:8080`. After deploying your service to Kubernetes, this tool will generate an ingress like `myservice-8080.myservice.cluster-X.datacenter-Y.internal`, allowing you to access the service. It will also automatically delete the ingress when you delete the service.
## Installation
```bash
$ kubectl apply -f ./deployment.yaml
```

## Configuration
You can configure the `CLUSTER_NAME` and `DATACENTER_NAME` values used in the `./deployment.yaml` file to match your requirements:
```bash
$ vim ./deployment.yaml
...
  env:
    - name: CLUSTER_NAME
      value: "cluster-1"
    - name: DATACENTER_NAME
      value: "datacenter-1"
...
```

## Testing

To test the ingress generator, you can deploy a test service:
```
$ kubectl apply -f ./test-service.yaml
$
$ kubectl get service
NAME         TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)        AGE
test         NodePort    10.43.167.60   <none>        80:32036/TCP   5s
$
$ kubectl get ingress
NAME             CLASS   HOSTS                                              ADDRESS         PORTS   AGE
test-80          nginx   test-80.default.cluster-1.datacenter-1.internal          10.43.112.173   80      37s
```

You need to define `test-80.default.cluster-1.datacenter-1.internal` in your DNS server. After that, you can access your service using the generated ingress.

```bash
$ curl http://test-80.default.cluster-1.datacenter-1.internal
```