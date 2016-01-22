#!/usr/bin/env python
from flask import abort, request
from schema import Schema, Optional, SchemaError

from asura import logic
from asura.www.base import json_request, route

@route('/ping', methods=['GET'])
def ping():
    return 'pong'

@route('/users/<user_id>', methods=['GET'])
@json_request
def get_user(user_id):
    user = logic.get_user(user_id)
    return user if user else abort(404)

@route('/users/', methods=['POST'])
@json_request
def create_user():
    payload = request.get_json()
    try:
        Schema({
            'username': unicode,
            'email': unicode,
            'password': unicode,
            Optional('bio'): unicode,
            Optional('time_created'): int
            }).validate(payload)
    except SchemaError, e:
        return abort(400)
    return logic.create_user(**payload)

@route('/users/<user_id>/followers', methods=['GET'])
@json_request
def get_followers(user_id):
    return logic.get_followers(user_id)

@route('/users/<user_id>/followings', methods=['GET'])
@json_request
def get_followings(user_id):
    return logic.get_followings(user_id)

@route('/users/<user_id>/follow/<other_id>', methods=['POST'])
@json_request
def follow(user_id, other_id):
    return logic.follow(user_id, other_id)

@route('/users/<user_id>/unfollow/<other_id>', methods=['POST'])
@json_request
def unfollow(user_id, other_id):
    return logic.unfollow(user_id, other_id)

@route('/users/<user_id>/feeds', methods=['GET'])
@json_request
def get_user_feeds(user_id):
    return logic.get_user_feeds(user_id)

@route('/users/<user_id>/friend-feeds', methods=['GET'])
@json_request
def get_friend_feeds(user_id):
    return logic.get_friend_feeds(user_id)

@route('/feeds/<feed_id>', methods=['GET'])
@json_request
def get_feed(feed_id):
    feed = logic.get_feed(feed_id)
    return feed if feed else abort(404)

@route('/feeds/', methods=['POST'])
@json_request
def post_feed():
    payload = request.get_json()
    try:
        Schema({
            'user_id': int,
            'content': unicode,
            Optional('time_created'): int
            }).validate(payload)
    except SchemaError:
        return abort(400)
    return logic.post_feed(**payload)

@route('/clear-all', methods=['POST'])
@json_request
def clear_all():
    return logic.clear_all()
