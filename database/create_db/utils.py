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

    try: # try to create database
        cursor.execute(db_command[0]) 
    except:
        # if database ('reservation') already exists, print table names to the screen and return
        print("Database already exists!")
        cursor.execute("USE RESERVATIONS")
        print("Tables:")
        cursor.execute("SHOW TABLES")
        for table in cursor:
            print(f"- {table[0]}")
        return


    print("Database is created successfully!")
    with open(table_script, "r") as tables_file: # reads the .sql scripts to create necessary tables
        tables_commands = tables_file.read().split(";")

    for table_command in tables_commands: # block to create each tables
        if table_command.strip():
            cursor.execute(table_command)
    print("Tables are created successfully!")

    # print tables to the screen
    cursor.execute("USE RESERVATIONS")
    print("Tables:")
    cursor.execute("SHOW TABLES")
    for table in cursor:
        print(f"- {table[0]}")



def stable_tables(cursor, stables_path):

    # .sql dosyasından sorguyu oku
    with open(stables_path, "r") as tables_file:
        sql_insert = tables_file.read().split(";")

    # Sorguyu çalıştır
    for table_command in sql_insert: # block to create each tables
        if table_command.strip():
            cursor.execute(table_command)

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



