'''Handlers for the keth operator
'''
# pylint: disable=missing-function-docstring
import os
import datetime

import kopf
import yaml
import kubernetes
from kubernetes.client.rest import ApiException


GROUP = 'kube-blockchain.io'
VERSION = 'v1'
PLURAL = 'ethereum'


def _timestamp():
    return datetime.datetime.utcnow().isoformat("T") + "Z"


@kopf.on.probe(id='now')
def get_current_timestamp(**_):
    return _timestamp()


@kopf.on.resume(GROUP, VERSION, PLURAL)
@kopf.on.create(GROUP, VERSION, PLURAL)
@kopf.on.update(GROUP, VERSION, PLURAL)
def ensure_deployment(name, namespace, logger, **_):
    logger.info('ensure_deployment')

    ensure_config_map_genesis(f'{name}-genesis', namespace)
    ensure_service_geth_api(f'{name}-geth-api', namespace)
    ensure_statefulset_geth_api(f'{name}-geth-api', namespace)


def ensure_config_map_genesis(name, namespace):
    template_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'templates',
        'config-map-genesis.yaml',
    )
    with open(template_file, 'r') as template:
        resource = yaml.safe_load(template.read().format(
            name=name,
            namespace=namespace,
        ))
    kopf.adopt(resource)
    kubernetes.config.load_incluster_config()
    client = kubernetes.client.CoreV1Api()
    try:
        client.create_namespaced_config_map(namespace, resource)
    except ApiException as error:
        if error.status != 409:
            raise
        client.patch_namespaced_config_map(name, namespace, resource)


def ensure_service_geth_api(name, namespace):
    template_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'templates',
        'service-geth-api.yaml',
    )
    with open(template_file, 'r') as template:
        resource = yaml.safe_load(template.read().format(
            name=name,
            namespace=namespace,
        ))
    kopf.adopt(resource)
    kubernetes.config.load_incluster_config()
    client = kubernetes.client.CoreV1Api()
    try:
        client.create_namespaced_service(namespace, resource)
    except ApiException as error:
        if error.status != 409:
            raise
        client.patch_namespaced_service(name, namespace, resource)


def ensure_statefulset_geth_api(name, namespace):
    template_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'templates',
        'statefulset-geth-api',
    )
    with open(template_file, 'r') as template:
        resource = yaml.safe_load(template.read().format(
            name=name,
            namespace=namespace,
        ))
    kopf.adopt(resource)
    kubernetes.config.load_incluster_config()
    client = kubernetes.client.AppsV1Api()
    try:
        client.create_namespaced_stateful_set(namespace, resource)
    except ApiException as error:
        if error.status != 409:
            raise
        client.patch_namespaced_stateful_set(name, namespace, resource)
