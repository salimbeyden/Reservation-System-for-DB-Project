import numpy as np
import random
from faker import Faker
import yaml


def read_config():
    # config file keeps the parameters like host, user, password and sql command paths
    # you can change them if needed
    with open("config.yaml", "r") as f:
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