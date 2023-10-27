# k8s-locust
PoC of a load testing stress api with kubernetes deployment and cluster

Command cli to expose service:
$ kubectl port-forward svc/locust-master 8089:8089 -n locust


## Deploy Locust to Kubernetes

### Create `Locust` namespace and switch to `Locust` namespace

```bash
kubectl create namespace locust
kubectl config set-context --current --namespace=locust
```

### Create a ConfigMap containing locust-tasks folder items

`locust-tasks` contains your script and dependencies for load testing.

Your script must have the name `locustfile.py`.

```bash
kubectl create configmap locust-configmap --from-file=locust-tasks/
```
### Deploy

```bash
kubectl apply -f k8s/locust-master-deployment.yaml
kubectl apply -f k8s/locust-worker-deployment.yaml
```

### (Optional) Activate HPA

```bash
kubectl apply -f k8s/locust-worker-hpa.yaml
```

### Get external IP to access to Locust portal 

```bash
kubectl get svc locust-master -o jsonpath="{.status.loadBalancer.ingress[0].ip}"
```

### Launch Locust portal

`http://[external_ip]:8089`

### Delete created ressources

```bash
kubectl delete namespace locust
```


USEFUL LINKS
https://github.com/karol-brejna-i/locust-experiments/tree/master/kubernetes
https://github.com/vmallya-123/learn-locust/blob/main/distributed/k8s/master-controller-with-metrics.yaml
https://github.com/peter-evans/locust-docker/tree/master/kubernetes
https://github.com/jthin/locust-k8s/blob/master/README.md
https://github.com/koudaiii/distributed-load-testing-using-locust-on-aks/tree/main


