from __future__ import annotations
from abc import ABC, abstractmethod


from registry_client.service_registry_client import ServiceRegistryClient
from registry_client.service_registry_client import AbstractServiceRegistryClient
import os

"""
    Usage:
    registry_client object is made a callable object.
    Hence can be used like a function. registry_client() will return the ServiceRegistryClient Object.
"""


class AbstractRegistryClientFactory(ABC):

    @abstractmethod
    def get_registry_client(self, client_id, client_secret, token_url):
        pass


class RegistryClientFactory(AbstractRegistryClientFactory):

    def __get_client_credentials(self):
        client_id = os.getenv('REGISTRY_CLIENT_ID', '##########')
        client_secret = os.getenv('REGISTRY_CLIENT_SECRET', '########')
        token_url = 'https://sensorsystems.iais.fraunhofer.de/auth/realms/participants/protocol/openid-connect/token'
        return client_id, client_secret, token_url

    def get_registry_client(self) -> AbstractServiceRegistryClient:
        client_id, client_secret, token_url = self.__get_client_credentials()
        service_registry_client = ServiceRegistryClient(client_id, client_secret, token_url)
        service_registry_client.request_access_token()
        return service_registry_client


class RegistryClient:
    registry_factory: AbstractRegistryClientFactory

    def __init__(self, factory: AbstractRegistryClientFactory):
        self.registry_factory = factory

    def __call__(self):
        return self.registry_factory.get_registry_client()


registry_client = RegistryClient(RegistryClientFactory())
