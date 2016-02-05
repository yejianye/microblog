from bomb.mbsrv.models.base import db

class Feed(db.Model):
    __tablename__ = 'Feed'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, index=True)
    content = db.Column(db.String(1024))
    time_created = db.Column(db.Integer)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'content': self.content,
            'time_created': self.time_created
        }
