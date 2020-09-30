'''Handlers for the keth operator
'''
# pylint: disable=missing-function-docstring
import datetime
import kopf


def _timestamp():
    return datetime.datetime.utcnow().isoformat("T") + "Z"


@kopf.on.probe(id='now')
def get_current_timestamp(**_):
    return _timestamp()
