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


def _template_file(file):
    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'templates', file
    )


def _template_load(file, **kwargs):
    template_file = _template_file('config-map-genesis.yaml')
    with open(template_file, 'r') as template:
        return yaml.safe_load(template.read().format(kwargs))


def _timestamp():
    return datetime.datetime.utcnow().isoformat("T") + "Z"


@kopf.on.probe(id='now')
def get_current_timestamp(**_):
    return _timestamp()


@kopf.on.resume(GROUP, VERSION, PLURAL)
@kopf.on.create(GROUP, VERSION, PLURAL)
@kopf.on.update(GROUP, VERSION, PLURAL)
def ensure_deployment(logger, name, namespace, spec, **_):
    logger.info('ensure_deployment')

    ensure_config_map_genesis(name, f'{name}-genesis', namespace)
    ensure_deployment_bootnode(name, f'{name}-bootnode', namespace)
    ensure_deployment_ethstats(name, namespace, spec)
    ensure_statefulset_geth_api(name, f'{name}-geth-api', namespace, spec)
    ensure_service_bootnode(name, f'{name}-bootnode', namespace)
    ensure_service_ethstats(name, f'{name}-ethstats', namespace)
    ensure_service_geth_api(name, f'{name}-geth-api', namespace)


def ensure_config_map_genesis(release, name, namespace):
    resource = _template_load(
        'config-map-genesis.yaml',
        name=name,
        namespace=namespace,
        release=release,
    )
    kopf.adopt(resource)
    kubernetes.config.load_incluster_config()
    client = kubernetes.client.CoreV1Api()
    try:
        client.create_namespaced_config_map(namespace, resource)
    except ApiException as error:
        if error.status != 409:
            raise
        client.patch_namespaced_config_map(name, namespace, resource)


def ensure_deployment_bootnode(release, name, namespace):
    template_file = _template_file('deployment-bootnode.yaml')
    with open(template_file, 'r') as template:
        resource = yaml.safe_load(template.read().format(
            name=name,
            namespace=namespace,
            release=release,
        ))
    kopf.adopt(resource)
    kubernetes.config.load_incluster_config()
    client = kubernetes.client.AppsV1Api()
    try:
        client.create_namespaced_deployment(namespace, resource)
    except ApiException as error:
        if error.status != 409:
            raise
        client.patch_namespaced_deployment(name, namespace, resource)


def ensure_deployment_ethstats(name, namespace, spec):
    template_file = _template_file('deployment-ethstats.yaml')
    with open(template_file, 'r') as template:
        resource = yaml.safe_load(template.read())

    resource['metadata']['labels']['app'] = 'ethstats'
    resource['metadata']['labels']['component'] = f'{name}-ethstats'
    resource['metadata']['name'] = f'{name}-ethstats'
    resource['metadata']['namespace'] = namespace
    resource['spec']['replicas'] = spec['ethstats']['replicas']
    resource['spec']['selector']['matchLabels']['component'] = f'{name}-ethstats'
    resource['spec']['template']['metadata'][
        'labels']['component'] = f'{name}-ethstats'
    container = resource['spec']['template']['spec']['containers'][0]
    container['image'] = spec['ethstats']['container']['image']

    kopf.adopt(resource)
    kubernetes.config.load_incluster_config()
    client = kubernetes.client.AppsV1Api()
    try:
        client.create_namespaced_deployment(namespace, resource)
    except ApiException as error:
        if error.status != 409:
            raise
        client.patch_namespaced_deployment(name, namespace, resource)


def ensure_service_bootnode(release, name, namespace):
    template_file = _template_file('service-bootnode.yaml')
    with open(template_file, 'r') as template:
        resource = yaml.safe_load(template.read().format(
            name=name,
            namespace=namespace,
            release=release,
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


def ensure_service_ethstats(release, name, namespace):
    template_file = _template_file('service-ethstats.yaml')
    with open(template_file, 'r') as template:
        resource = yaml.safe_load(template.read().format(
            name=name,
            namespace=namespace,
            release=release,
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


def ensure_service_geth_api(release, name, namespace):
    template_file = _template_file('service-geth-api.yaml')
    with open(template_file, 'r') as template:
        resource = yaml.safe_load(template.read().format(
            name=name,
            namespace=namespace,
            release=release,
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


def ensure_statefulset_geth_api(release, name, namespace, spec):
    template_file = _template_file('statefulset-geth-api.yaml')
    with open(template_file, 'r') as template:
        resource = yaml.safe_load(template.read().format(
            accountSecret=spec['account']['secret'],
            ethstatsSecret=spec['ethstats']['secret'],
            name=name,
            namespace=namespace,
            release=release,
            storageClassName=spec['geth']['storageClassName'],
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
