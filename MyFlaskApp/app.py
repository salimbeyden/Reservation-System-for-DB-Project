from flask import Flask, render_template, redirect, url_for, session, flash
from MyFlaskApp.forms import LoginForm
from MyFlaskApp import mysql

app = Flask(__name__)

# to view a personalized page with personalized http extension
@app.route('/about/<username>')
def about_person_page(username):
    return f'<h1>This is the about the page of {username}</h1>'

# for home page
@app.route('/') # home page as default
@app.route('/home') # hume page at /home, also
def home_page():
    return render_template('index.html')
 
# for login page at /login
@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    print("Hello, console!")
    if form.validate_on_submit():
        email = form.email_address.data
        password = form.password.data

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM user WHERE email = % s AND password_hash = % s', (email, password, ))
        user = cursor.fetchone()
        cursor.close()
        if user:
            session['user_id'] = user[0]
            return redirect(url_for('home_page'))
        else:
            msg = "Login failed. Please check your email and password"
            return redirect(url_for('home_page'))

    return render_template('login2.html',msg=msg)
