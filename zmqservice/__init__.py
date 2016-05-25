"""Main module for zmqservice"""

from zmqservice.reqrep import Requester, Responder
from zmqservice.pubsub import Subscriber, Publisher
from zmqservice.crypto import Authenticator
from zmqservice.error import (
    ZmqServiceError,
    ServiceError,
    ClientError,
    ConfigError,
    AuthenticatorInvalidSignature,
    RequestParseError,
    PublisherError,
    SubscriberError,
    EncodeError,
    DecodeError,
    AuthenticateError
)

__all__ = [
    'Requester', 'Responder', 'Subscriber', 'Publisher', 'Authenticator',
    'ZmqServiceError', 'ServiceError', 'ClientError', 'ConfigError',
    'AuthenticatorInvalidSignature', 'RequestParseError',
    'PublisherError', 'SubscriberError', 'EncodeError',
    'DecodeError', 'AuthenticateError'
]

""" # Deprication example...
######################################################################
# Emit warnings for deprecated components
######################################################################

import logging


class Service(Responder):

    def __init__(self, address, encoder=None, authenticator=None,
                 socket=None, bind=True):
        logging.warning('Service is deprecated; use Responder instead.')
        super(Service, self).__init__(
            address, encoder, authenticator, socket, bind)


class Client(Requester):

    def __init__(self, address, encoder=None, authenticator=None,
                 socket=None, bind=False):
        logging.warning('Client is deprecated; use Requester instead.')
        super(Client, self).__init__(
            address, encoder, authenticator, socket, bind)
"""
