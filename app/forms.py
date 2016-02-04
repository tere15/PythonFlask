from flask.ext.wtf import Form 
from wtforms import StringField,PasswordField,SubmitField,IntegerField, FileField
from wtforms.validators import Required,Email,NumberRange

class LoginForm(Form): # LoginForm perii Formin eli esim <input type="text"/>, <input type="submit"/> #
	email = StringField('Enter your email',validators=[Required(),Email()])
	passw = PasswordField('Enter password', validators=[Required()])
	submit = SubmitField('Login')

class RegisterForm(Form):
	email = StringField('Enter your email',validators=[Required(),Email()])
	passw = PasswordField('Enter password', validators=[Required()])
	submit = SubmitField('Login')
    
class FriendForm(Form):
	name = StringField('Enter your friend\'s name:', validators=[Required()])
	address = StringField('Enter your friend\'s address:', validators=[Required()])
	age = IntegerField('Enter your friend\'s age:', validators=[Required(),NumberRange(min=0,max=150,message="Enter value between 0-115")])
	upload_file = FileField('Upload Image')
	submit = SubmitField('Save')
	