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

## Install Keth

Add the keth helm repository.

```sh
helm repo add keth https://kube-blockchain.github.io/keth
```

Install Keth using Helm.

```sh
helm upgrade keth keth/keth \
  --create-namespace \
  --install \
  --namespace keth \
  --set 'image.pullPolicy=Always'
```

Check the status of the release.

```sh
kubectl get pods -l "app.kubernetes.io/name=keth,app.kubernetes.io/instance=keth" \
  --namespace keth
```

## Deploy a private ethereum network

```sh
export NAMESPACE=ethereum
```

```sh
export ACCOUNT_SECRET=<your-account-secret>
export ACCOUNT_PRIVATEKEY=<your-account-privatekey>
```

```sh
export WS_SECRET=<your-ws-secret>
```

```sh
kubectl create namespace "${NAMESPACE}"
```

```sh
kubectl create secret generic geth-account \
  --namespace "${NAMESPACE}" \
  --from-literal "accountPrivateKey=${ACCOUNT_PRIVATEKEY}" \
  --from-literal "accountSecret=${ACCOUNT_SECRET}"
```

```sh
kubectl create secret generic ethstats \
  --namespace "${NAMESPACE}" \
  --from-literal "WS_SECRET=${WS_SECRET}"
```

```sh
kubectl apply \
  --namespace "${NAMESPACE}" \
  --filename ./samples/private-chain.yaml
```

## Cleanup

Teardown the sample Ethereum network by deleting the namespace.

```sh
kubectl delete namespace "${NAMESPACE}"
```

Teardown Keth by uninstalling the Helm release and deleting the namespace.

```sh
helm uninstall keth --namespace keth
kubectl delete namespace keth
```
