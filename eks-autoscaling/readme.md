## Cluster AutoScaler & Horizotal Pod AutoScaler

1. Cluster AutoScaler Setup  
[AWS Cluster AutoScaling - AWS Official Document](https://docs.aws.amazon.com/ko_kr/eks/latest/userguide/autoscaling.html)


2. Horizontal Pod AutoScaler Setup
  1) [K8S Metric Server - K8S Official Document](https://github.com/kubernetes-sigs/metrics-server)
  ```
  kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
  ``` 
  2) [K8S HPA](https://v1-22.docs.kubernetes.io/ko/docs/tasks/run-application/horizontal-pod-autoscale-walkthrough/)