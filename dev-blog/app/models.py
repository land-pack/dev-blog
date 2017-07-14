from flask_admin.contrib.sqla import ModelView
from flask_admin.actions import action
from app import db, admin
from datetime import datetime
from wtforms.validators import DataRequired
from wtforms import TextAreaField
from wtforms.widgets import TextArea


class CKTextAreaWidget(TextArea):

    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()


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
            return unicode(self.id)  # python 2.x
        except NameError:
            return str(self.id)  # python 3.x

    def __repr__(self):
        return '<User %r>' % (self.nickname)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)


class RecommendInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16))
    com = db.Column(db.String(32))
    desc = db.Column(db.String(1024))
    timestamp = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return '<Post %r>' % (self.name)


class AboutInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16))
    greeting = db.Column(db.String(32))
    describer = db.Column(db.String(1024))
    services = db.Column(db.String(1024))
    jobs = db.Column(db.String(16))
    timestamp = db.Column(db.DateTime)

    def __repr__(self):
        return '<About %r>' % (self.username)


class ContactInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(16))
    email = db.Column(db.String(32))
    leisure = db.Column(db.String(1024))
    title = db.Column(db.String(128))
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return '<Contact %r>' % (self.phone)


class ContectSubjects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(64))

    def __repr__(self):
        return '<Subject %r>' % (self.id)


class MyModelView(ModelView):
    edit_template = 'microblog_edit.html'
    list_template = 'about_list.html'
    column_editable_list = ['jobs']
    form_choices = {
        'jobs': [
            ('MR', 'Ruby Dev'),
            ('ss', 'Java Dev'),
            ('python', 'Python Dev'),
            ('DR', 'C++'),
            ('PROF', 'Erlang')
        ]
    }
    can_export = True
    #create_modal = True
    #edit_modal = True
    form_args = {
        'username': {
            'label': 'username',
            'validators': [DataRequired(), ]
        }
    }
    form_widget_args = {
        'description': {
            'rows': 3,
            'style': 'color: black'
        }
    }

    @action('approve', 'Approve', 'Are you want to ')
    def action_approve(self, ids):
        pass

    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']

    form_overrides = {
        'content': CKTextAreaField
    }


class MessageAdmin(ModelView):
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']

    form_overrides = {
        'content': CKTextAreaField
    }

admin.add_view(ModelView(RecommendInfo, db.session))
admin.add_view(MyModelView(AboutInfo, db.session))
admin.add_view(MessageAdmin(ContactInfo, db.session))
admin.add_view(ModelView(ContectSubjects, db.session))
