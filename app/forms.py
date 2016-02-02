from flask.ext.wtf import Form 
from wtforms import StringField,PasswordField,SubmitField 
from wtforms.validators import Required,Email

class LoginForm(Form): # LoginForm perii Formin eli esim <input type="text"/>, <input type="submit"/> #
	email = StringField('Enter your email',validators=[Required(),Email()])
	passw = PasswordField('Enter password', validators=[Required()])
	submit = SubmitField('Login')

class RegisterForm(Form):
	email = StringField('Enter your email',validators=[Required(),Email()])
	passw = PasswordField('Enter password', validators=[Required()])
	submit = SubmitField('Login')
    
class FriendsForm(Form):
    name = StringField('Name:', validators=[Required()])
    address = StringField('Address:', validators=[Required()])
    age = StringField('Age:', validators=[Required()])
    submit = SubmitField('Save')
	