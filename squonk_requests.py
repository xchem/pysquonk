import requests


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

    # return token as string
    token = str(response.json()['access_token'].decode('ascii'))

    return token


