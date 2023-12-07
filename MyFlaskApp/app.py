from flask import Flask, render_template, redirect, url_for, session, flash
from MyFlaskApp.forms import LoginForm
from MyFlaskApp import mysql
from MyFlaskApp import app
from MyFlaskApp.models import User  # Import User from models.py
from flask_login import login_user

# to view a personalized page with peralized http extension
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
            user_obj = User(id=user[0], name=user[1], surname=user[2], email=user[3], tel_no=user[4], faculty_name=user[5], department=user[6], 
                 birth_date=user[7], password=user[8], gender=user[9], f_team_id=user[10], v_team_id=user[11], b_team_id=user[12], t_team_id=user[13], p_team_id=user[14])  # Create a user object
            login_user(user_obj)  # Log in the user
            return redirect(url_for('home_page'))
        else:
            msg = "Login failed. Please check your email and password"
            return redirect(url_for('home_page'))

    return render_template('login2.html',form=form)
