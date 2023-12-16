from flask_wtf import FlaskForm
from wtforms import DateField, IntegerField, StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError


class LoginForm(FlaskForm):
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])    
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in', render_kw={"class": "form-container button"})
    
class RegisterForm(FlaskForm):
    name = StringField(label='Name:', validators=[Length(min=2, max=20), DataRequired()])
    surname = StringField(label='Surname:', validators=[Length(min=2, max=20), DataRequired()])
    student_number = IntegerField(label='Student Number:', validators=[DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])    
    password = StringField(label='Password:', validators=[DataRequired()])    
    phone_number = StringField(label='Phone Number:', validators=[Length(min=2, max=18), DataRequired()])    
    birth_date = DateField(label='Birth Date:', validators=[DataRequired()])
    faculty = StringField(label='Faculty:', validators=[Length(min=2, max=50), DataRequired()])
    department = StringField(label='Department:', validators=[Length(min=2, max=50), DataRequired()])
    gender = StringField(label='Gender:', validators=[Length(1), DataRequired()])
    submit = SubmitField(label='Register')