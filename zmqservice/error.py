"""ZmqService Exceptions"""


class ZmqServiceError(Exception):
    """Base exception for Nanoservice"""
    pass


class ServiceError(ZmqServiceError):
    """Service Generic Exception"""
    pass


class ClientError(ZmqServiceError):
    """Client Generic Exception"""
    pass


class ConfigError(ZmqServiceError):
    """Config Generic Exception"""
    pass


class AuthenticatorInvalidSignature(ZmqServiceError):
    """ Message could not be authenticated """
    pass


class RequestParseError(ZmqServiceError):
    """ Message from client could not be parsed """
    pass


class PublisherError(ZmqServiceError):
    """Publisher Generic Exception"""
    pass


class SubscriberError(NameError):
    """Subscriber Generic Exception"""
    pass


class DecodeError(ServiceError):
    """ Cannot decode request """
    pass


class EncodeError(ServiceError):
    """ Cannot encode request """
    pass


class AuthenticateError(ServiceError):
    """ Cannot authenticate request """
    pass


class EndpointError(ServiceError):
    """ Endpoint Error """
    pass
