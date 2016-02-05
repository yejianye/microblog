import logging

from flask import Flask, request

from webrpc.serialize import pack, unpack

class ErrorCode(object):
    UnknownError = 1
    MethodNotFound = 10

def error(rc, msg):
    return {'rc': rc, 'msg': msg}

class Server(Flask):
    def __init__(self, service_name, service_obj):
        super(Server, self).__init__(service_name)
        self._service_obj = service_obj
        self.route('/ping', methods=['GET', 'POST'])(self.ping)
        self.route('/', methods=['POST'])(self.view)

    def ping(self):
        return 'pong'

    def view(self):
        payload = unpack(request.data)
        method = getattr(self._service_obj, payload['cmd'], None)
        if not method:
            return error(ErrorCode.MethodNotFound,
                         "Cannot find command {}".format(payload['cmd']))
        try:
            data = method(*payload['args'], **payload['kwargs'])
            return pack({
                'rc': 0,
                'data': data})
        except Exception, e:
            logging.exception("Error in executing command %s", payload['cmd'])
            return pack({
                'rc': getattr(e, 'code', ErrorCode.UnknownError),
                'err_msg': e.message
                })
