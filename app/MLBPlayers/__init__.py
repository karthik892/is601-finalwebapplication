from typing import List, Dict
import simplejson as json
from flask import Flask, Response, render_template, redirect, request
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

from flask_login import LoginManager

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'citiesData'
app.config['SECRET_KEY'] = 'secret-key-goes-here'
mysql.init_app(app)

from .auth import auth as auth_blueprint
from .auth import User
app.register_blueprint(auth_blueprint)

# blueprint for non-auth parts of app
from .main import main as main_blueprint
app.register_blueprint(main_blueprint)


login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT * FROM user WHERE id= '"+user_id+"'")
    row = cursor.fetchone()

    return User(row)