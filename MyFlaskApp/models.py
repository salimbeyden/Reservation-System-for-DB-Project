from flask_login import UserMixin, current_user
from MyFlaskApp import mysql, login_manager

class User(UserMixin):
    def __init__(self, user_id, email, name, surname, tel_no, faculty_name, department, 
                 birth_date, password, gender, f_team_id=None, v_team_id=None, b_team_id=None, t_team_id=None, p_team_id=None):
        self.school_id = user_id
        self.name = name
        self.surname = surname
        self.email = email
        self.tel_no = tel_no
        self.faculty_name = faculty_name
        self.department = department
        self.birth_date = birth_date
        self.password = password
        self.gender = gender
        self.f_team_id = f_team_id
        self.v_team_id = v_team_id
        self.b_team_id = b_team_id
        self.t_team_id = t_team_id
        self.p_team_id = p_team_id
    
    def get_id(self):
        return str(self.school_id) 

@login_manager.user_loader
def load_user(user_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM user WHERE school_id  = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    if user:
        return User(user_id, name=user[1], surname=user[2], email=user[3], tel_no=user[4], faculty_name=user[5], department=user[6], 
                 birth_date=user[7], password=user[8], gender=user[9], f_team_id=user[10], v_team_id=user[11], b_team_id=user[12], t_team_id=user[13], p_team_id=user[14])  # Adjust fields as needed
    return None
