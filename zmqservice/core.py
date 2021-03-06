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

import os
import sys
import signal
import logging
import threading
import zmq

from .error import EncodeError
from .error import DecodeError
from .error import AuthenticateError
from .error import AuthenticatorInvalidSignature
from .error import EndpointError

def setGlobalContext():
    procId = getattr(zmq, 'procId', None)
    # This is the first import or ...
    # This is a new process (from a fork or similar), the old context is stale
    if (procId is None and getattr(zmq, 'context', None) is None) or \
       procId != os.getpid():

        zmq.context = zmq.Context()
        zmq.procId = os.getpid()

class Endpoint(object):

    """ An Endpoints sends and receives messages

    Processing incoming messages:
        socket receive -> verify(*) -> decode

    Processing outgoing messages:
        encode -> sign(*) -> socket send

    (*) Sign/Verify only if authenticator is available
    """

    # pylint: disable=too-many-arguments
    # pylint: disable=no-member
    def __init__(self, socket, address, bind, encoder, authenticator,
                 timeouts=(None, None), logger=None):

        # timeouts must be a pair of the form:
        # (send-timeout-value, recv-timeout-value)

        self.socket = socket
        self.address = address
        self.bind = bind
        self.encoder = encoder
        self.authenticator = authenticator
        self.logger = logger or logging.getLogger()
        self.initialize(timeouts)

    def initialize(self, timeouts):
        """ Bind or connect the zmq socket to some address """

        # Bind or connect to address
        try:
            if self.bind is True:
                self.socket.bind(self.address)
            else:
                self.socket.connect(self.address)
        except zmq.error.ZMQError:
            self.socket.connect(self.address)

        # Set send and recv timeouts
        self._set_timeouts(timeouts)

    def _set_timeouts(self, timeouts):
        #Set socket timeouts for send and receive respectively

        (send_timeout, recv_timeout) = (None, None)

        try:
            (send_timeout, recv_timeout) = timeouts
        except TypeError:
            raise EndpointError(
                '`timeouts` must be a pair of numbers (2, 3) which represent '
                'the timeout values for send and receive respectively')

        if send_timeout is not None:
            self.socket.setsockopt(zmq.SNDTIMEO, send_timeout)

        if recv_timeout is not None:
            self.socket.setsockopt(zmq.RCVTIMEO, recv_timeout)

    def send(self, payload):
        """ Encode and sign (optional) the send through socket """
        payload = self.encode(payload)
        payload = self.sign(payload)
        self.socket.send(payload)

    def receive(self, decode=True):
        """ Receive from socket, authenticate and decode payload """
        payload = self.socket.recv()
        payload = self.verify(payload)
        if decode:
            payload = self.decode(payload)
        return payload

    def sign(self, payload):
        """ Sign payload using the supplied authenticator """
        if self.authenticator:
            return self.authenticator.signed(payload)
        return payload

    def verify(self, payload):
        """ Verify payload authenticity via the supplied authenticator """
        if not self.authenticator:
            return payload
        try:
            self.authenticator.auth(payload)
            return self.authenticator.unsigned(payload)
        except AuthenticatorInvalidSignature:
            raise
        except Exception as exception:
            raise AuthenticateError(str(exception))

    def decode(self, payload):
        """ Decode payload """
        try:
            return self.encoder.decode(payload)
        except Exception as exception:
            raise DecodeError(str(exception))

    def encode(self, payload):
        """ Encode payload """
        try:
            return self.encoder.encode(payload)
        except Exception as exception:
            raise EncodeError(str(exception))


class Process(object):
    """ A long running process """

    def start(self):
        """ Start and listen for calls """

        if threading.current_thread().name == 'MainThread':
            signal.signal(signal.SIGINT, self.stop)

        self.logger.debug('Starting ZMQProcess on {}'.format(self.address))

        while True:
            self.process()

    def stop(self, dummy_signum=None, dummy_frame=None):
        """ Shutdown process (this method is also a signal handler) """
        self.logger.debug('Stopping ZMQProcess')
        self.socket.close()
        sys.exit(0)
