from flask import Flask
from flask_login import LoginManager
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'

with open('config.yaml', 'r') as config_file:
    db = yaml.load(config_file, Loader=yaml.FullLoader)
    
app.config['MYSQL_HOST'] = db['host']
app.config['MY SQL_USER'] = db['user']
app.config['MYSQL_PASSWORD'] = db['passwd']
app.config['MYSQL_DB'] = db['database']

mysql = MySQL(app)

login_manager = LoginManager(app)