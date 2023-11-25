import mysql.connector as connector
import yaml


def read_config():
    # config file keeps the parameters like host, user, password and sql command paths
    # you can change them if needed
    with open("create_db/config.yaml", "r") as f:
        config = yaml.safe_load(f)
    return config


def create_db():
    config = read_config()

    host = config["host"] # assigns host information to host variable
    user = config["user"]  # assigns user information to user variable
    passwd = config["passwd"]  # you need to change passwd key located in 'config.yaml' to your password

    mydb = connector.connect(
        host=host,
        user=user,
        passwd=passwd,
        auth_plugin="mysql_native_password" # necessary
    )

    db_script = config["sqldb_path"] # path to sql commands that creates 'reservation' database
    table_script = config["sqltables_path"] # path to sql commands that creates tables for our database

    mycursor = mydb.cursor()

    with open(db_script, "r") as db_file: # reads .sql scripts
        db_command = db_file.read().split(";")

    try: # try to create database
        mycursor.execute(db_command[0]) 
    except connector.errors.DatabaseError:
        # if database ('reservation') already exists, print table names to the screen and return
        print("Database already exists!")
        mycursor.execute("USE RESERVATIONS")
        print("Tables:")
        mycursor.execute("SHOW TABLES")
        for table in mycursor:
            print(f"- {table[0]}")
        return


    print("Database is created successfully!")
    with open(table_script, "r") as tables_file: # reads the .sql scripts to create necessary tables
        tables_commands = tables_file.read().split(";")

    for table_command in tables_commands: # block to create each tables
        if table_command.strip():
            mycursor.execute(table_command)
    mydb.commit()
    print("Tables are created successfully!")

    # print tables to the screen
    mycursor.execute("USE RESERVATIONS")
    print("Tables:")
    mycursor.execute("SHOW TABLES")
    for table in mycursor:
        print(f"- {table[0]}")