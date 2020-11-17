# Kubernetes Ethereum

![Maintenance](https://img.shields.io/maintenance/yes/2020)
![GitHub](https://img.shields.io/github/license/kube-blockchain/keth)
[![Gitter](https://badges.gitter.im/kube-blockchain/keth.svg)](https://gitter.im/kube-blockchain/keth?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)
![GitHub contributors](https://img.shields.io/github/contributors-anon/kube-blockchain/keth)
![GitHub commit activity](https://img.shields.io/github/commit-activity/y/kube-blockchain/keth)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/kube-blockchain/keth)

![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/kube-blockchain/keth?include_prereleases)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/kube-blockchain/keth/Docker)
![GitHub issues](https://img.shields.io/github/issues-raw/kube-blockchain/keth)
![GitHub closed issues](https://img.shields.io/github/issues-closed/kube-blockchain/keth)
![GitHub Repo stars](https://img.shields.io/github/stars/kube-blockchain/keth?label=github%20stars)

![Docker Cloud Build Status](https://img.shields.io/docker/cloud/build/kubeblockchain/keth)
![Docker Pulls](https://img.shields.io/docker/pulls/kubeblockchain/keth.svg)
![Docker Image Version (latest by date)](https://img.shields.io/docker/v/kubeblockchain/keth?label=image%20version)
![Docker Image Size (latest by date)](https://img.shields.io/docker/image-size/kubeblockchain/keth)
![Docker Stars](https://img.shields.io/docker/stars/kubeblockchain/keth)

------------------------------------------------------------

Kubernetes implementation of the Ethereum protocol.

```sh
kubectl create namespace keth
helm repo add keth https://kube-blockchain.github.io/keth
helm repo update
helm upgrade keth keth/keth \
  --namespace keth \
  --install
```

```sh
kubectl create namespace samples
```

```sh
export ACCOUNT_SECRET=<your-account-secret>
export ACCOUNT_PRIVATEKEY=<your-account-privatekey>
```

```sh
kubectl create secret generic geth-account \
  --namespace samples \
  --from-literal "accountPrivateKey=${ACCOUNT_PRIVATEKEY}" \
  --from-literal "accountSecret=${ACCOUNT_SECRET}"
```

```sh
export WS_SECRET=<your-ws-secret>
```

```sh
kubectl create secret generic ethstats \
  --namespace samples \
  --from-literal "WS_SECRET=${WS_SECRET}"
```

```sh
kubectl apply \
  --namespace samples \
  --filename ./samples/private-chain.yaml
```

```sh
kubectl delete namespace samples
```

```sh
helm uninstall keth --namespace keth
kubectl delete namespace keth
```
