import random

import requests

from mbref.client import Client

api_url = 'http://localhost:7431'
c = Client(api_url)

def _mock_user(uid=None):
    if not uid:
        uid = random.randint(1, 1<<32)
    return dict(
        username = 'tester+{}'.format(uid),
        email = 'tester+{}@microblog.com'.format(uid),
        password = 'secret',
        bio = "I'm tester ({})".format(uid)
    )

def test_bad_request():
    result = requests.post('{}/users/'.format(api_url), json={'foo': 'bar'})
    assert result.status_code == 400

def test_user():
    # create user
    user_info = _mock_user()
    u = c.create_user(**user_info)
    assert u['username'] == user_info['username']
    assert u['email'] == user_info['email']
    assert u['bio'] == user_info['bio']
    assert 'password' not in u

    # fetch user
    fetched = c.get_user(u['id'])
    assert fetched['username'] == u['username']
    assert fetched['email'] == u['email']
    assert fetched['bio'] == u['bio']

def test_follow():
    u1 = c.create_user(**_mock_user())
    u2 = c.create_user(**_mock_user())
    u3 = c.create_user(**_mock_user())
    c.follow(u1['id'], u2['id'])
    c.follow(u1['id'], u3['id'])

    # check followings
    followings = c.get_followings(u1['id'])
    assert len(followings) == 2
    assert u2['id'] in [x['id'] for x in followings]
    assert u3['id'] in [x['id'] for x in followings]

    # check followers
    followers = c.get_followers(u2['id'])
    assert len(followers) == 1
    follower = followers[0]
    assert follower['id'] == u1['id']
    assert follower['username'] == u1['username']

    # unfollow
    c.unfollow(u1['id'], u3['id'])
    followings = c.get_followings(u1['id'])
    assert u3['id'] not in [x['id'] for x in followings]

def test_feeds():
    u1 = c.create_user(**_mock_user())
    u2 = c.create_user(**_mock_user())
    u3 = c.create_user(**_mock_user())
    c.follow(u3['id'], u1['id'])
    c.follow(u3['id'], u2['id'])

    # Reference time: 2016/01/14 6:45PM
    ref_ts = 1452768307

    # post feed and get feed
    f1 = c.post_feed(u1['id'], content='feed1', time_created=ref_ts - 100)
    assert c.get_feed(f1['id'])['content'] == 'feed1'

    # get user feed stream
    c.post_feed(u1['id'], content='feed2', time_created=ref_ts - 99)
    result = c.get_user_feeds(u1['id'])
    assert result[0]['content'] == 'feed2'
    assert result[1]['content'] == 'feed1'

    # friend feed stream
    c.post_feed(u2['id'], content='feed3', time_created=ref_ts - 98)
    result = c.get_friend_feeds(u3['id'])
    assert result[0]['content'] == 'feed3'
    assert result[1]['content'] == 'feed2'
    assert result[2]['content'] == 'feed1'
