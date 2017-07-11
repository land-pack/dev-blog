from flask_admin.contrib.sqla import ModelView
from app import db, admin


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    posts = db.relationship("Post", backref='author', lazy='dynamic')

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id) # python 2.x
        except NameError:
            return str(self.id) # python 3.x

    def __repr__(self):
        return '<User %r>' % (self.nickname)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)

class RecommendInfo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(16))
    com = db.Column(db.String(32))
    desc = db.Column(db.String(1024))
    timestamp = db.Column(db.DateTime)
    

    def __repr__(self):
        return '<Post %r>' % (self.name)

class AboutInfo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(16))
    greeting = db.Column(db.String(32))
    describer = db.Column(db.String(1024))
    services = db.Column(db.String(1024))
    timestamp = db.Column(db.DateTime)
    jobs = db.Column(db.String(16))
    
    def __repr__(self):
        return '<About %r>' % (self.username)


admin.add_view(ModelView(RecommendInfo, db.session))
admin.add_view(ModelView(AboutInfo, db.session))