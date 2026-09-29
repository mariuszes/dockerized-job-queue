# Kubernetes setup commands

Short list of commands used to create the local cluster in kind and install components required by this project.

Run the commands from the repository root.

## Cluster
##### Multi-node kind cluster
```text
kind create cluster --config .\kind-config.yaml
kubectl apply -f .\k8s\namespace.yaml
kubectl config set-context --current --namespace=job-queue
```

## Application image
##### Build and load image into kind
```text
docker build -t dockerized-job-queue:local .
kind load docker-image dockerized-job-queue:local --name job-queue
```

## KEDA
##### Kubernetes Event-driven Autoscaling
```text
helm repo add kedacore https://kedacore.github.io/charts
helm repo update
helm install keda kedacore/keda --namespace keda --create-namespace
```

## Envoy Gateway
##### Gateway API controller and Envoy Proxy
```text
helm install eg oci://docker.io/envoyproxy/gateway-helm --version v1.9.1 -n envoy-gateway-system --create-namespace
```

## TLS certificate
##### RSA 2048 self-signed certificate and Kubernetes TLS Secret creation
```text
docker run --rm -v "${PWD}\k8s\kind\gateway\certs:/certs" alpine/openssl req -x509 -newkey rsa:2048 -nodes -sha256 -days 365 -keyout /certs/localhost.key -out /certs/localhost.crt -subj "/CN=localhost" -addext "subjectAltName=DNS:localhost"

kubectl create secret tls api-gateway-tls --cert=.\k8s\kind\gateway\certs\localhost.crt --key=.\k8s\kind\gateway\certs\localhost.key -n job-queue

```

## Kubernetes manifests
##### Apply project resources
```text
kubectl apply -k .\k8s\kind
```

## Check
```text
kubectl get pods -A
kubectl get gateway
kubectl get networkpolicy
kubectl get svc -n envoy-gateway-system
```

## Application
```text
HTTP:  http://localhost:30081/docs
HTTPS: https://localhost:30082/docs
```

## Delete cluster
```text
kind delete cluster --name job-queue
```
