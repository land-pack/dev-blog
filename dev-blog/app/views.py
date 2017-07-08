from flask import render_template, flash, redirect, url_for, session ,g, request
from flask_login import login_user, logout_user, current_user, login_required
from app import app
from app import lm
from app import oid
from .forms import LoginForm
from .models import User

@app.route("/test")
def test():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("_base.html")

@app.route("/work")
def work():
    return render_template("_base.html")

@app.before_request
def before_request():
    g.user = current_user

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

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
    login_user(user, remember = remember_me)
    return redirect(request.args.get('next') or url_for('index'))


@app.route("/")
@app.route("/index")
def index():
    user = g.user
    posts = [
        {
            'author':{'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author':{'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template("index.html", title="Home", user=user, posts=posts)


@app.route("/login", methods=['GET','POST'])
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
