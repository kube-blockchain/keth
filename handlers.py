'''Handlers for the keth operator
'''
# pylint: disable=missing-function-docstring
import datetime
import kopf


GROUP = 'ethereum.kube-blockchain.io'
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
def ensure_deployment(spec, name, namespace, logger, **_):
    logger.info('spec %s', spec)
    logger.info('name %s', name)
    logger.info('namespace %s', namespace)
