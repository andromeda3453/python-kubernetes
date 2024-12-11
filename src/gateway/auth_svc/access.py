import os, requests


def login(request):
    auth = request.authorization

    if not auth:
        return None, ("missing credentials", 401)

    basic_auth = (auth.username, auth.password)

    response = requests.post(
        f'http://{os.environ.get('AUTH_SVC_ADDRESS')/login}', auth=basic_auth
    )

    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)


def validate_token(request):
    """
    Validates JWT in user's request

    Args:
        request: HTTP request received from user

    """

    if "Authorization" not in request.headers:
        return None, ("missing credentials", 401)

    token = request.headers["Authorization"]

    if not token:
        return None, ("missing credentials", 401)

    response = requests.post(
        f"http://{os.environ.get("AUTH_SVC_ADDRESS")}/validate",
        headers={"Authorization": token},
    )

    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)
