from flask import render_template, flash, redirect, url_for, session ,g, request, send_from_directory
from flask_login import login_user, logout_user, current_user, login_required
from app import app
from app import lm
from app import oid
from .forms import LoginForm, EmailForm
from .models import User
from werkzeug.routing import BaseConverter

class RegexConverter(BaseConverter):
	def __init__(self, url_map, *items):
		super(RegexConverter, self).__init__(url_map)
		self.regex = items[0]


app.url_map.converters['regex'] = RegexConverter


@app.context_processor
def inject_user():
	return dict(user_info=g.user_info)

@app.before_request
def query_user_info():
	g.user_info = {
		"username":"Frank AK",
		"job":"Python Developer ~"
	}

@app.route("/home")
def home():

	form = EmailForm()
	if form.validate_on_submit():
		print 'somethinf'
	return render_template("home.html", form=form)

@app.route("/about")
def about():
    form = EmailForm()
    if form.validate_on_submit():
        print 'somethinf'
    greeting = 'Hi, I am'
    username = 'Frank AK'
    describer = """
         <p>I am in the website field since 2004 Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin at quam at orci commodo hendrerit vitae nec eros. Vestibulum neque est, imperdiet nec tortor nec, tempor semper metus. <b>I am a developer</b>, et accumsan nisi. Duis laoreet pretium ultricies. Curabitur rhoncus auctor nunc congue sodales. Sed posuere nisi ipsum, eget dignissim nunc dapibus eget. Aenean elementum sollicitudin sapien ut sapien fermentum aliquet mollis. Curabitur ac quam orci sodales quam ut tempor. suspendisse, gravida in augue in, interdum <b><a href="work.html" data-toggle="tooltip" data-placement="top" title="Check out my work.">Work</a></b> bibendum dui. Suspendisse sit amet justo sit amet diam fringilla commodo. Praesent ac magna at metus malesuada tincidunt non ac arcu. Nunc gravida eu felis vel elementum. Vestibulum sodales quam ut tempor tempor Donec sollicitudin imperdiet nec tortor nec, tempor semper metus..</p>
    """
    services = [
                "Website Design",
                "Website Development",
                "Python Game Server",
                "Nginx",
                "Openresty",
                "Linux"
            ]

    return render_template("about.html", form=form, greeting=greeting, username=username, describer=describer, services=services)

@app.route("/contact")
def contact():
    form = EmailForm()
    if form.validate_on_submit():
        print 'somethinf'
    return render_template("contact.html", form=form)

@app.route("/work")
def work():
    form = EmailForm()
    if form.validate_on_submit():
        print 'somethinf'
    return render_template("work.html", form=form)

@app.route("/single")
def single():
    form = EmailForm()
    if form.validate_on_submit():
        print 'somethinf'
    return render_template("single.html", form=form)


@app.route("/mv")
def mv():
    #return send_from_directory("static", "1080p.mov")
    return '<h1>Hello</h1>'


@app.route('/email', methods=['GET','POST'])
def email(uuid):
    print 'recv a email'
    return render_template("single.html")

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
