def check_response(response):
    if not response.status_code == 200:
        print(response.content)
        response.raise_for_status()
