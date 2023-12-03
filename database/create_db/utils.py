import numpy as np
import random
from faker import Faker
import yaml


def read_config():
    # config file keeps the parameters like host, user, password and sql command paths
    # you can change them if needed
    with open("C:\\Users\\90543\\Desktop\\ITU\\ITU Fall 2024\\BLG317E-Database Systems\\Project\\DatabaseSystems_Project\\config.yaml", "r") as f:
        config = yaml.safe_load(f)
    return config


def create_db(cursor, config):
    
    db_script = config["sqldb_path"] # path to sql commands that creates 'reservation' database
    table_script = config["sqltables_path"] # path to sql commands that creates tables for our database


    with open(db_script, "r") as db_file: # reads .sql scripts
        db_command = db_file.read().split(";")

    cursor.execute(db_command[0]) 

    print("Database created successfully!")
    with open(table_script, "r") as tables_file: # reads the .sql scripts to create necessary tables
        tables_commands = tables_file.read().split(";")

    for table_command in tables_commands: # block to create each tables
        if table_command.strip():
            cursor.execute(table_command)
    print("Tables created successfully!")

    # print tables to the screen
    cursor.execute("USE RESERVATIONS")
    print("Tables:")
    cursor.execute("SHOW TABLES")
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

    query = "select sport_id, capacity_min, capacity_max, sport_type from sport where capacity_max > 1;"
    cursor.execute(query)
    result = cursor.fetchall()

    sports = [[row[0], row[1], row[2], row[3]] for row in result]

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

            query = f"""insert into team (team_id, name, captain_id, foundation_date, password_hash, sport_id) 
            values ({team_id}, '{team_name}', '{users[curr_user]}', '{foundation_date}', '{password}', '{sport[0]}')"""

            cursor.execute(query)
            for j in range(curr_user, curr_user + player_in_team):
                query = "UPDATE user SET team_id_{} = {} WHERE school_id = {};".format(sport[3], team_id, users[j])
                cursor.execute(query)

            curr_user += player_in_team

    print("Values inserted into 'team' table successfully!")


def generate_ind_reservation(cursor, reservation_count):

    #faker to create date
    fake = Faker()
    
    #get sport_id's from sport table
    query_sport = "select sport_id from sport"
    cursor.execute(query_sport)
    result_sport = cursor.fetchall()
    sport_ids = [row[0] for row in result_sport]

    #get campus_id's from campus table
    query_campus = "select campus_id from campus"
    cursor.execute(query_campus)
    result_campus = cursor.fetchall()
    campus_ids = [row[0] for row in result_campus]
    
    #get facility_id's from facility table
    query_facility = "select facility_id from facility"
    cursor.execute(query_facility)
    result_facility = cursor.fetchall()
    facility_ids = [row[0] for row in result_facility]

    #get user_id's from user table
    query_user = "select user_id from user"
    cursor.execute(query_user)
    result_user = cursor.fetchall()
    user_ids = [row[0] for row in result_user]


    #choose randomly id's
    sports = np.random.choice(sport_ids, reservation_count, replace=True)
    campuses = np.random.choice(campus_ids, reservation_count, replace=True)
    facilities = np.random.choice(facility_ids, reservation_count, replace=True)
    users = np.random.choice(user_ids, reservation_count, replace=True)
    
    reservation_id = 0
    idx = 0
    for i in range(reservation_count):
        reservation_id += 1
        
        #generate random date
        date = fake.date()

        query = f"""insert into reservation_individual (reservation_id, sport_id, campus_id, facility_id, date, user)
        values ({reservation_id}, {sports[idx]}, {campuses[idx]}, {facilities[idx]}, {date}, {users[idx]})"""

        #increase index one
        idx += 1

    print("Values inserted into 'reservation_individual' table successfully!")

def generate_ind_match_reservation(cursor, reservation_count):

    #faker to create date
    fake = Faker()
    
    #get sport_id's from sport table
    query_sport = "select sport_id from sport"
    cursor.execute(query_sport)
    result_sport = cursor.fetchall()
    sport_ids = [row[0] for row in result_sport]

    #get campus_id's from campus table
    query_campus = "select campus_id from campus"
    cursor.execute(query_campus)
    result_campus = cursor.fetchall()
    campus_ids = [row[0] for row in result_campus]
    
    #get facility_id's from facility table
    query_facility = "select facility_id from facility"
    cursor.execute(query_facility)
    result_facility = cursor.fetchall()
    facility_ids = [row[0] for row in result_facility]

    #get user_id's from user table
    query_user = "select user_id from user"
    cursor.execute(query_user)
    result_user = cursor.fetchall()
    user_ids = [row[0] for row in result_user]

    #choose randomly id's
    sports = np.random.choice(sport_ids, reservation_count, replace=True)
    campuses = np.random.choice(campus_ids, reservation_count, replace=True)
    facilities = np.random.choice(facility_ids, reservation_count, replace=True)
    
    reservation_id = 0
    idx = 0
    for i in range(reservation_count):
        reservation_id += 1
        
        #generate random date
        date = fake.date()
        
        #get two different users
        users = np.random.choice(user_ids, 2, replace=False)

        query = f"""insert into reservation_individual (reservation_id, sport_id, campus_id, facility_id, date, user_1, user_2)
        values ({reservation_id}, {sports[idx]}, {campuses[idx]}, {facilities[idx]}, {date}, {users[0]} , {users[1]})"""

        #increase index one
        idx += 1
    
    print("Values inserted into 'reservation_ind_match' table successfully!")

def generate_team_reservation(cursor, reservation_count):

    #faker to create date
    fake = Faker()
    
    #get sport_id's from sport table
    query_sport = "select sport_id from sport"
    cursor.execute(query_sport)
    result_sport = cursor.fetchall()
    sport_ids = [row[0] for row in result_sport]

    #get campus_id's from campus table
    query_campus = "select campus_id from campus"
    cursor.execute(query_campus)
    result_campus = cursor.fetchall()
    campus_ids = [row[0] for row in result_campus]
    
    #get facility_id's from facility table
    query_facility = "select facility_id from facility"
    cursor.execute(query_facility)
    result_facility = cursor.fetchall()
    facility_ids = [row[0] for row in result_facility]

    #get user_id's from user table
    query_user = "select team_id from team"
    cursor.execute(query_user)
    result_team = cursor.fetchall()
    team_ids = [row[0] for row in result_team]

    #choose randomly id's
    sports = np.random.choice(sport_ids, reservation_count, replace=True)
    campuses = np.random.choice(campus_ids, reservation_count, replace=True)
    facilities = np.random.choice(facility_ids, reservation_count, replace=True)
    
    reservation_id = 0
    idx = 0
    for i in range(reservation_count):
        reservation_id += 1
        
        #generate random date
        date = fake.date()

        #get two different teams
        teams = np.random.choice(team_ids, 2, replace=False)

        query = f"""insert into reservation_individual (reservation_id, sport_id, campus_id, facility_id, date, team_1, team_2)
        values ({reservation_id}, {sports[idx]}, {campuses[idx]}, {facilities[idx]}, {date}, {teams[0]}, {teams[1]})"""

        #increase index one
        idx += 1

    print("Values inserted into 'reservation_team' table successfully!")