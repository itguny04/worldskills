## AWS ALB Ingress Controller Setup

1. 클러스터의 IAM OIDC 자격 증명 공급자 생성  
```
eksctl utils associate-iam-oidc-provider --cluster wsi-cluster --approve
```

2. 정책 다운로드  
```
curl -o iam_policy.json https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.3.1/docs/install/iam_policy.json
```

3. 정책 생성  
```
aws iam create-policy --policy-name AWSLoadBalancerControllerIAMPolicy --policy-document file://iam_policy.json
```

4. 서비스 유저 생성  
```
eksctl create iamserviceaccount \
  --cluster=wsi-cluster \
  --namespace=kube-system \
  --name=aws-load-balancer-controller \
  --attach-policy-arn=arn:aws:iam::060764678458:policy/AWSLoadBalancerControllerIAMPolicy \
  --override-existing-serviceaccounts \
  --approve
```

5. Helm Repo 추가  
```
helm repo add eks https://aws.github.io/eks-charts
```

6. AWS ALB Ingress Controller 설치  
  ```
  helm install aws-load-balancer-controller eks/aws-load-balancer-controller \
    --set clusterName=wsi-cluster \
    --set serviceAccount.create=false \
    --set region=ap-northeast-2 \
    --set vpcId=vpc-0490bad6e4a303b21 \
    --set serviceAccount.name=aws-load-balancer-controller \
    -n kube-system
  ```

6. Ingress 생성 및 서비스 생성 등  
