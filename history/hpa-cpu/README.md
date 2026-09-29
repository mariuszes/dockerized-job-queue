# CPU-based HPA

Small experiment with Kubernetes Horizontal Pod Autoscaler based on worker CPU usage.

* **Install Metrics Server**

```text
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

* **Patch Metrics Server for local kind cluster**

Add `--kubelet-insecure-tls` to the Metrics Server container args.

In kind, kubelet certificates are not trusted by Metrics Server by default. This flag allows Metrics Server to collect CPU and memory metrics from kubelets without verifying those certificates.

Apply the saved patch:

```text
kubectl patch deployment metrics-server -n kube-system --type=json --patch-file .\history\hpa-cpu\metrics-patch.json
```

* **Verify metrics**

```text
kubectl top pods
```

* **Create HPA**

```text
kubectl apply -f .\history\hpa-cpu\worker-hpa.yaml
```

* **Observe scaling**

```text
kubectl get hpa worker-hpa -w
```
