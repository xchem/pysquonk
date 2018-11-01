import configparser
import requests

from auth import SquonkAuth
from functions import check_response


class SquonkServiceInfo:

    def __init__(self):
        settings_file = 'config.ini'
        settings = configparser.ConfigParser()
        settings._interpolation = configparser.ExtendedInterpolation()
        settings.read(settings_file)

        # general settings
        self.base_url = settings.get('general', 'base_url')

        # config read for list_service_ids
        self.ids_endpoint = settings.get('ids', 'endpoint')


    # uses http protocol
    def list_services(self, token=SquonkAuth().get_token()):

        url = str(self.base_url + '/' + self.ids_endpoint)

        headers = {
            'authorization': str('bearer ' + token),
        }

        # post the request
        response = requests.post(url, headers=headers, verify=False)

        check_response(response)

        return response

    def list_service_ids(self):

        response = self.list_services

        out = [method['id'] for method in response.json()]

        return out

    def list_service_info(self, service_id):

        response = self.list_services()

        out = [method for method in response.json() if method['id'] == service_id]

        return out

    def list_full_service_info(self, service_id, token=SquonkAuth().get_token()):
        url = str(self.base_url + '/' + self.ids_endpoint + '/' + service_id)

        headers = {
            'authorization': str('bearer ' + token),
        }

        # post the request
        response = requests.post(url, headers=headers, verify=False)

        check_response(response)

        return response.json()

    def list_service_info_field(self, service_id, field):

        response = self.list_full_service_info(service_id)

        field = response[field]

        return field