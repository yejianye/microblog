#!/usr/bin/env python
import time
from hashlib import sha1

from mbutils.cache import Cache
from mbutils.cache import pubsub
from asura.extensions import db
from asura.models.user import User, FollowRelation
from asura.models.feed import Feed

class Event(object):
    FOLLOWER_UPDATED = 'follower_updated'
    FOLLOWING_UPDATED = 'following_updated'
    USER_FEEDS_UPDATED = 'user_feeds_updated'
    FRIEND_FEEDS_UPDATED = 'friend_feeds_updated'

class UserCache(Cache):
    prefix = 'user'
    def get_from_backend(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return None
        return user.to_dict()
user_cache = UserCache()

class FollowerCache(Cache):
    prefix = 'follower'
    evict_at = [
        Event.FOLLOWER_UPDATED
    ]
    def get_from_backend(self, user_id):
        rows = FollowRelation.query.filter_by(user_id = user_id).all()
        followers = User.query.filter(User.id.in_([r.follower_id for r in rows])).all()
        return [f.to_dict() for f in followers]
follower_cache = FollowerCache()

class FollowingCache(Cache):
    prefix = 'following'
    evict_at = [
        Event.FOLLOWING_UPDATED
    ]
    def get_from_backend(self, user_id):
        rows = FollowRelation.query.filter_by(follower_id = user_id).all()
        followings = User.query.filter(User.id.in_([r.user_id for r in rows])).all()
        return [f.to_dict() for f in followings]
following_cache = FollowingCache()

class FeedCache(Cache):
    prefix = 'feed'
    def get_from_backend(self, feed_id):
        feed = Feed.query.filter_by(id = feed_id).first()
        if not feed:
            return None
        else:
            return feed.to_dict()
feed_cache = FeedCache()

class UserFeedsCache(Cache):
    prefix = 'user_feeds'
    evict_at = [
        Event.USER_FEEDS_UPDATED
        ]
    def get_from_backend(self, user_id):
        feeds = (Feed.query.filter_by(user_id = user_id)
                .order_by(Feed.time_created.desc()).all())
        return [f.to_dict() for f in feeds]
user_feeds_cache = UserFeedsCache()

class FriendFeedsCache(Cache):
    prefix = 'friend_feeds'
    evict_at = [
        Event.FRIEND_FEEDS_UPDATED
        ]
    def get_from_backend(self, user_id):
        followings = FollowRelation.query.filter_by(follower_id = user_id).all()
        following_ids = [f.user_id for f in followings]
        feeds = (Feed.query.filter(Feed.user_id.in_(following_ids))
                .order_by(Feed.time_created.desc()).all())
        return [f.to_dict() for f in feeds]
friend_feeds_cache = FriendFeedsCache()

def get_user(user_id):
    return user_cache.get(user_id)

def create_user(username, email, password, bio='', time_created=None):
    if not time_created:
        time_created = int(time.time())
    user = User(username=username,
                email=email,
                password=sha1(password).hexdigest(),
                bio=bio,
                time_created = time_created,
                time_modified = time_created)
    db.session.add(user)
    db.session.commit()
    return user.to_dict()

def get_followers(user_id):
    return follower_cache.get(user_id)

def get_followings(user_id):
    return following_cache.get(user_id)

def is_following(user_id, other_id):
    return bool(FollowRelation.query.filter_by(follower_id=user_id, user_id=other_id).first())

def follow(user_id, other_id):
    if is_following(user_id, other_id):
        return False
    follow_relation = FollowRelation(follower_id = user_id, user_id = other_id)
    db.session.add(follow_relation)
    db.session.commit()
    pubsub.publish(Event.FOLLOWING_UPDATED, user_id)
    pubsub.publish(Event.FOLLOWER_UPDATED, other_id)
    return True

def unfollow(user_id, other_id):
    follow_relation = FollowRelation.query.filter_by(follower_id=user_id, user_id=other_id).one()
    if follow_relation:
        db.session.delete(follow_relation)
        db.session.commit()
        pubsub.publish(Event.FOLLOWING_UPDATED, user_id)
        pubsub.publish(Event.FOLLOWER_UPDATED, other_id)
        return True
    else:
        return False

def get_user_feeds(user_id):
    return user_feeds_cache.get(user_id)

def get_friend_feeds(user_id):
    return friend_feeds_cache.get(user_id)

def get_feed(feed_id):
    return feed_cache.get(feed_id)

def post_feed(user_id, content, time_created=None):
    if not time_created:
        time_created = int(time.time())
    feed = Feed(user_id=user_id, content=content, time_created=time_created)
    db.session.add(feed)
    db.session.commit()
    pubsub.publish(Event.USER_FEEDS_UPDATED, user_id)
    for u in get_followers(user_id):
        pubsub.publish(Event.FRIEND_FEEDS_UPDATED, u['id'])
    return feed.to_dict()

def clear_all():
    db.drop_all()
    db.create_all()
