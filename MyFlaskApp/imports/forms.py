from flask_wtf import FlaskForm
from wtforms import DateField, IntegerField, StringField, PasswordField, SubmitField, SelectField
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

class MatchHistFrom(FlaskForm):
    sports = SelectField(label='Sport', choices=[], validators=[DataRequired()])
    submit_button = SubmitField(label = 'See Results')
    
    def __init__(self, sports, placeholder, *args, **kwargs):
        super(FlaskForm, self).__init__(*args, **kwargs)

        sports = list(sports)

        if placeholder == "*":
            sports.insert(0, ("*", "All Sports"))
        else:
            placeholder = [tup for tup in sports if str(tup[0]) == placeholder][0]
            sports.remove(placeholder)
            sports.insert(0, placeholder)
            sports.insert(1, ("*", "All Sports"))

        self.sports.choices = sports

    