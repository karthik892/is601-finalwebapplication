from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

import sendgrid
import os
from sendgrid.helpers.mail import *
import string
import random


from . import mysql

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

# mysql data is loaded as a dict, but login_user expects a class, this should bridge the gap
# Loosely based on https://stackoverflow.com/questions/53401996/attributeerror-dict-object-has-no-attribute-is-active-pymongo-and-flask
class User(UserMixin):
    userRow = None
    def __init__(self, user):
        self.userRow = user

    # Overriding get_id is required if you don't have the id property
    # Check the source code for UserMixin for details
    def get_id(self):
        return str(self.userRow["id"])

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT * FROM user WHERE email= '"+email+"' and email_verified=1")
    row = cursor.fetchone()


    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if row is None or not check_password_hash(row["password"], password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

    
    # if the above check passes, then we know the user has the right credentials
    login_user(User(row), remember=remember)
    return redirect(url_for('main.index'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    password = request.form.get('password')

    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT * FROM user WHERE email= '"+email+"'")
    user = cursor.fetchone()
    
    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('A user with this E-Mail address is already registered')
        return redirect(url_for('auth.signup'))


    # lets create a random key to make it harder to brute-force the email verification process
    letters = string.ascii_uppercase
    randomkey =  ''.join(random.choice(letters) for i in range(10)) 

    inputData = (email, generate_password_hash(password, method='sha256'), randomkey)

    sql_insert_query = """INSERT INTO user (`email`, `password`, `email_verified`, `email_key`) VALUES (%s, %s, 0, %s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()

    #send activation email
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("ks584@njit.edu")
    to_email = To(email)
    subject = "IS601 MLBPlayers - Email verification and account activation"
    content = Content("text/html", "<a href='http://127.0.0.1:5000/emailactivate?id="+randomkey+"' >Click here to activate your account</a>")
    mail = Mail(from_email, to_email, subject, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    """ print(response.status_code)
    print(response.body)
    print(response.headers) """
    flash('User created successfully, use the link in the verification email to activate your account.')
    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route("/emailactivate")
def activateEmail():
    emailkey = request.args.get("id")
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT * FROM user WHERE email_key= '"+emailkey+"'")

    user = cursor.fetchone()
    
    if user: 
        cursor.execute("UPDATE user SET email_verified=1 where email_key= '"+emailkey+"'")
        mysql.get_db().commit()
        flash('This email address has been verified, please login to continue.')
        return redirect(url_for('auth.login'))
    else:
        flash('There was an error while verifying your email address.')
        return redirect(url_for('auth.login'))
