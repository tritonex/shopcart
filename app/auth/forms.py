from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Length, EqualTo
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Passwort', validators=[DataRequired()])
    remember_me = BooleanField('Angemeldet bleiben')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=3, max=20, message="Username muss zwischen 3 und 20 Zeichen lang sein")
    ])
    password = PasswordField('Passwort', validators=[
        DataRequired(),
        Length(min=6, message="Das Passwort muss mindestens 6 Zeichen lang sein")
    ])
    password2 = PasswordField('Passwort wiederholen', 
                            validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrieren')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Dieser Username ist bereits vergeben.')
        