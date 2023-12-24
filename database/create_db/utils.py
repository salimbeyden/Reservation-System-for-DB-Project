import numpy as np
import random
from faker import Faker
from datetime import date as d, timedelta, datetime
import yaml

def read_config():
    # config file keeps the parameters like host, user, password and sql command paths
    # you can change them if needed
    print("here")
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
    return config

def create_db(cursor, config):
    
    db_script = config["sqldb_path"] # path to sql commands that creates 'reservation' database
    db = config["database"]


    print("Database created successfully!")
    with open(db_script, "r") as tables_file: # reads the .sql scripts to create necessary tables
        tables_commands = tables_file.read().split(";")

    cursor.execute(tables_commands[0]) 

    for table_command in tables_commands[1:]: # block to create each tables
        if table_command.strip():
            cursor.execute(table_command)
    print("Tables created successfully!")

    # print tables to the screen
    cursor.execute(f"use {db}")
    print("Tables:")
    cursor.execute("show tables")
    for table in cursor:
        print(f"- {table[0]}")

    print()

def stable_tables(cursor, stables_path):

    # .sql dosyasından sorguyu oku
    with open(stables_path, "r") as tables_file:
        sql_insert = tables_file.read().split(";")

    # Sorguyu çalıştır
    for table_command in sql_insert: # block to create each tables
        if table_command.strip():
            cursor.execute(table_command)

    print("Values inserted into 'campus' table successfully!")
    print("Values inserted into 'facility' table successfully!")
    print("Values inserted into 'facility_for_sport' table successfully!")
    print("Values inserted into 'sport' table successfully!")

def generate_user_table(cursor, faculties, majors, user_count):
    school_ids = np.random.randint(100000000, 999999999, size = user_count)

    fake = Faker()
    
    for user in range(user_count):

        id = school_ids[user]
        first_name, last_name = fake.name().split(" ")[:2]
        mail = last_name.lower() + first_name[0].lower() + str(np.random.choice([17,18,19,20,21,22,23])) + "@itu.edu.tr"
        phone_number = "5" + ''.join(random.choices('123456789', k=9))
        phone_number = f'+90 ({phone_number[:3]}) {phone_number[3:6]} {phone_number[6:]}'
        faculty = np.random.choice(faculties)
        major = np.random.choice(majors[faculty])
        birth_date = fake.date_of_birth(minimum_age=18, maximum_age=30).isoformat()
        password = fake.password()
        gender = np.random.choice(["m", "f"])


        
        insert_query = f'''
            INSERT INTO user (
                school_id, name, surname, email, tel_no, faculty_name, department, birth_date, password_hash, gender
            ) VALUES ({id}, "{first_name}", "{last_name}", "{mail}", "{phone_number}", "{faculty}", "{major}", "{birth_date}", "{password}", "{gender}")
        '''
        cursor.execute(insert_query)

    print("Values inserted into 'user' table successfully!")

def generate_team_table(cursor, team_count):
    fake = Faker()

    query = "select sport_id, capacity_min, capacity_max, sport_type, is_ind from sport where is_ind = 0;"
    cursor.execute(query)
    result = cursor.fetchall()

    sports = [[row[0], row[1], row[2], row[3].lower().split(" ")[0], row[4]] for row in result]

    team_id = 0
    for sport in sports:
        query = "select school_id from user where team_id_{} is null;".format(sport[3])
        cursor.execute(query)
        result = cursor.fetchall()

        school_ids = [row[0] for row in result]
        max_user_count = int(sport[2]) * team_count

        users = np.random.choice(school_ids, max_user_count, replace=False)
        curr_user = 0
        for i in range(team_count):
            team_id+=1

            player_in_team = np.random.randint(int(sport[1]), int(sport[2])+1)

            team_name = fake.word() + " " + fake.word()
            foundation_date = fake.date_of_birth(minimum_age=0, maximum_age=5).isoformat()
            password = fake.password()

            query = f"""insert into team (name, captain_id, team_score, foundation_date, password_hash, sport_id) 
            values ('{team_name}', {users[curr_user]}, 0, '{foundation_date}', '{password}', {sport[0]})"""

            cursor.execute(query)
            for j in range(curr_user, curr_user + player_in_team):
                query = "UPDATE user SET team_id_{} = {} WHERE school_id = {};".format(sport[3], team_id, users[j])
                cursor.execute(query)

            curr_user += player_in_team

    print("Values inserted into 'team' table successfully!")

def random_date_in_next_month():
    """
    Returns a random date within the next one month from today.
    """
    today = datetime.now()
    random_days = np.random.randint(0, 30)

    return today + timedelta(days=random_days)

def generate_ind_reservation(cursor, reservation_count):


    #get campus_id's from campus table
    query_campus = "select campus_id from campus"
    cursor.execute(query_campus)
    result_campus = cursor.fetchall()
    campus_ids = [row[0] for row in result_campus]

    #get user_id's from user table
    query_user = "select school_id from user"
    cursor.execute(query_user)
    result_user = cursor.fetchall()
    user_ids = [row[0] for row in result_user]


    #choose randomly id's
    users = np.random.choice(user_ids, reservation_count, replace=True)
    
    reservation_id = 0
    idx = 0     
    for i in range(reservation_count):
        reservation_id += 1

        campus = np.random.choice(campus_ids)

        #get facility_id's from facility table
        query_facility = f"select facility_id from facility where campus_id = {campus}"
        cursor.execute(query_facility)
        result_facility = cursor.fetchall()
        facility_ids = [row[0] for row in result_facility]

        facility = np.random.choice(facility_ids)

        #get sport_id's from sport table
        query_sport = f"select sport_id from facility_for_sport where facility_id = {facility}"
        cursor.execute(query_sport)
        result_sport = cursor.fetchall()
        sport_ids = [row[0] for row in result_sport]

        #choose the sport
        sport_id = np.random.choice(sport_ids)

        #generate random date
        date = random_date_in_next_month()

        query = f"""insert into reservation_individual (reservation_id, sport_id, campus_id, facility_id, date, user)
        values ({reservation_id}, {sport_id}, {campus}, {facility}, '{date}', {users[idx]})"""

        cursor.execute(query)

        #increase index one
        idx += 1

    print("Values inserted into 'reservation_individual' table successfully!")

def generate_ind_match_reservation(cursor, reservation_count):
    
    query = "select date, user_1, user_2, sport_id, campus_id, facility_id from individuals_match_history"
    cursor.execute(query)
    results = cursor.fetchall()
    
    reservation_id = 0
    for result in results:
        reservation_id += 1
        
        date, user_1, user_2, sport_id, campus_id, facility_id = result

        query = f"""insert into reservation_individual_match (reservation_id, sport_id, campus_id, facility_id, date, user_1, user_2)
        values ({reservation_id}, {sport_id}, {campus_id}, {facility_id}, '{date}', {user_1}, {user_2})"""

        cursor.execute(query)
    
    print("Values inserted into 'reservation_individual_match' table successfully!")

def generate_team_reservation(cursor, reservation_count):

    query = "select date, team_1, team_2, sport_id, campus_id, facility_id from team_match_history"
    cursor.execute(query)
    results = cursor.fetchall()

    reservation_id = 0
    for result in results:
        reservation_id += 1
        
        date, team_1, team_2, sport_id, campus_id, facility_id = result

        query = f"""insert into reservation_team (reservation_id, sport_id, campus_id, facility_id, date, team_1, team_2)
        values ({reservation_id}, {sport_id}, {campus_id}, {facility_id}, '{date}', {team_1}, {team_2})"""

        cursor.execute(query)


    print("Values inserted into 'reservation_team' table successfully!")

def random_score(sport_type):
    """
        returns logical score for given sport and point that winner will get
    """
    match sport_type.split(" ")[0]:
        case "Football":
            return abs(round(np.random.normal(1.5, 1))), abs(round(np.random.normal(1.5, 1))), 3
        case "Basketball":
            return abs(round(np.random.normal(50, 7))), abs(round(np.random.normal(50, 7))), 2
        case "Volleyball":
            score1 = np.random.randint(0,3)
            return score1, 3 - score1, 3
        case "Tennis":
            score1 = np.random.randint(0,3)
            return score1, 3 - score1, 1
        case "PingPong":
            score1 = np.random.randint(0,3)
            return score1, 3 - score1, 1
        
def random_date(foundation_date):
    """
        retrurns random date between today and given date
    """
    time_diff = d.today() - foundation_date
    return foundation_date + timedelta(np.random.randint(0, time_diff.days))

def generate_team_match_history(cursor, hist_count):

    query = """select sport_id, sport_type, is_ind from sport
                where is_competitive = 1 and is_ind = 0;"""
    cursor.execute(query)

    sport_ids = cursor.fetchall()

    for sport in sport_ids:
        query = f"""select team_id, foundation_date from team 
                    where sport_id = {sport[0]};"""
        cursor.execute(query)

        team_ids = np.array(cursor.fetchall())
        
        num_of_teams = len(team_ids)
        
        query = f"""select facility_id from facility_for_sport
                        where sport_id = {sport[0]};"""
        cursor.execute(query)

        facilities = [i[0] for i in cursor.fetchall()]

        for i in range(hist_count):
            team1 ,team2 = team_ids[np.random.choice(num_of_teams, 2, replace=False)]
            score1, score2, point = random_score(sport[1])
            facility_id = np.random.choice(facilities) # facility_for_sporta göre
            
            query = f"""select campus_id from facility
                        where facility_id = {facility_id};"""
            cursor.execute(query)
            campus_id = cursor.fetchall()[0][0]

            date = random_date(max(team1[1], team2[1]))

            query = f"""insert into team_match_history (date, team_1, team_2, score_1, score_2, campus_id, facility_id, sport_id)
                        values ('{date}', {team1[0]}, {team2[0]}, {score1}, {score2}, {campus_id}, {facility_id}, {sport[0]})"""
            cursor.execute(query)

            query = """update team set team_score = team_score + {}
                     where team_id = {};"""
            
            if score1 > score2:
                cursor.execute(query.format(point, team1[0]))
            elif score2 > score1:
                cursor.execute(query.format(point, team2[0]))
            else:
                cursor.execute(query.format(1, team1[0]))
                cursor.execute(query.format(1, team2[0]))


    print("Values inserted into 'team_match_history' table successfully!")



def generate_individuals_match_history(cursor, hist_count):

    query = """select sport_id, sport_type, is_ind from sport
                where is_competitive = 1 and is_ind = 1;"""
    cursor.execute(query)

    sport_ids = cursor.fetchall()
    for sport in sport_ids:
        query = f"""select school_id from user;"""
        cursor.execute(query)

        user_ids = np.array(cursor.fetchall())
        
        num_of_users = len(user_ids)
        
        query = f"""select facility_id from facility_for_sport
                        where sport_id = {sport[0]};"""
        cursor.execute(query)

        facilities = [i[0] for i in cursor.fetchall()]

        for i in range(hist_count):
            user1 ,user2 = user_ids[np.random.choice(num_of_users, 2, replace=False)]
            score1, score2, point = random_score(sport[1])
            facility_id = np.random.choice(facilities) # facility_for_sporta göre
            
            query = f"""select campus_id from facility
                        where facility_id = {facility_id};"""
            cursor.execute(query)
            campus_id = cursor.fetchall()[0][0]

            date = d.today() - timedelta(np.random.randint(0,730)) # in 2 years

            query = f"""insert into individuals_match_history (date, user_1, user_2, score_1, score_2, campus_id, facility_id, sport_id)
                        values ('{date}', {user1[0]}, {user2[0]}, {score1}, {score2}, {campus_id}, {facility_id}, {sport[0]});"""
            cursor.execute(query)

    print("Values inserted into 'individuals_match_history' table successfully!")

