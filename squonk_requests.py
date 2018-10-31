import requests


def check_response(response):
    if not response.status_code == 200:
        response.raise_for_status()


# uses https protocol
def get_token(content_type, grant_type, client_id, client_secret, url):

    # -H option in curl request
    headers = {
        'Content-Type': content_type,
    }

    # data to pass: -d in curl request
    data = {
        'grant_type': grant_type,
        'client_id': client_id,
        'client_secret': client_secret,
    }

    # post the request to the token url
    response = requests.post(url, headers=headers, data=data, verify=False)

    check_response(response)

    # return token as string
    token = str(response.json()['access_token'].decode('ascii'))

    return token


# uses http protocol
def list_service_ids(token, url):

    headers = {
        'authorization': str('bearer ' + token)
    }

    # post the request
    response = requests.post(url, headers=headers, verify=False)

    check_response(response)

    out = [method['id'] for method in response.json()]
    return out


def post_job(token, base_url, job_service_endpoint, username, options, input_data, input_metadata, service_id):

    url = str(base_url + '/' + job_service_endpoint + '/' + service_id)

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

    check_response(response)

    job_id = str(response.json()['job_id'])

    return job_id


