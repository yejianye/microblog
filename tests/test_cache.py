from mbutils import pubsub
from mbutils.cache import Cache
from mbutils.cache import init as init_cache

class SummonStore(object):
    data = {
        'asura': {
            'hp': 3000,
            'mp': 200,
            },
        'bahamut': {
            'hp': 9999,
            'mp': 999,
            },
        'chocobo': {
            'hp': 100,
            'mp': 100
            }
        }
    default = {
        'hp': 0,
        'mp': 0,
        }

    def get(self, name):
        return self.data.get(name, self.default)

    def update(self, name, hp=None, mp=None):
        summon = self.data.setdefault(name, self.default.copy())
        if hp:
            summon['hp'] = hp
        if mp:
            summon['mp'] = hp
        pubsub.publish('summon_updated', name)

class SummonCache(Cache):
    evict_at = [
        'summon_updated',
    ]

    def __init__(self, store):
        super(SummonCache, self).__init__()
        self.store = store

    def get_from_backend(self, key):
        return self.store.get(key)

def test_cache():
    init_cache()
    store = SummonStore()
    cache = SummonCache(store)
    # cache miss
    assert cache.get('asura') == {'hp': 3000, 'mp': 200}
    assert cache.status() == {'hit': 0, 'miss': 1}
    # cache hit
    assert cache.get('asura') == {'hp': 3000, 'mp': 200}
    assert cache.status() == {'hit': 1, 'miss': 1}

    # update
    store.update('asura', hp=4000)
    assert cache.get('asura') == {'hp': 4000, 'mp': 200}
    assert cache.status() == {'hit': 1, 'miss': 2}
