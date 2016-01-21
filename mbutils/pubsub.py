class Notifier(object):
    def __init__(self):
        self.event_map = {}

    def publish(self, event_name, *args, **kwargs):
        callbacks = self.event_map.get(event_name, [])
        [f(event_name, *args, **kwargs) for f in callbacks]

    def subscribe(self, event_name, callback):
        self.event_map.setdefault(event_name, set()).add(callback)

    def unsubscribe(self, event_name, callback):
        self.event_map.setdefault(event_name, set()).remove(callback)

_notifier = Notifier()

def publish(event_name, *args, **kwargs):
    _notifier.publish(event_name, *args, **kwargs)

def subscribe(event_name, callback):
    _notifier.subscribe(event_name, callback)
