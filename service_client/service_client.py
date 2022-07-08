from __future__ import annotations

import uuid
from abc import ABC, abstractmethod

from service_client.service_registry_factory.registry_client_factory import registry_client
from service_client.db.persistence_clients.service_client_persistence import AbstractServiceClientPersistence
from service_client.db.persistence_clients.service_client_persistence import DummyServiceClientPersistence
from urllib.parse import urlencode, urlparse
import requests
import json
import time
import os


class AbstractServiceClient(ABC):

    @abstractmethod
    def get_oauth2_auth_url(self):
        pass

    @abstractmethod
    def get_service_client_persistence(self):
        pass

    @abstractmethod
    def set_service_client_persistence(self, persistence_client):
        pass

    @abstractmethod
    def get_service_base_url(self):
        pass

    @abstractmethod
    def pair_service(self):
        pass

    @abstractmethod
    def systems_paired(self):
        pass

    @abstractmethod
    def pair_systems(self):
        pass

    @abstractmethod
    def service_endpoint_authentication(self):
        pass

    @abstractmethod
    def trigger_oauth2_authorization_code_flow(self):
        pass

    @abstractmethod
    def finalize_oauth2_authorization_code_flow(self, code, state, service_registration_id, oauth2_token_url, user_id,
                                                service_name):
        pass

    @abstractmethod
    def request_new_access_token(self, service_id, refresh_token, client_id, client_secret, user_token_id):
        pass


class ServiceClient(AbstractServiceClient):

    service_client_persistence: AbstractServiceClientPersistence

    def __init__(self, service_id, redirect_url):
        self.service_id = service_id
        self.service_registry_client = registry_client()
        self.service_client_persistence = DummyServiceClientPersistence()
        self.service_info = self.service_registry_client.get_service(self.service_id)
        self.service_pairing_info = self.service_registry_client.get_service_pairing_info(self.service_id)
        self.oauth2_token_url = self.service_pairing_info['oauth2_token_url']
        self.oauth2_auth_url = self.service_pairing_info['oauth2_auth_url']
        self.oauth2_grant_code_redirect_url = None
        self.redirect_url = redirect_url
        self.service_api_info = self.service_registry_client.get_service_api(self.service_id)
        self.service_base_url = self.service_api_info['service_base_url']

    def get_oauth2_auth_url(self):
        return self.oauth2_auth_url

    def get_service_client_persistence(self):
        return self.service_client_persistence

    def set_service_client_persistence(self, persistence_client):
        """
            Initially we have a DummyPersistenceClient initialized. This needs to be reset by the client
            that will be using this library with its own persistence client.
        """
        self.service_client_persistence = persistence_client

    def get_service_base_url(self):
        return self.service_base_url

    def pair_service(self):

        print('pairing with service', self.service_id)

        # #DEBUG
        print(self.service_info)
        # print(service_pairing_info)

        if self.systems_paired():
            # DEBUG
            print('systems are already paired')

        else:
            # DEBUG
            print('systems not paired yet')

            self.pair_systems()

        self.service_endpoint_authentication()

        return self.oauth2_grant_code_redirect_url

    def systems_paired(self):
        print(
            self.service_client_persistence.get_service_registration_data_by_auth_url(self.oauth2_auth_url) is not None)
        return self.service_client_persistence.get_service_registration_data_by_auth_url(
            self.oauth2_auth_url) is not None

    def pair_systems(self):
        """
            Fetch client registration info from registry if automatic registration. Otherwise provide it as
            environment variables. In our case we have manual registration, hence providing it as environment
            variables.

            client_registration_info = self.service_registry_client.register_service(self.service_id,
                                                                                 [self.redirect_url])
        """

        client_id = os.getenv('CLIENT_ID', 'hello_world_service')
        client_secret = os.getenv('CLIENT_SECRET', 'e8ec4c29-475b-456f-b3be-aa986c0acdc7')
        self.service_client_persistence.persist_client_registration_info(oauth2_auth_url=self.oauth2_auth_url,
                                                                         client_id=client_id,
                                                                         client_secret=client_secret)

    def service_endpoint_authentication(self):
        print('initiate service pairing...')
        if not self.service_info['enabled']:
            print('ERROR: service is not enabled')
            return None
        self.trigger_oauth2_authorization_code_flow()

    def trigger_oauth2_authorization_code_flow(self):

        print(f'triggering oauth2 authorization code flow with {self.oauth2_auth_url}...')
        print('\treading client credentials')

        client_credentials = self.service_client_persistence.get_service_registration_data_by_auth_url(
            self.oauth2_auth_url)

        print(
            f'\t\tclient id: {client_credentials.client_id}\n\t\tclient secret: {client_credentials.client_secret}')

        state_id = str(uuid.uuid4())
        auth_params = {'client_id': client_credentials.client_id, 'response_type': 'code', 'state': state_id,
                       'redirect_uri': self.redirect_url, 'scope': 'openid'}

        self.service_client_persistence.delete_oauth2_authorization_code_flow(state_id)
        self.service_client_persistence.persist_oauth2_authorization_code_flow_data(state_id,
                                                                                    self.service_id,
                                                                                    self.service_info['name'],
                                                                                    self.oauth2_auth_url,
                                                                                    self.oauth2_token_url)

        self.oauth2_grant_code_redirect_url = self.oauth2_auth_url + (
            '&' if urlparse(self.oauth2_auth_url).query else '?') + urlencode(auth_params)
        return self.oauth2_grant_code_redirect_url

    def finalize_oauth2_authorization_code_flow(self, code, state, service_registration_id, oauth2_token_url, user_id,
                                                service_name):
        # DEBUG
        print(f'finalizing oauth2 authorization code flow ...')
        print(f'\tstate: {state}')
        print(f'\tcode: {code}')
        print(f'\tredirect url: {self.redirect_url}')
        print(f'\tuser_id: {user_id}')

        service_registration_data = self.service_client_persistence.get_service_registration_data_by_registration_id(
            service_registration_id)

        client_id = service_registration_data.client_id
        client_secret = service_registration_data.client_secret

        # DEBUG
        print('\tclient id\t', client_id)
        print('\tclient secret\t', client_secret)

        data = {'grant_type': 'authorization_code',
                'code': code,
                'redirect_uri': self.redirect_url,
                'client_id': client_id,
                'client_secret': client_secret
                }

        access_token_response = requests.post(oauth2_token_url, data=data, verify=True, allow_redirects=False)

        if access_token_response.status_code != 200:
            err_res = json.loads(access_token_response.text)
            print('ERROR', access_token_response, err_res)

            if err_res['error'] == 'invalid_grant':
                print('token not active, initiate service pairing')
                self.service_client_persistence.delete_user_services_by_service_id(self.service_id)
                self.pair_service()
                return None

        token_data = json.loads(access_token_response.text)

        print(token_data)

        self.service_client_persistence.delete_user_token(user_id, service_registration_id)
        self.service_client_persistence.persist_user_token(user_id,
                                                           token_data['access_token'],
                                                           time.time() + token_data['expires_in'],
                                                           token_data['refresh_token'],
                                                           time.time() + token_data['refresh_expires_in'],
                                                           service_registration_id)

        user_token = self.service_client_persistence.get_user_token_data(user_id, service_registration_id)
        self.service_client_persistence.persist_user_services(self.service_id, service_name, user_id,
                                                              user_token.user_token_id)

    def request_new_access_token(self, service_id, refresh_token, client_id, client_secret, user_token_id):

        service_pairing_info = self.service_registry_client.get_service_pairing_info(service_id)
        print('Inside service client. Requesting new access token')

        refresh_params = {'grant_type': 'refresh_token',
                          'refresh_token': refresh_token,
                          'client_id': client_id,
                          'client_secret': client_secret}

        access_token_response = requests.post(service_pairing_info['oauth2_token_url'], data=refresh_params,
                                              verify=True, allow_redirects=False)

        if access_token_response.status_code != 200:
            err_res = json.loads(access_token_response.text)
            print('ERROR', access_token_response, err_res)

            if err_res['error'] == 'invalid_grant':
                print('token not active, initiate service pairing')
                self.service_client_persistence.delete_service_from_user_services(user_token_id)
                self.pair_service()
                return None

        else:
            print('updating access token')
            tokens = json.loads(access_token_response.text)
            self.service_client_persistence.update_user_token(user_token_id, tokens['access_token'],
                                                              tokens['refresh_token'])

        return tokens['access_token']
