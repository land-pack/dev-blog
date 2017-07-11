# coding=utf8
from flask import render_template, flash, redirect, url_for, session, g, request, send_from_directory
from flask_login import login_user, logout_user, current_user, login_required
from app import app
from app import lm
from app import oid
from app import admin
from .forms import LoginForm, EmailForm
from .models import User, RecommendInfo, AboutInfo, ContactInfo, ContectSubjects
from werkzeug.routing import BaseConverter


class RegexConverter(BaseConverter):

    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


app.url_map.converters['regex'] = RegexConverter


@app.context_processor
def inject_user():
    return dict(user_info=g.user_info)


@app.context_processor
def inject_email_form():
    form = EmailForm(request.form)
    return dict(form=form)


@app.before_request
def query_user_info():
    d = AboutInfo.query.first() or {}
    g.user_info = {
        "username": d.username if d else 'set your name ~',
        "job": d.jobs if d else "set your jobs ~"
    }


@app.route("/home", methods=['GET', 'POST'])
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    about_query = AboutInfo.query.first()
    services = about_query.services.split('|')
    return render_template("about.html", about_data=about_query, services=services)


@app.route("/contact")
def contact():
    subjects = ContectSubjects.query.all()
    d = ContactInfo.query.first() or default_data
    reco = RecommendInfo.query.all()
    return render_template("contact.html", d=d, recommends=reco, subjects=subjects)


@app.route("/work")
def work():
    return render_template("work.html")


@app.route("/single")
def single():
    return render_template("single.html")


@app.route("/mv")
def mv():
    # return send_from_directory("static", "1080p.mov")
    return '<h1>Hello</h1>'


@app.route('/email', methods=['GET', 'POST'])
def email(uuid):
    print 'recv a email'
    return render_template("single.html")


@app.before_request
def before_request():
    g.user = current_user


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

#o
@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == '':
        flash("Invalid login, Please try again.")
        return redirect(url_for('login'))
    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        user = User(nickname=nickname, email=resp.email)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember=remember_me)
    return redirect(the_request.args.get('next') or url_for('index'))


@app.route("/")
@app.route("/index")
def index():
    user = g.user
    posts = [
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template("index.html", title="Home", user=user, posts=posts)


@app.route("/login", methods=['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS']
                           )


@app.route("/logout")
def logout():
    login_user()
    return redirect(url_for('index'))
