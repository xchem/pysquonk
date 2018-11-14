import yaml
import configparser
import requests
import json
import curlify

from functions import check_response


class SquonkJob:
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

    def post_job_from_yaml(self, ymlin, token):
        with open(ymlin, 'r') as ymlfile:
            job_setup = yaml.load(ymlfile)

        options = job_setup['options']
        inputs = job_setup['input_data']
        username = job_setup['username']
        service_name = job_setup['service_name']
        content_type = job_setup['content_type']

        url = str(self.base_url + '/' + self.job_post_endpoint + service_name)

        headers = {
            'Content-Type': content_type,
            'Authorization': str('bearer ' + token),
            'SquonkUsername': username,
        }

        files = {
            'options': (None, json.dumps(options))
        }

        for input_key in inputs.keys():
            files[input_key] = ((inputs[input_key]['name']), open((inputs[input_key]['name']), 'rb'),
                                inputs[input_key]['type'])

        print(files)

        response = requests.post(url, headers=headers, files=files, verify=False, allow_redirects=True)

        for resp in response.history:
            print(resp.status_code, resp.url)

        print(curlify.to_curl(response.request))

        check_response(response)

        job_id = response.json()

        return job_id
