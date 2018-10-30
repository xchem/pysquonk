import requests
import json

def get_token(content_type, grant_type, client_id, client_secret, url):
    headers = {
        'Content-Type': content_type,
    }

    data = {
        'grant_type': grant_type,
        'client_id': client_id,
        'client_secret': client_secret,
    }

    response = requests.post(url, headers=headers, data=data, verify=False)
    json_data = json.loads(response)

    token = json_data['token']

    return token

