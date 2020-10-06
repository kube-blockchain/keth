#!/usr/bin/env bash

export AWS_ACCESS_KEY_ID=AKIA5AFAEAL35OH3QD7M
export AWS_SECRET_ACCESS_KEY=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
eksctl create cluster \
  --alb-ingress-access \
  --appmesh-access \
  --asg-access \
  --external-dns-access \
  --full-ecr-access \
  --managed \
  --name apps-1 \
  --nodes-max 100 \
  --nodes-min 2 \
  --node-type m5.large \
  --node-volume-size 75 \
  --region us-east-1 \
  --version 1.17

kubectl get nodes

kubectl delete namespace keth
kubectl create namespace keth
kubectl apply --kustomize ./kustomize
kubectl -n keth get all