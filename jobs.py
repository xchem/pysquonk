import yaml
import configparser
import requests
import json
import curlify
import auth
from functions import check_response


class SquonkJob:
    def __init__(self):
        settings_file = 'config.ini'
        settings = configparser.ConfigParser()
        settings._interpolation = configparser.ExtendedInterpolation()
        settings.read(settings_file)

        # general settings
        self.base_url = settings.get('general', 'job_base_url')

        # config read for posting a job
        self.job_post_endpoint = settings.get('job', 'endpoint')
        self.job_post_content_type = settings.get('job', 'content_type')
        self.auth = auth.SquonkAuth()
        self.token = self.auth.get_token()

    def post_job(self, input_json_files, input_json_metadata):
        url = str(self.base_url + '/' + self.job_post_endpoint + service_name)

        headers = {
            'Content-Type': 'mixed/multipart',
            'Authorization': str('bearer ' + self.token),
            'SquonkUsername': 'user101',
        }

        for input_key in inputs.keys():
            outfile = self.prepare_input_json(file=inputs[input_key]['name'], format=inputs[input_key]['type'],
                                    options=inputs[input_key]['options'])
            infiles[input_key] = ((outfile), open(outfile, 'rb'))

        response = requests.post(url, headers=headers, files=infiles, verify=False, allow_redirects=True)
        check_response(response)

        job_json = response.json()
        job_id = job_json['jobDefinition']['jobId']
        job_status = job_json['status']

        return job_id, job_status

    def check_job(self, idno, token):
        url = str(self.base_url + '/' + self.job_post_endpoint + idno + '/status')
        print(url)
        headers = {'Authorization': str('bearer ' + token),
                   'SquonkUsername': 'user101',
                   'Accept-Encoding': 'gzip'}

        response = requests.post(url, headers=headers, verify=False, allow_redirects=True)
        print(response.history)
        print(curlify.to_curl(response.request))
        print(response.content)

