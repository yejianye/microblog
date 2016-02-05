import requests

from webrpc.serialize import pack, unpack

class HTTPError(Exception):
    def __init__(self, status_code, err_msg):
        message = 'Error code {}: {}'.format(status_code, err_msg)
        super(HTTPError, self).__init__(message)

class ServiceException(Exception):
    pass

class Client(object):
    def __init__(self, service_uri):
        self._service_uri = service_uri

    def execute(self, cmd, *args, **kwargs):
        payload = pack({
            'cmd': cmd,
            'args': args,
            'kwargs': kwargs
            })
        resp = requests.post(self._service_uri, data=payload)
        if resp.status_code != 200:
            raise HTTPError(resp.status_code, resp.content)
        result = unpack(resp.content)
        if result.get('rc', 0):
            raise ServiceException(result.get('err_msg', 'Unknown exception'))
        return result.get('data', {})
