def check_response(response):
    if not response.status_code == 200:
        response.raise_for_status()
