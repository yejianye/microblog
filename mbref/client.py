#!/usr/bin/env python
import requests

class Client(object):
    def __init__(self, api_url):
        self.api_url = api_url

    def _get(self, path, **kwargs):
        resp = requests.get(self.api_url + path, params=kwargs)
        if resp.status_code == 200:
            return resp.json()
        else:
            return {'err_code': resp.status_code, 'err_msg': resp.content}

    def _post(self, path, **kwargs):
        resp = requests.post(self.api_url + path, json=kwargs)
        if resp.status_code == 200:
            return resp.json()
        else:
            return {'err_code': resp.status_code, 'err_msg': resp.content}

    def get_user(self, user_id):
        return self._get('/users/{}'.format(user_id))

    def create_user(self, username, email, password, bio=''):
        return self._post('/users/',
                          username = username,
                          email = email,
                          password = password,
                          bio = bio)

    def follow(self, user_id, other_id):
        return self._post('/users/{}/follow/{}'.format(user_id, other_id))

    def unfollow(self, user_id, other_id):
        return self._post('/users/{}/unfollow/{}'.format(user_id, other_id))

    def get_followers(self, user_id):
        return self._get('/users/{}/followers'.format(user_id))

    def get_followings(self, user_id):
        return self._get('/users/{}/followings'.format(user_id))

if __name__ == '__main__':
    import random
    from pprint import pprint
    random_id = random.randint(1,100000)
    c = Client('http://localhost:7431')
    user = c.create_user('ryanye+{}'.format(random_id), 'yejianye+{}@gmail.com'.format(random_id), 'secret')
    pprint(user)
