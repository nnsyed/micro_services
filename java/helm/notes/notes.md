kubectl create namespace java-ms
kubectl create secret generic postgres-credentials --from-literal=password='Welcome123' -n java-ms
kubectl create secret generic postgres-credentials --from-literal=password='mysecretpassword' -n java-ms
kubectl get secret postgres-credentials -n java-ms


minikube image load employee-service:latest
minikube image load cache-service:latest


helm lint ./java-ms

helm template myservices ./java-ms -n java-ms

helm install myservices ./java-ms  -n java-ms --wait --timeout 5m


debugging tricks:
-----------------
helm list -n java-ms -a
helm status myservices -n java-ms
kubectl get pods -n java-ms -o wide
kubectl get events -n java-ms --sort-by=.lastTimestamp

kubectl logs deployment/employee-service-deployment -n java-ms --tail=50


Cleaning up:
-----------------------

$ helm uninstall myservices -n java-ms
release "myservices" uninstalled
$ helm list -n java-ms -a
NAME	NAMESPACE	REVISION	UPDATED	STATUS	CHART	APP VERSION
$ kubectl delete namespace java-ms
namespace "java-ms" deleted
$ kubectl get namespace java-ms
Error from server (NotFound): namespaces "java-ms" not found

$ kubectl get pods
No resources found in default namespace.
$ 
-----------------------------------

Setting up again:
---------------------

$ kubectl create namespace java-ms
namespace/java-ms created
$ kubectl create secret generic postgres-credentials --from-literal=password='mysecretpassword' -n java-ms
secret/postgres-credentials created
$ kubectl get secret postgres-credentials -n java-ms
NAME                   TYPE     DATA   AGE
postgres-credentials   Opaque   1      14s
$ helm lint ./java-ms
==> Linting ./java-ms
[INFO] Chart.yaml: icon is recommended

1 chart(s) linted, 0 chart(s) failed
$ helm install myservices ./java-ms  -n java-ms --wait --timeout 5m
NAME: myservices
LAST DEPLOYED: Tue Nov 10 19:31:23 2026
NAMESPACE: java-ms
STATUS: deployed
REVISION: 1
TEST SUITE: None
$ 

running the fontend and tunneling the container
-----------------------------------------------------
minikube service frontend-service -n java-ms




