import redis
import msgpack

from mbutils import pubsub

class CacheKeyNotExists(Exception):
    pass

_conn = None
def _pack(val):
    return msgpack.packb(val, encoding='utf-8')

def _unpack(val):
    return msgpack.unpackb(val, encoding='utf-8')

def init(host='localhost', port=6379):
    global _conn
    _conn = redis.StrictRedis(host=host, port=port)

class Cache(object):
    prefix='default'
    version='1.0'
    evict_at = []
    def __init__(self):
        self.hit_cnt = 0
        self.miss_cnt = 0
        [pubsub.subscribe(e, self.on_evict) for e in self.evict_at]

    def cache_key(self, key):
        return '{}-{}:{}'.format(self.prefix, self.version, key)

    def on_evict(self, event_name, key):
        self.conn.delete(self.cache_key(key))

    def get(self, key):
        try:
            val = self.get_from_cache(key)
            self.hit_cnt += 1
        except CacheKeyNotExists:
            val = self.get_from_backend(key)
            self.miss_cnt += 1
            self.set(key, val)
        return val

    def set(self, key, val):
        self.conn.set(self.cache_key(key), _pack(val))

    def get_from_cache(self, key):
        val = self.conn.get(self.cache_key(key))
        if val is None:
            raise CacheKeyNotExists()
        return _unpack(val)

    def get_from_backend(self, key):
        raise NotImplemented()

    def status(self):
        return {
            'hit': self.hit_cnt,
            'miss': self.miss_cnt
            }

    @property
    def conn(self):
        return _conn
