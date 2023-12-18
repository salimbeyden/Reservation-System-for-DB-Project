from flask import Flask, render_template, redirect, url_for, session, flash, request
from flask_login import login_user, current_user

from MyFlaskApp import app
from MyFlaskApp import mysql

from imports.forms import *
from imports.utils import *
from imports.models import User  # Import User from models.py

# to view a personalized page with peralized http extension
@app.route('/about/<username>')
def about_person_page(username):
    return f'<h1>This is the about the page of {username}</h1>'

# for home page
@app.route('/') # home page as default
@app.route('/home') # hume page at /home, also
def home_page():
    return render_template('index.html')

@app.route('/dash')
def dash_page():
    return render_template('dashboard.html')

# for login page at /login
@app.route('/login', methods=['GET', 'POST'])
def login_page():
    login_form = LoginForm()
    register_form = RegisterForm()
    print("Hello, console!")
    ### FOR LOGIN ###
    if login_form.validate_on_submit():
        email = login_form.email_address.data
        password = login_form.password.data

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM user WHERE email = % s AND password_hash = % s', (email, password, ))
        user = cursor.fetchone()
        cursor.close()
        if user:
            user_obj = User(user_id=user[0], name=user[1], surname=user[2], email=user[3], tel_no=user[4], faculty_name=user[5], department=user[6], 
                 birth_date=user[7], password=user[8], gender=user[9], f_team_id=user[10], v_team_id=user[11], b_team_id=user[12], t_team_id=user[13], p_team_id=user[14])  # Create a user object
            login_user(user_obj)  # Log in the user
            return redirect(url_for('dash_page'))
        else:
            flash("Login failed. Please check your email and password")
    
    ### FOR REGISTRATION ###
    elif register_form.validate_on_submit():
        print()

    return render_template('login.html',login_form=login_form, register_form=register_form)

@app.route('/matchhist/', methods = ["GET","POST"])
@app.route('/matchhist/<selected_sport>', methods = ["GET","POST"])
def match_hist(selected_sport = "*"):
    cursor = mysql.connection.cursor()

    cursor.execute('SELECT sport_id, sport_type FROM sport where is_competitive = 1')
    sports = cursor.fetchall()

    if request.method == 'POST':
        selected_sport = request.form['sports']

    match_hist_form = MatchHistFrom(sports, selected_sport)


    if selected_sport == "*":
        query = """select t1.name, t2.name, hist.score_1, hist.score_2, campus.name, facility.name, hist.date
                   from team_match_history as hist
                   join team as t1 on t1.team_id = hist.team_1
                   join team as t2 on t2.team_id = hist.team_2
                   join campus on campus.campus_id = hist.campus_id
                   join facility on facility.facility_id = hist.facility_id;"""
        is_ind = 0
        
    else:
        cursor.execute('SELECT is_ind FROM sport where sport_id = {}'.format(selected_sport))
        is_ind = cursor.fetchall()[0][0]

        if is_ind == 0:
            query = """select t1.name, t2.name, hist.score_1, hist.score_2, campus.name, facility.name, hist.date 
                    from team_match_history as hist
                    join team as t1 on t1.team_id = hist.team_1
                    join team as t2 on t2.team_id = hist.team_2
                    join campus on campus.campus_id = hist.campus_id
                    join facility on facility.facility_id = hist.facility_id
                    where hist.sport_id = {};""".format(selected_sport)
            
        else:
            query = """select u1.name, u1.surname, u2.name, u2.surname, hist.score_1, hist.score_2, campus.name, facility.name, hist.date
                       from individuals_match_history as hist
                       join user as u1 on u1.school_id = hist.user_1
                       join user as u2 on u2.school_id = hist.user_2
                       join campus on campus.campus_id = hist.campus_id
                       join facility on facility.facility_id = hist.facility_id
                       where sport_id = {};""".format(selected_sport)
            

    cursor.execute(query)
    table_data = cursor.fetchall()

    table_data, title = manipulate_hist_data(table_data, is_ind)
    
    cursor.close()
    return render_template('match_hist.html', match_hist_form=match_hist_form, selected_sport=selected_sport, table_data=table_data, title=title)

@app.route('/rank/', methods = ["GET","POST"])
@app.route('/rank/<selected_sport><order_by>', methods = ["GET","POST"])
def rank_page(selected_sport = "*", order_by = "score"):
    print(selected_sport, order_by)
    cursor = mysql.connection.cursor()

    cursor.execute('SELECT sport_id, sport_type FROM sport where is_ind = 0')
    sports = cursor.fetchall()

    if request.method == 'POST':
        print(request.form.keys())
        selected_sport = request.form['sports']
        order_by = request.form['order']
    rank_form = RankFrom(sports, selected_sport, order_by)


    if selected_sport == "*":
        query = """select team.name, u.name, u.surname, s.sport_type, team.team_score as score, count(*) as count, team.team_score/count(*) as avrg, team.foundation_date from team
                   join user as u on u.school_id = team.captain_id
                   join team_match_history as hist1 on hist1.team_1 = team.team_id or hist1.team_2 = team.team_id
                   join sport as s on s.sport_id = team.sport_id
                   group by s.sport_type, team.name, u.name, u.surname, team.team_score, team.foundation_date
                   order by {} desc;
                """.format(order_by)
        
    else:
        query = """select team.name, u.name, u.surname, s.sport_type, team.team_score as score, count(*) as count, team.team_score/count(*) as avrg, team.foundation_date from team
                   join user as u on u.school_id = team.captain_id
                   join team_match_history as hist1 on hist1.team_1 = team.team_id or hist1.team_2 = team.team_id
                   join sport as s on s.sport_id = team.sport_id
                   where s.sport_id = {}
                   group by s.sport_type, team.name, u.name, u.surname, team.team_score, team.foundation_date
                   order by {} desc;
                """.format(selected_sport, order_by)
    cursor.execute(query)
    table_data = cursor.fetchall()
    table_data, title = manipulate_rank_data(table_data)

    cursor.close()
    return render_template('ranking.html', selected_sport=selected_sport, rank_form=rank_form, table_data=table_data, title=title)

#RESERVATION PAGE(processing...)
@app.route('/reservation/', methods = ["GET","POST"])
@app.route('/reservation/<selected_sport><selected_campus><selected_area><order_by>', methods = ["GET","POST"])
def reservation_page(selected_sport="*", selected_campus="*", selected_area="*", order_by="campus"):
    return render_template("reservation.html", selected_sport=selected_sport, selected_campus=selected_campus, selected_area=selected_area, order_by=order_by)

# @app.route('/profile_page')
# def profile_page():
#     return render_template('profile.html')
