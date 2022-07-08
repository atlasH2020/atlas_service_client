from __future__ import annotations
from abc import ABC, abstractmethod


class AbstractServiceClientPersistence(ABC):

    @abstractmethod
    def get_service_registration_id(self, client_id, client_secret):
        pass

    @abstractmethod
    def get_service_registration_data_by_registration_id(self, service_registration_id):
        pass

    @abstractmethod
    def get_service_registration_data_by_auth_url(self, oauth2_auth_url):
        pass

    @abstractmethod
    def persist_client_registration_info(self, oauth2_auth_url, client_id, client_secret):
        pass

    @abstractmethod
    def get_oauth2_code_flow_state(self, state_id):
        pass

    @abstractmethod
    def persist_oauth2_authorization_code_flow_data(self, state_id, service_id, service_name, oauth2_auth_url,
                                                    oauth2_token_url):
        pass

    @abstractmethod
    def delete_oauth2_authorization_code_flow(self, state_id):
        pass

    @abstractmethod
    def persist_user_token(self, user_id, access_token, access_token_expires_in, refresh_token,
                           refresh_token_expires_in, registration_id):
        pass

    @abstractmethod
    def update_user_token(self, user_token_id, access_token, refresh_token):
        pass

    @abstractmethod
    def delete_user_token(self, user_id, registration_id):
        pass

    @abstractmethod
    def get_user_token_data_by_id(self, user_token_id):
        pass

    @abstractmethod
    def get_user_token_data(self, user_id, registration_id):
        pass

    @abstractmethod
    def persist_user_services(self, service_id, service_name, user_id, user_token_id):
        pass

    @abstractmethod
    def get_user_services_by_id(self, service_id):
        pass

    @abstractmethod
    def get_user_services_by_user_and_services_id(self, user_id, service_id):
        pass

    @abstractmethod
    def get_user_services(self, user_id, service_name):
        pass

    @abstractmethod
    def delete_user_services_by_service_id(self, service_id):
        pass

    @abstractmethod
    def delete_service_from_user_services(self, user_token_id):
        pass


class DummyServiceClientPersistence(AbstractServiceClientPersistence):

    def get_service_registration_id(self, client_id, client_secret):
        raise Exception('This is just a dummy persistence. You need to implement your own persistence client.'
                        'And set it in the service client.')

    def get_service_registration_data_by_registration_id(self, service_registration_id):
        raise Exception('This is just a dummy persistence. You need to implement your own persistence client.'
                        'And set it in the service client.')

    def get_service_registration_data_by_auth_url(self, oauth2_auth_url):
        raise Exception('This is just a dummy persistence. You need to implement your own persistence client.'
                        'And set it in the service client.')

    def persist_client_registration_info(self, oauth2_auth_url, client_id, client_secret):
        raise Exception('This is just a dummy persistence. You need to implement your own persistence client.'
                        'And set it in the service client.')

    def get_oauth2_code_flow_state(self, state_id):
        raise Exception('This is just a dummy persistence. You need to implement your own persistence client.'
                        'And set it in the service client.')

    def persist_oauth2_authorization_code_flow_data(self, state_id, service_id, service_name, oauth2_auth_url,
                                                    oauth2_token_url):
        raise Exception('This is just a dummy persistence. You need to implement your own persistence client.'
                        'And set it in the service client.')

    def delete_oauth2_authorization_code_flow(self, state_id):
        raise Exception('This is just a dummy persistence. You need to implement your own persistence client.'
                        'And set it in the service client.')

    def persist_user_token(self, user_id, access_token, access_token_expires_in, refresh_token,
                           refresh_token_expires_in, registration_id):
        raise Exception('This is just a dummy persistence. You need to implement your own persistence client.'
                        'And set it in the service client.')

    def update_user_token(self, user_token_id, access_token, refresh_token):
        raise Exception('This is just a dummy persistence. You need to implement your own persistence client.'
                        'And set it in the service client.')

    def delete_user_token(self, user_id, registration_id):
        raise Exception('This is just a dummy persistence. You need to implement your own persistence client.'
                        'And set it in the service client.')

    def get_user_token_data_by_id(self, user_token_id):
        raise Exception('This is just a dummy persistence. You need to implement your own persistence client.'
                        'And set it in the service client.')

    def get_user_token_data(self, user_id, registration_id):
        raise Exception('This is just a dummy persistence. You need to implement your own persistence client.'
                        'And set it in the service client.')

    def persist_user_services(self, service_id, service_name, user_id, user_token_id):
        raise Exception('This is just a dummy persistence. You need to implement your own persistence client.'
                        'And set it in the service client.')

    def get_user_services_by_id(self, service_id):
        raise Exception('This is just a dummy persistence. You need to implement your own persistence client.'
                        'And set it in the service client.')

    def get_user_services_by_user_and_services_id(self, user_id, service_id):
        raise Exception('This is just a dummy persistence. You need to implement your own persistence client.'
                        'And set it in the service client.')

    def get_user_services(self, user_id, service_name):
        raise Exception('This is just a dummy persistence. You need to implement your own persistence client.'
                        'And set it in the service client.')

    def delete_user_services_by_service_id(self, service_id):
        raise Exception('This is just a dummy persistence. You need to implement your own persistence client.'
                        'And set it in the service client.')

    def delete_service_from_user_services(self, user_token_id):
        raise Exception('This is just a dummy persistence. You need to implement your own persistence client.'
                        'And set it in the service client.')
