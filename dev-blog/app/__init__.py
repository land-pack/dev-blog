import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_openid import OpenID
from config import basedir



app = Flask(__name__)
app.config.from_object("config")
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
oid = OpenID(app, os.path.join(basedir, 'tmp'))
db = SQLAlchemy(app)
app.debug=True
"""
If you are wondering why the import statement is at the end and not at 
the beginning of the script as it is always done, the reason is to avoid 
circular references, because you are going to see that the views module 
needs to import the app variable defined in this script. Putting the 
import at the end avoids the circular import error.
"""
from app import views, models
