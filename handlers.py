'''Handlers for the Ethereum operator
'''
# pylint: disable=missing-function-docstring
import os
import datetime
import kopf


def _timestamp():
    return datetime.datetime.utcnow().isoformat("T") + "Z"


@kopf.on.probe(id='now')
def get_current_timestamp(**_):
    return _timestamp()
