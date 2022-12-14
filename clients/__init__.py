import json


class JsonResponse:
    def __init__(self, body, status, raw_body):
        self.body = body
        self.status = status
        self.raw_body = raw_body


def parse_response(resp):
    r"""
    :return: parsed Python object from Response
    :param resp: Response from API call :class:`Response <Response>` object
    """
    if resp.status_code in (200, 201, 203, 204):
        body = resp.content and json.loads(resp.content)
    else:
        body = None

    status = resp.status_code
    print(f"Response is parsed with status {status} and body {body}")
    return JsonResponse(body, status, resp.content)
