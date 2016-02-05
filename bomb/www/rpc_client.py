from flask import current_app
from flask import _app_ctx_stack as stack

from webrpc.client import Client

class RPC(object):
    def __init__(self, service_name):
        self.service_name = service_name

    def execute(self, cmd, *args, **kwargs):
        ctx = stack.top
        if ctx is not None:
            if not hasattr(ctx, 'rpc_clients'):
                ctx.rpc_clients = {}
            if self.service_name not in ctx.rpc_clients:
                ctx.rpc_clients[self.service_name] = Client(self.service_url)
            return ctx.rpc_clients[self.service_name].execute(cmd, *args, **kwargs)

    @property
    def service_url(self):
        return current_app.config['SERVICE_URLS'][self.service_name]

    def __getattr__(self, attr):
        if attr.startswith('_'):
            raise AttributeError("{} object has no attribute {}".format(type(self).__name__, attr))
        return lambda *args, **kwargs: self.execute(attr, *args, **kwargs)
