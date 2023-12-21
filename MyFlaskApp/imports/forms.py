from flask_wtf import FlaskForm
from wtforms import DateField, IntegerField, StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError


class LoginForm(FlaskForm):
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()],  render_kw={"id": "login_email"})    
    password = PasswordField(label='Password:', validators=[DataRequired()],  render_kw={"id": "login_passw"})
    submit = SubmitField(label='Sign in', render_kw={"id": "login_submit"})
    
class RegisterForm(FlaskForm):
    name = StringField(label='Name:', validators=[Length(min=2, max=20), DataRequired()])
    surname = StringField(label='Surname:', validators=[Length(min=2, max=20), DataRequired()])
    student_number = IntegerField(label='Student Number:', validators=[DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()], render_kw={"id": "register_email"})    
    password = StringField(label='Password:', validators=[DataRequired()], render_kw={"id": "register_passw"})    
    phone_number = StringField(label='Phone Number:', validators=[Length(min=2, max=18), DataRequired()])    
    birth_date = DateField(label='Birth Date:', validators=[DataRequired()])
    faculty = StringField(label='Faculty:', validators=[Length(min=2, max=50), DataRequired()])
    department = StringField(label='Department:', validators=[Length(min=2, max=50), DataRequired()])
    gender = StringField(label='Gender:', validators=[Length(1), DataRequired()])
    submit = SubmitField(label='Register',render_kw={"id": "register_submit"})

class RankFrom(FlaskForm):
    sports = SelectField(label='sport', choices=[], validators=[DataRequired()])
    order = SelectField(label='order', choices=[])
    orders = [("score", "Total Score"),("count", "Total Maches"),("avrg", "Average score")]
    submit_button = SubmitField(label = 'See Results')
    
    def __init__(self, sports, default_sport, default_ord, *args, **kwargs):
        super(FlaskForm, self).__init__(*args, **kwargs)
        sports = list(sports)

        if default_sport == "*":
            sports.insert(0, ("*", "All Team Sports"))
        else:
            default_sport = [tup for tup in sports if str(tup[0]) == default_sport][0]
            sports.remove(default_sport)
            sports.insert(0, default_sport)
            sports.insert(1, ("*", "All Team Sports"))

        o = self.orders.copy()
        if default_ord != "score":
            default_ord = [tup for tup in self.orders if tup[0] == default_ord][0]
            o.remove(default_ord)
            o.insert(0, default_ord)
            self.order.choices=o

        self.sports.choices = sports
        self.order.choices = o
        
class MatchHistFrom(FlaskForm):
    sports = SelectField(label='sport', choices=[], validators=[DataRequired()])
    submit_button = SubmitField(label = 'See Results')
    
    def __init__(self, sports, placeholder, *args, **kwargs):
        super(FlaskForm, self).__init__(*args, **kwargs)

        sports = list(sports)

        if placeholder == "*":
            sports.insert(0, ("*", "All Individual Sports"))
        else:
            placeholder = [tup for tup in sports if str(tup[0]) == str(placeholder)][0]
            sports.remove(placeholder)
            sports.insert(0, placeholder)
            sports.insert(1, ("*", "All Individual Sports"))

        self.sports.choices = sports
        
class ReservationForm(FlaskForm):
    sports = SelectField(label='sport', choices=[], validators=[DataRequired()])
    campuses = SelectField(label='campus', choices=[], validators=[DataRequired()])
    area = SelectField(label='area', choices=[], validators=[DataRequired()])
    set_time = DateField(label='res_time', format='%Y-%m-%d', validators=[DataRequired()])
    submit_button = SubmitField(label = 'See Results')  

    def __init__(self, sports, campuses, area, default_sport, default_campus, default_area, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)
        self.sports.choices = [(str(s[0]), s[1]) for s in sports]
        self.campuses.choices = [(str(c[0]), c[1]) for c in campuses]
        self.area.choices = [(str(a[0]), a[1]) for a in area]

        # Dropdown sport
        if default_sport == "*":
            self.sports.choices.insert(0, ("*", "All Sports"))
        else:
            default_sport_tuple = next((tup for tup in sports if str(tup[0]) == default_sport), None)
            if default_sport_tuple:
                if default_sport_tuple in self.sports.choices:
                    self.sports.choices.remove(default_sport_tuple)
                self.sports.choices.insert(0, (str(default_sport_tuple[0]), default_sport_tuple[1]))
                self.sports.choices.insert(1, ("*", "All Sports"))

        # Dropdown campus
        if default_campus == "*":
            self.campuses.choices.insert(0, ("*", "All Campuses"))
        else:
            default_campus_tuple = next((tup for tup in campuses if str(tup[0]) == default_campus), None)
            if default_campus_tuple:
                if default_campus_tuple in self.campuses.choices:
                    self.campuses.choices.remove(default_campus_tuple)
                self.campuses.choices.insert(0, (str(default_campus_tuple[0]), default_campus_tuple[1]))
                self.campuses.choices.insert(1, ("*", "All Campuses"))

        # Dropdown area
        if default_area == "*":
            self.area.choices.insert(0, ("*", "All Saloons"))
        else:
            default_area_tuple = next((tup for tup in area if str(tup[0]) == default_area), None)
            if default_campus_tuple:
                if default_area_tuple in self.area.choices:
                        self.area.choices.remove(default_area_tuple)
                self.area.choices.insert(0, (str(default_area_tuple[0]), default_area_tuple[1]))
                self.area.choices.insert(1, ("*", "All Saloons"))
    
    