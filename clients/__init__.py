import json


class JsonResponse:
    def __init__(self, body, status):
        self.body = body
        self.status = status


def parse_response(resp):
    r"""
    :return: parsed Python object from Response
    :param resp: Response from API call :class:`Response <Response>` object
    """
    body = json.loads(resp.content)
    status = resp.status_code
    print(f"Response is parsed with status {status} and body {body}")
    return JsonResponse(body, status)
