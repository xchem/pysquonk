import configparser
import shutil, os
import requests
import curlify
import auth
from functions import check_response
from molops import dict_to_json_file


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
        self.job_id = None

    def post_job(self, input_files, input_names, service_name):
        url = str(self.base_url + '/' + self.job_post_endpoint + service_name)

        input_names = [str(x + '_data') for x in input_names]

        headers = {
            'Content-Type': 'multipart/mixed',
            'Accept-Encoding': 'gzip',
            'Authorization': str('bearer ' + self.token),
            'SquonkUsername': 'user101',
            'Accept': 'application/x-squonk-metadata+json'
        }

        meta_dict = {'type': 'org.squonk.types.MoleculeObject'}

        files = {'options': (None, {})}

        tmp_files = []

        for i in range(0, len(input_files)):
            shutil.copy(input_files[i], input_files[i].split('/')[-1])
            tmp_files.append(input_files[i].split('/')[-1])
            os.system(str('gzip ' + input_files[i].split('/')[-1]))
            input_files[i] = str(input_files[i].split('/')[-1] + '.gz')
            tmp_files.append(str(input_files[i]))

        for name, f in zip(input_names, input_files):
            files[name] = (f, open(f, 'rb'))
            meta_name = str(name.replace('_data', '_metadata'))
            meta_file = meta_name.replace('_metadata', '') + '.metadata'
            dict_to_json_file(outfile=meta_file, jdict=meta_dict)
            files[meta_name] = (meta_file, open(meta_file, 'rb'))
            tmp_files.append(meta_file)

        print(files)

        response = requests.post(url, headers=headers, files=files, verify=False, allow_redirects=True)
        # print(curlify.to_curl(response.request))
        check_response(response)

        job_json = response.json()
        self.job_id = job_json['jobDefinition']['jobId']
        job_status = job_json['status']

        for f in tmp_files:
            if os.path.isfile(f):
                os.remove(f)

        return self.job_id, job_status

    def check_job(self):
        if self.job_id:
            url = str(self.base_url + '/' + self.job_post_endpoint + self.job_id + '/status')
            print(url)
            headers = {'Authorization': str('bearer ' + self.token),
                       'SquonkUsername': 'user101'}

            response = requests.get(url, headers=headers, verify=False, allow_redirects=True)
            print(curlify.to_curl(response.request))
            print(response.content)
        else:
            raise Exception('Please submit a job first!')

