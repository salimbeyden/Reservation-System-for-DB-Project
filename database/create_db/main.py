import mysql.connector as connector
from utils import *
import constants as c


config = read_config()


host = config["host"] # assigns host information to host variable
user = config["user"]  # assigns user information to user variable
passwd = config["passwd"]  # you need to change passwd key located in 'config.yaml' to your password
stables_path = config["stabletables_path"]

mydb = connector.connect(
    host=host,
    user=user,
    passwd=passwd,
    auth_plugin="mysql_native_password" # necessary
)


cursor = mydb.cursor()

create_db(cursor, config)


stable_tables(cursor, stables_path)

generate_user_table(cursor ,c.FACULTY, c.MAJOR_DICT, c.USER_COUNT)


mydb.commit()