import requests
import configparser


class SquonkRequests:

    def __init__(self):
        settings_file = 'config.ini'
        settings = configparser.ConfigParser()
        settings._interpolation = configparser.ExtendedInterpolation()
        settings.read(settings_file)

        # general settings
        self.base_url = settings.get('general', 'base_url')

        # config read for get_token
        self.token_content_type = settings.get('token', 'content_type')
        self.token_grant_type = settings.get('token', 'grant_type')
        self.token_client_id = settings.get('token', 'client_id')
        self.token_client_secret = settings.get('token', 'client_secret')
        self.token_url = settings.get('token', 'url')

        # config read for list_service_ids
        self.ids_endpoint = settings.get('ids', 'endpoint')

    def check_response(self, response):
        if not response.status_code == 200:
            response.raise_for_status()

    # uses https protocol
    def get_token(self):

        # -H option in curl request
        headers = {
            'Content-Type': self.token_content_type,
        }

        # data to pass: -d in curl request
        data = {
            'grant_type': self.token_grant_type,
            'client_id': self.token_client_id,
            'client_secret': self.token_client_secret,
        }

        # post the request to the token url
        response = requests.post(self.token_url, headers=headers, data=data, verify=False)

        self.check_response(response)

        # return token as string
        token = str(response.json()['access_token'].decode('ascii'))

        return token

    # uses http protocol
    def list_service_ids(self, token):

        url = str(self.base_url + '/' + self.ids_endpoint)

        headers = {
            'authorization': str('bearer ' + token),
        }

        # post the request
        response = requests.post(url, headers=headers, verify=False)

        self.check_response(response)

        out = [method['id'] for method in response.json()]

        return out

    def post_job(self, token, job_service_endpoint, username, options, input_data, input_metadata, service_id):

        url = str(self.base_url + '/' + job_service_endpoint + '/' + service_id)

        headers = {
            'Authorization': str('bearer ' + token),
            'Content-Type': 'multipart/mixed',
            'SquonkUsername': username,
        }

        files = {
            'options': options,
            'input_data': input_data,
            'input_metadata': input_metadata,
        }

        response = requests.post(url, headers=headers, files=files, verify=False)

        self.check_response(response)

        job_id = str(response.json()['job_id'])

        return job_id


