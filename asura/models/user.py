from asura.extensions import db

class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(64))
    bio = db.Column(db.String(255))
    time_created = db.Column(db.Integer)
    time_modified = db.Column(db.Integer)

    def get_followers(self):
        followers = FollowRelation.query.filter_by(user_id = self.id)

    def get_followings(self):
        followings = FollowRelation.query.filter_by(follower_id = self.id)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'bio': self.bio,
            'time_created': self.time_created,
            'time_modified': self.time_modified
        }

class FollowRelation(db.Model):
    __tablename__ = 'FollowRelation'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, index=True)
    follower_id = db.Column(db.Integer, index=True)

