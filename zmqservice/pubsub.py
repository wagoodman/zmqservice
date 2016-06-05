'''
The MIT License (MIT)

Copyright (c) 2016 Tony Walker

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''

import zmq
import logging

from .error import SubscriberError
from .error import DecodeError
from .error import RequestParseError
from .error import AuthenticateError
from .error import AuthenticatorInvalidSignature
from .core import Endpoint, Process, setGlobalContext
from .encoder import MsgPackEncoder, PickleEncoder


class Subscriber(Endpoint, Process):
    """ A Subscriber executes various functions in response to
    different subscriptions it is subscribed to """

    # pylint: disable=too-many-arguments
    # pylint: disable=no-member
    def __init__(self, address, encoder=None, authenticator=None,
                 socket=None, bind=None, timeouts=(None, None), logger=None):
        setGlobalContext()

        # Defaults
        socket = socket or zmq.context.socket(zmq.SUB)
        socket.linger = 0 # prevent hang on close
        encoder = encoder or PickleEncoder()

        if bind is None:
            if address.startswith("ipc:\\"):
                bind = True
            else:
                bind = False

        super(Subscriber, self).__init__(
            socket, address, bind, encoder, authenticator, timeouts, logger)

        self.methods = {}
        self.descriptions = {}

    def parse(self, subscription):
        """ Fetch the function registered for a certain subscription """
        subTag, message = subscription.split(" ",1)
        for name in self.methods:
            tag = bytes(name.encode('utf-8'))
            if subTag.startswith(tag):
                fun = self.methods.get(name)
                return subTag, message, fun
        return None, None, None

    def register(self, name, fun, description=None):
        raise SubscriberError('Operation not allowed on this type of service')

    # pylint: disable=no-member
    def subscribe(self, tag, fun, description=None):
        """ Subscribe to something and register a function """
        self.methods[tag] = fun
        self.descriptions[tag] = description
        self.socket.setsockopt(zmq.SUBSCRIBE, tag)

    # pylint: disable=logging-format-interpolation
    # pylint: disable=duplicate-code
    def process(self):
        """ Receive a subscription from the socket and process it """

        subscription = None
        result = None

        try:
            subscription = self.socket.recv()

        except AuthenticateError as exception:
            self.logger.error(
                'Subscriber error while authenticating request: {}'
                .format(exception), exc_info=1)

        except AuthenticatorInvalidSignature as exception:
            self.logger.error(
                'Subscriber error while authenticating request: {}'
                .format(exception), exc_info=1)

        except DecodeError as exception:
            self.logger.error(
                'Subscriber error while decoding request: {}'
                .format(exception), exc_info=1)

        except RequestParseError as exception:
            self.logger.error(
                'Subscriber error while parsing request: {}'
                .format(exception), exc_info=1)
        else:
            self.logger.debug(
                'Subscriber received payload: {}'
                .format(subscription))

        tag, message, fun = self.parse(subscription)
        message = self.verify(message)
        message = self.decode(message)

        try:
            result = fun(tag, message)
        except Exception as exception:
            self.logger.error(exception, exc_info=1)

        # Return result to check successful execution of `fun` when testing
        return result


class Publisher(Endpoint):
    """ A Publisher sends messages down the zmq socket """

    # pylint: disable=too-many-arguments
    # pylint: disable=no-member
    def __init__(self, address, encoder=None, authenticator=None,
                 socket=None, bind=True, timeouts=(None, None), logger=None):
        setGlobalContext()

        # Defaults
        socket = socket or zmq.context.socket(zmq.PUB)
        socket.linger = 0 # prevent hang on close
        encoder = encoder or PickleEncoder()

        super(Publisher, self).__init__(
            socket, address, bind, encoder, authenticator, timeouts, logger)

    def build_payload(self, tag, message):
        """ Encode, sign payload(optional) and attach subscription tag """
        message = self.encode(message)
        message = self.sign(message)
        #payload = bytes(tag.encode('utf-8')) +" " + message
        payload = "%s %s" % (tag, message)
        return payload

    def publish(self, tag, message):
        """ Publish a message down the socket """
        payload = self.build_payload(tag, message)
        self.socket.send(payload)
