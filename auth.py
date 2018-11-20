import requests
import configparser

from functions import check_response


class SquonkAuth:

    def __init__(self):
        settings_file = 'config.ini'
        settings = configparser.ConfigParser()
        settings._interpolation = configparser.ExtendedInterpolation()
        settings.read(settings_file)

        # config read for get_token
        self.token_content_type = settings.get('token', 'content_type')
        self.token_grant_type = settings.get('token', 'grant_type')
        self.token_client_id = settings.get('token', 'client_id')
        self.token_client_secret = settings.get('token', 'client_secret')
        self.token_url = settings.get('token', 'url')

    # uses https protocol
    def get_token(self):
        """Get a token from squonk's authorisation protocol. This should be posted with all further requests, and is
        valid for ~5 minutes."""

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

        check_response(response)

        # return token as string
        token = str(response.json()['access_token'])

        return token



