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
        self.base_url = settings.get('general', 'job_base_url')

        # config read for posting a job
        self.job_post_endpoint = settings.get('job', 'endpoint')
        self.job_post_content_type = settings.get('job', 'content_type')

    def prepare_input_json(self, file, format, options):
        jdict = {
            'source': open(file, 'rb').read(),
            'format': format,
            'values': options,
                 }

        outfile = str(file.split('.')[0] + '.json')

        print(jdict)

        with open(outfile, 'w') as f:
            json.dump(jdict, f)

        return outfile

    def post_job_from_yaml(self, ymlin, token):
        with open(ymlin, 'r') as ymlfile:
            job_setup = yaml.load(ymlfile)

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

        infiles = {}

        for input_key in inputs.keys():
            outfile = self.prepare_input_json(file=inputs[input_key]['name'], format=inputs[input_key]['type'],
                                    options=inputs[input_key]['options'])
            infiles[input_key] = ((outfile), open(outfile, 'rb'))

        print(infiles)

        response = requests.post(url, headers=headers, files=infiles, verify=False, allow_redirects=True)
        check_response(response)

        job_json = response.json()
        job_id = job_json['jobDefinition']['jobId']
        job_status = job_json['status']

        print(str('job ' + str(job_id) + ' ' + str(job_status)))
        return job_id

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
