from flask import Flask
from flask_login import LoginManager
from flask_mysqldb import MySQL
import yaml
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)

with open('config.yaml', 'r') as config_file:
    db = yaml.load(config_file, Loader=yaml.FullLoader)
    
app.config['MYSQL_HOST'] = db['host']
app.config['MY SQL_USER'] = db['user']
app.config['MYSQL_PASSWORD'] = db['passwd']
app.config['MYSQL_DB'] = db['database']

app.config['SECRET_KEY'] = 'voltran1234'
print("hello")
# Initialize CSRF protection
csrf = CSRFProtect(app)
mysql = MySQL(app)

login_manager = LoginManager(app)