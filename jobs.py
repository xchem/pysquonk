import configparser
import requests

from functions import check_response

class SubmitJob:

    def __init__(self):
        settings_file = 'config.ini'
        settings = configparser.ConfigParser()
        settings._interpolation = configparser.ExtendedInterpolation()
        settings.read(settings_file)

        # general settings
        self.base_url = settings.get('general', 'base_url')

        # config read for posting a job
        self.job_post_endpoint = settings.get('job', 'endpoint')
        self.job_post_content_type = settings.get('job', 'content_type')

    def post_job(self, token, username, options, input_data, input_metadata, service_id):

        url = str(self.base_url + '/' + self.job_post_endpoint + '/' + service_id)

        headers = {
            'Authorization': str('bearer ' + token),
            'Content-Type': self.job_post_content_type,
            'SquonkUsername': username,
        }

        files = {
            'options': options,
            'input_data': input_data,
            'input_metadata': input_metadata,
        }

        response = requests.post(url, headers=headers, files=files, verify=False)

        check_response(response)

        job_id = str(response.json()['job_id'])

        return job_id