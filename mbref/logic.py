#!/usr/bin/env python
import time
from hashlib import sha1

from mbref.extensions import db
from mbref.models.user import User, FollowRelation
from mbref.models.feed import Feed

def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return None
    return user.to_dict()

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
    rows = FollowRelation.query.filter_by(user_id = user_id).all()
    followers = User.query.filter(User.id.in_([r.follower_id for r in rows])).all()
    return [f.to_dict() for f in followers]

def get_followings(user_id):
    rows = FollowRelation.query.filter_by(follower_id = user_id).all()
    followings = User.query.filter(User.id.in_([r.user_id for r in rows])).all()
    return [f.to_dict() for f in followings]

def is_following(user_id, other_id):
    return bool(FollowRelation.query.filter_by(follower_id=user_id, user_id=other_id).first())

def follow(user_id, other_id):
    if is_following(user_id, other_id):
        return False
    follow_relation = FollowRelation(follower_id = user_id, user_id = other_id)
    db.session.add(follow_relation)
    db.session.commit()
    return True

def unfollow(user_id, other_id):
    follow_relation = FollowRelation.query.filter_by(follower_id=user_id, user_id=other_id).one()
    if follow_relation:
        db.session.delete(follow_relation)
        db.session.commit()
        return True
    else:
        return False

def get_user_feeds(user_id):
    feeds = (Feed.query.filter_by(user_id = user_id)
             .order_by(Feed.time_created.desc()).all())
    return [f.to_dict() for f in feeds]

def get_friend_feeds(user_id):
    followings = FollowRelation.query.filter_by(follower_id = user_id).all()
    following_ids = [f.user_id for f in followings]
    feeds = (Feed.query.filter(Feed.user_id.in_(following_ids))
             .order_by(Feed.time_created.desc()).all())
    return [f.to_dict() for f in feeds]

def get_feed(feed_id):
    feed = Feed.query.filter_by(id = feed_id).first()
    if not feed:
        return None
    else:
        return feed.to_dict()

def post_feed(user_id, content, time_created=None):
    if not time_created:
        time_created = int(time.time())
    feed = Feed(user_id=user_id, content=content, time_created=time_created)
    db.session.add(feed)
    db.session.commit()
    return feed.to_dict()

def clear_all():
    db.drop_all()
    db.create_all()
