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

    config_map_genesis_tpl = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "templates/config-map-genesis.yaml",
    )
    config_map_genesis_name=f'{name}-genesis'
    with open(config_map_genesis_tpl, 'r') as template:
        config_map_genesis = yaml.safe_load(template.read().format(
            name=config_map_genesis_name,
            namespace=namespace,
        ))
    kopf.adopt(config_map_genesis)
    kubernetes.config.load_incluster_config()
    apps = kubernetes.client.AppsV1Api()
    core = kubernetes.client.CoreV1Api()
    try:
        core.create_namespaced_config_map(
            namespace,
            config_map_genesis,
        )
    except ApiException as error:
        if error.status != 409:
            raise

        core.patch_namespaced_config_map(
            config_map_genesis_name,
            namespace,
            config_map_genesis,
        )
