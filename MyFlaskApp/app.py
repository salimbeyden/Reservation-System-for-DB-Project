from flask import Flask, render_template, redirect, url_for, session, flash, request, jsonify, session
from flask_login import login_user, current_user, logout_user

from MyFlaskApp import app
from MyFlaskApp import mysql, csrf

from imports.forms import *
from imports.utils import *
from imports.models import User  # Import User from models.py
import random

# to be able to reachable from every file
@app.context_processor
def inject_campus_dropdown():
    return dict(dropdown_campus_items=manipulate_campus_dropdown())

# to be able to reachable from every file
@app.context_processor
def inject_sport_dropdown():
    return dict(dropdown_sport_items=manipulate_sports_dropdown())

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

    login_form = LoginForm()
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
            return redirect(url_for('home_page'))
        else:
            flash("Login failed. Please check your email and password")

    return render_template('login.html',login_form=login_form)

# for register page at /register
@app.route('/register', methods=['GET', 'POST'])
def register_page():
    register_form = RegisterForm()
    ### FOR REGISTRATION ###
    if register_form.validate_on_submit():
        try:
            id = register_form.student_number.data
            name = register_form.name.data
            surname = register_form.surname.data
            email = register_form.email_address.data
            tel_no = register_form.phone_number.data
            faculty_name = register_form.faculty.data
            department = register_form.department.data 
            birth_date = register_form.birth_date.data
            password = register_form.password.data
            gender = register_form.gender.data
            
            cursor = mysql.connection.cursor()
            query= """INSERT INTO user (school_id, name, surname, email, tel_no, faculty_name, department, birth_date, password_hash, gender) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            values = (id, name, surname, email, tel_no, faculty_name, department, birth_date, password, gender)
            cursor.execute(query, values)
            mysql.connection.commit()
            cursor.close()
            # flash("Registration successful, please login.")
            return redirect(url_for('login_page'))

        except Exception as e:
            print("An error occurred: " + str(e))

    return render_template('register.html', register_form=register_form)

@app.route('/matchhist/', methods = ["GET","POST"])
@app.route('/matchhist/<selected_user>', methods = ["GET","POST"])
def match_hist(selected_user, selected_sport = "*", selected_team_sport = "*"):
    cursor = mysql.connection.cursor()

    if request.method == 'POST':
        selected_sport = request.form['sports']
    cursor.execute('SELECT sport_id, sport_type FROM sport where is_competitive = 1 and is_ind = 1;')
    sports = cursor.fetchall()
    

    match_hist_form = MatchHistFrom(sports, selected_sport)

    if selected_sport == "*":
        query = """select u1.name, u1.surname, u1.school_id, score_1, score_2, u2.name, u2.surname, u2.school_id, campus.name, campus.campus_id, f.name, f.facility_id, sport.sport_type, sport.sport_id, date 
                   from individuals_match_history as hist
                   join user as u1 on hist.user_1 = u1.school_id
                   join user as u2 on hist.user_2 = u2.school_id
                   join campus on campus.campus_id = hist.campus_id
                   join facility as f on f.facility_id = hist.facility_id
                   join sport on sport.sport_id = hist.sport_id
                   where u1.school_id = {user} or u2.school_id = {user};""".format(user = selected_user)
    else:
        query = """select u1.name, u1.surname, u1.school_id, score_1, score_2, u2.name, u2.surname, u2.school_id, campus.name, campus.campus_id, f.name, f.facility_id, sport.sport_type, sport.sport_id, date 
                   from individuals_match_history as hist
                   join user as u1 on hist.user_1 = u1.school_id
                   join user as u2 on hist.user_2 = u2.school_id
                   join campus on campus.campus_id = hist.campus_id
                   join facility as f on f.facility_id = hist.facility_id
                   join sport on sport.sport_id = hist.sport_id
                   where (u1.school_id = {user} or u2.school_id = {user}) and sport.sport_id = {sport};""".format(user=selected_user, sport=selected_sport)
        
    cursor.execute(query)
    data = cursor.fetchall()
    data, title = manipulate_hist_data(data, "ind")

    cursor.close()
    return render_template('match_hist.html', user = selected_user, form=match_hist_form, data=data, title=title)

@app.route('/rank/', methods = ["GET","POST"])
@app.route('/rank/<selected_sport><order_by>', methods = ["GET","POST"])
def rank_page(selected_sport = "*", order_by = "score"):
    if request.method == 'POST':
        selected_sport = request.form['sports']
        order_by = request.form['order']


    cursor = mysql.connection.cursor()

    cursor.execute('SELECT sport_id, sport_type FROM sport where is_ind = 0')
    sports = cursor.fetchall()

    rank_form = RankFrom(sports, selected_sport, order_by)

    if selected_sport == "*":
        query = """select  team.name, team.team_id, u.name, u.surname, u.school_id, s.sport_type, team.sport_id, team.team_score as score, count(*) as count, team.team_score/count(*) as avrg, team.foundation_date from team
                   join user as u on u.school_id = team.captain_id
                   join team_match_history as hist1 on hist1.team_1 = team.team_id or hist1.team_2 = team.team_id
                   join sport as s on s.sport_id = team.sport_id
                   group by team.name, team.team_id, u.name, u.surname, u.school_id, s.sport_type, team.sport_id, team.team_score, team.foundation_date
                   order by {} desc;
                """.format(order_by)
        
    else:
        query = """select  team.name, team.team_id, u.name, u.surname, u.school_id, s.sport_type, team.sport_id, team.team_score as score, count(*) as count, team.team_score/count(*) as avrg, team.foundation_date from team
                   join user as u on u.school_id = team.captain_id
                   join team_match_history as hist1 on hist1.team_1 = team.team_id or hist1.team_2 = team.team_id
                   join sport as s on s.sport_id = team.sport_id
                   where s.sport_id = {}
                   group by team.name, team.team_id, u.name, u.surname, u.school_id, s.sport_type, team.sport_id, team.team_score, team.foundation_date
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

    if request.method == 'POST':
        selected_sport = request.form['sports']
        selected_campus = request.form['campuses']
        selected_area = request.form['area']

        # Store the selected date in the session
        session['selected_date'] = request.form['set_time']

    cursor = mysql.connection.cursor()

    cursor.execute('SELECT sport_id, sport_type FROM sport')
    sports = cursor.fetchall()

    if selected_sport == "*":
        cursor.execute('SELECT campus_id, name FROM campus')
        campuses = cursor.fetchall()
    else:
        query = """SELECT DISTINCT c.campus_id, c.name FROM facility as f
                    join facility_for_sport as fps on f.facility_id = fps.facility_id
                    join campus as c on c.campus_id = f.campus_id
                    join sport as s on s.sport_id = fps.sport_id
                    where fps.current < fps.capacity and fps.sport_id = {}""".format(selected_sport)
        cursor.execute(query)
        campuses = cursor.fetchall()
    
    if selected_campus == "*":
        cursor.execute('SELECT facility_id, name FROM facility')
        area = cursor.fetchall()
    else:
        query = """SELECT DISTINCT f.facility_id, f.name FROM facility as f
                    join facility_for_sport as fps on f.facility_id = fps.facility_id
                    join campus as c on c.campus_id = f.campus_id
                    join sport as s on s.sport_id = fps.sport_id
                    where fps.current < fps.capacity and fps.sport_id = {} and f.facility_id = {}""".format(selected_sport, selected_campus)
        cursor.execute(query)
        area = cursor.fetchall()

    base_query = """SELECT DISTINCT c.name, f.name, s.sport_type, f.email, fps.current, fps.capacity FROM facility as f
                JOIN facility_for_sport as fps on f.facility_id = fps.facility_id
                JOIN campus as c on c.campus_id = f.campus_id
                JOIN sport as s on s.sport_id = fps.sport_id
                WHERE fps.current < fps.capacity"""

    #add necessary additions
    if selected_sport != "*":
        base_query += f" AND s.sport_id = {selected_sport}"

    if selected_campus != "*":
        base_query += f" AND c.campus_id = {selected_campus}"

    cursor.execute(base_query)
    data = cursor.fetchall()
    data, title = manipulate_reservation_data(data)

    reservation_form = ReservationForm(sports, campuses, area, selected_sport, selected_campus, selected_area)

    cursor.close()
    return render_template("reservation.html", selected_sport=selected_sport, selected_campus=selected_campus, selected_area=selected_area, order_by=order_by, reservation_form=reservation_form,
                           data=data, title=title)


@app.route('/reservation_result', methods=['POST'])
def reservation_result():
    campus = request.form.get('campus')
    saloon = request.form.get('saloon')
    sport = request.form.get('sport')
    mail = request.form.get('mail')
    current = request.form.get('current')
    capacity = request.form.get('capacity')
    
    #take reservation in that date
    selected_date = session.get('selected_date', None)
    
    data = [campus, saloon, sport, mail, current, capacity, selected_date]

    cursor = mysql.connection.cursor()

    query = """SELECT is_competitive,is_ind FROM sport WHERE sport_type = '{}'""".format(sport)
    cursor.execute(query)
    res_table = cursor.fetchall()
    print(res_table)

    #get sport id
    query = """SELECT sport_id FROM sport WHERE sport_type = '{}'""".format(sport)
    cursor.execute(query)
    sport_id = cursor.fetchall()[0][0]
    print(sport_id)

    #get campus id
    query = """SELECT campus_id FROM campus WHERE name = '{}'""".format(campus)
    cursor.execute(query)
    campus_id = cursor.fetchall()[0][0]

    #get saloon id
    query = """SELECT facility_id FROM facility WHERE name = '{}'""".format(saloon)
    cursor.execute(query)
    facility_id = cursor.fetchall()[0][0]

    #individual sports
    if(res_table[0][0] == 1 and res_table[0][1] == 0):
        #append reservation_team
        #decide the sport type of user

        #check if the user has a team
        has_team = False  #assume the user doesn't have a team by default

        if(current_user.f_team_id or current_user.v_team_id or current_user.b_team_id or current_user.t_team_id or current_user.p_team_id != None):
            has_team = True
        else:
            flash("You cannot make a reservation for a team sport because you don't have a team.")
            return redirect(url_for('reservation_page'))

        if(sport_id == 1):
            team_1 = current_user.f_team_id
        elif(sport_id == 2):
            team_1 = current_user.v_team_id
        elif(sport_id == 3):
            team_1 = current_user.b_team_id
        elif(sport_id == 5):
            team_1 = current_user.t_team_id
        elif(sport_id == 9):
            team_1 = current_user.p_team_id

        print(team_1)

        query = """SELECT team_id FROM team"""
        cursor.execute(query)
        team_ids = cursor.fetchall()
        team_2 = random.choice(team_ids)[0]

        query = """INSERT INTO reservation_team (sport_id, campus_id, facility_id, date, team_1, team_2)
                    VALUES (%s, %s, %s, %s, %s, %s)"""
        values = (sport_id, campus_id, facility_id, selected_date, team_1, team_2)


    elif(res_table[0][0] == 0 and res_table[0][1] == 1):
        #append individual reservation
        query = """INSERT INTO reservation_individual (sport_id, campus_id, facility_id, date, user)
                    VALUES (%s, %s, %s, %s, %s)"""
        values = (sport_id, campus_id, facility_id, selected_date, current_user.school_id)
        
    else:
        #append reservation individual_match
        query = """SELECT school_id FROM user"""
        cursor.execute(query)
        user_ids = cursor.fetchall()
        user_2 = random.choice(user_ids)[0]

        query = """INSERT INTO reservation_individual_match (sport_id, campus_id, facility_id, date, user_1, user_2)
                    VALUES (%s, %s, %s, %s, %s, %s)"""
        values = (sport_id, campus_id, facility_id, selected_date, current_user.school_id, user_2)
    cursor.execute(query, values)
    mysql.connection.commit()
        
    return render_template("success_res.html", data=data)


@app.route('/team_profile/<selected_team>', methods = ["GET","POST"])
@csrf.exempt
def team_profile(selected_team):
    cursor = mysql.connection.cursor()

    query = """select team.name, team.team_id, user.name, user.surname, user.school_id, sport.sport_type, sport.sport_id ,team.foundation_date, team.team_score, sport.capacity_max, count(*) from team
               join team_match_history as hist on team.team_id = hist.team_1 or team.team_id = hist.team_2
               join user on user.school_id = team.captain_id
               join sport on sport.sport_id = team.sport_id
               where team_id = {}
               group by team.name, team.team_id, user.name, user.surname, sport.sport_type, sport.sport_id ,team.foundation_date, team.team_score, sport.capacity_max;
            """.format(selected_team)
    
    cursor.execute(query)

    team_info = cursor.fetchall()

    team_info = manipulate_team_info(team_info)

    query = """select name, surname, school_id from user
               where team_id_football = {team} or 
               team_id_volleyball = {team} or 
               team_id_basketball = {team} or 
               team_id_tennis = {team} or
               team_id_pingpong = {team};
            """.format(team=selected_team)
    
    cursor.execute(query)

    players = [{"name": f"{row[0]} {row[1]}".title(), "school_id": row[2]} for row in cursor.fetchall()]
    
    query = """select team1.name, score_1, score_2, team2.name, hist.date from team_match_history as hist
               join team as team1 on team1.team_id = hist.team_1
               join team as team2 on team2.team_id = hist.team_2
               where team_1 = {team} or team_2 = {team};
            """.format(team = selected_team)

    cursor.execute(query)
    match_hist = [[row[0], f"{row[1]} - {row[2]}", row[3], row[4]] for row in cursor.fetchall()]

    
    no_teams = False
    if current_user.all_teams[team_info["sport_type"]]:
        no_teams = True

    query = """select  sport.capacity_max from team
                       join sport on sport.sport_id = team.sport_id
                       where team.team_id = {};""".format(team_info["team_id"])
            
    cursor.execute(query)
    max_player = cursor.fetchone()[0]
    
    if request.method == 'POST':
        print("Takimdan cikma-girme fonkisyonu calistirildi")
        if request.form.get('action') == 'leave_team':

            for player in players:
                if str(player["school_id"]) == current_user.school_id:
                    print("oyuncu silindi")
                    players.remove(player)

            base_query = "UPDATE user"
            
            match team_info["sport_id"]:
                case 1:
                    base_query += " SET team_id_football = NULL"
                case 2:
                    base_query += " SET team_id_volleyball = NULL"
                case 3:
                    base_query += " SET team_id_basketball = NULL"
                case 5:
                    base_query += " SET team_id_tennis = NULL"
                case 9:
                    base_query += " SET team_id_pingpong = NULL"

            base_query += " WHERE school_id = {};".format(current_user.school_id)
                
            cursor.execute(base_query)
            mysql.connection.commit()


            if len(players) == 0:
                query = "DELETE FROM team WHERE team_id = {});".format(team_info["team_id"])
                cursor.execute(query)
                mysql.connection.commit()

                return redirect(url_for("profile_page", selected_user = current_user.school_id))

            if str(team_info["captain_id"]) == current_user.school_id:
                print("kaptan çıktı")
                new_captain = players[0]["school_id"]
                print(new_captain, team_info["team_id"])
                query = "UPDATE team SET captain_id = {} WHERE team_id = {}".format(new_captain, team_info["team_id"])

                cursor.execute(query)
                mysql.connection.commit()

            return redirect(url_for("team_profile", selected_team = team_info["team_id"]))
        
        if request.form.get('action') == 'join_team':

            query = """UPDATE user
                    SET team_id_football = NULL
                    WHERE school_id = {};
                    """.format(current_user.school_id)
                
            cursor.execute(query)
            mysql.connection.commit()

            base_query = "UPDATE user"
            
            match team_info["sport_id"]:
                case 1:
                    base_query += " SET team_id_football = {}".format(team_info["team_id"])
                case 2:
                    base_query += " SET team_id_volleyball = {}".format(team_info["team_id"])
                case 3:
                    base_query += " SET team_id_basketball = {}".format(team_info["team_id"])
                case 5:
                    base_query += " SET team_id_tennis = {}".format(team_info["team_id"])
                case 9:
                    base_query += " SET team_id_pingpong = {}".format(team_info["team_id"])

            base_query += " WHERE school_id = {};".format(current_user.school_id)

            cursor.execute(base_query)
            mysql.connection.commit()

            return redirect(url_for("team_profile", selected_team = team_info["team_id"]))

    return render_template('team_profile.html', team=team_info ,players=players, match_hist=match_hist, no_teams=no_teams)


@app.route('/profile/<selected_user>', methods = ["GET"])
def profile_page(selected_user):
    cursor = mysql.connection.cursor()

    query = """select u.name, u.surname, u.school_id, u.email, u.tel_no, u.faculty_name, u.department, u.birth_date, u.gender from user u
              where u.school_id = {user};""".format(user = selected_user)
    
    cursor.execute(query)

    user = cursor.fetchall()

    user = manipulate_profile_user(user)
    
    query = """SELECT team.name, team.team_id, team.team_score, sport.sport_type, team.sport_id, team.captain_id  FROM user 
               join team on team.team_id = user.team_id_football
               join sport on sport.sport_id = team.sport_id
               WHERE school_id = {user} AND team_id_football IS NOT NULL
               UNION
               SELECT team.name, team.team_id, team.team_score, sport.sport_type, team.sport_id, team.captain_id  FROM user 
               join team on team.team_id = user.team_id_volleyball
               join sport on sport.sport_id = team.sport_id
               WHERE school_id = {user} AND team_id_volleyball IS NOT NULL
               UNION
               SELECT team.name, team.team_id, team.team_score, sport.sport_type, team.sport_id, team.captain_id FROM user 
               join team on team.team_id = user.team_id_basketball
               join sport on sport.sport_id = team.sport_id
               WHERE school_id = {user} AND team_id_basketball IS NOT NULL
               UNION
               SELECT team.name, team.team_id, team.team_score, sport.sport_type, team.sport_id, team.captain_id  FROM user 
               join team on team.team_id = user.team_id_tennis
               join sport on sport.sport_id = team.sport_id
               WHERE school_id = {user} AND team_id_tennis IS NOT NULL
               UNION
               SELECT team.name, team.team_id, team.team_score, sport.sport_type, team.sport_id, team.captain_id  FROM user 
               join team on team.team_id = user.team_id_pingpong
               join sport on sport.sport_id = team.sport_id
               WHERE school_id = {user} AND team_id_pingpong IS NOT NULL;""".format(user = selected_user)

    cursor.execute(query)

    team_table = cursor.fetchall()

    team_table = manipulate_profile_teams(team_table, user["school_id"])

    return render_template('profile.html', team_table=team_table, user=user)

@app.route("/update_profile", methods = ["GET", "POST"])
def update_profile():

    update_form = UpdateProfile()

    update_form.email_address.render_kw = {"placeholder": current_user.email, "value": current_user.email}
    update_form.tel_no.render_kw = {"placeholder": current_user.tel_no, "value": current_user.tel_no}
    update_form.password.render_kw = {"placeholder": "********", "value": current_user.password}

    if request.method == "POST":
        cursor = mysql.connection.cursor()

        new_mail = request.form["email_address"] if request.form["email_address"] != "" else current_user.email
        new_tel_no = request.form["tel_no"] if request.form["tel_no"] != "" else current_user.tel_no
        new_passw = request.form["password"] if request.form["password"] != "" else current_user.password


        query = """UPDATE `reservations`.`user` 
                   SET `email` = '{mail}', 
                       `tel_no` = '{tel}', 
                       `password_hash` = '{passw}' 
                   WHERE (`school_id` = '{user}');""".format(mail=new_mail, tel=new_tel_no, passw=new_passw, user=current_user.school_id)
        try:
            cursor.execute(query)
            mysql.connection.commit()
            print("Oldu :)")
        except:
            print("Olmadi!!")
        
        cursor.close()
        return redirect(url_for('profile_page', selected_user=current_user.school_id))


    return render_template("update_profile.html", form=update_form)

# when log out
@app.route('/logout')
def log_out():
    logout_user()
    session.clear()  # Clear the session
    return redirect(url_for('home_page'))

@app.route('/campus/<selected_campus>')
def campus_page(selected_campus):
    # Query for campus_id
    campus_query = "SELECT name, image_id FROM campus WHERE campus_id = %s"
    cursor = mysql.connection.cursor()
    cursor.execute(campus_query, (selected_campus,))
    campus = cursor.fetchone()
    campus_id = selected_campus
    campus_name = campus[0]
    campus_image = campus[1]

    # Query for facilities in this campus
    facilities_query = "SELECT * FROM facility WHERE campus_id = %s"
    cursor.execute(facilities_query, (campus_id,))
    facilities = cursor.fetchall()
    # For each facility, find associated sports
    facilities_sports = {}
    for facility in facilities:
        facility = manipulate_facility_info(facility)
        facility_id = facility["facility_id"]
        sports_query = """
        SELECT sport.sport_id, sport.sport_type FROM sport
        JOIN facility_for_sport ON sport.sport_id = facility_for_sport.sport_id
        WHERE facility_for_sport.facility_id = %s
        """
        cursor.execute(sports_query, (facility_id,))
        sports = cursor.fetchall()
        facilities_sports[facility["facility_id"]] = [facility, [sport for sport in sports]]
    # Render template with facilities and associated sports
    return render_template('campus.html', facilities_sports=facilities_sports, campus_id=campus_id, campus_name=campus_name, campus_image=campus_image)

# sports
@app.route('/sports/<selected_sport>')
def sports_page(selected_sport):
    # Query for campus_id
    sport_query = "SELECT sport_type FROM sport WHERE sport_id = %s"
    cursor = mysql.connection.cursor()
    cursor.execute(sport_query, (selected_sport,))
    sport_name = cursor.fetchone()[0]
    sport_id = selected_sport
    
    # Query for facilities which has the sport field
    facilities_query = """
    SELECT facility.* 
    FROM facility 
    JOIN facility_for_sport 
    ON facility.facility_id = facility_for_sport.facility_id 
    WHERE facility_for_sport.sport_id = %s
    """
    cursor.execute(facilities_query, (sport_id,))
    facilities = cursor.fetchall()
    # For each facility, find associated sports
    campus_facilities_dict = {}
    for facility in facilities:
        facility_info = manipulate_facility_info(facility)
        
        # Query for campus name
        campus_query = "SELECT * FROM campus WHERE campus_id = %s"
        cursor.execute(campus_query, (facility_info["campus_id"],))
        campus = cursor.fetchone()
        campus_info = manipulate_campus_info(campus)
        
        # Add to dictionary
        
        if campus_info["name"] not in campus_facilities_dict:
            campus_facilities_dict[campus_info["name"]] = [campus_info,[]]
        campus_facilities_dict[campus_info["name"]][1].append(facility_info)
    # Render template with facilities and associated sports
    return render_template('sports.html', campus_facilities_dict=campus_facilities_dict, sport_id=sport_id, sport_name=sport_name)
