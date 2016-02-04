from flask import Blueprint, session, redirect, request, render_template,flash
from app.forms import LoginForm, RegisterForm
from app import db
from app.db_models import Users,Friends
from flask.ext.bcrypt import check_password_hash


auth = Blueprint('auth',__name__,template_folder='templates')

@auth.route('/',methods=['GET','POST'])
def index(): #instanssi login-formista
	login = LoginForm()
	#Check if get method
	if request.method == 'GET':
		return render_template('template_index.html',form=login,isLogged=False)
	else:
		#check if form data is valid
		if login.validate_on_submit(): #zekkaa onko validatoreilla tarkistettu data validia
			#Check id correct username and password
			user = Users.query.filter_by(email=login.email.data)
			#muodostaa: Select email passw From User Where email="?" And Passw="?"
			#all()=[], first()=object
			if (user.count() == 1) and (check_password_hash(user[0].passw,login.passw.data)):
				print(user[0])
				session['user_id'] = user[0].id
				session['isLogged'] = True
				#tapa 1
				friends = Friends.query.filter_by(user_id=user[0].id)
				print(friends)
				return render_template('template_user.html',isLogged=True, friends=friends)
			else:
				flash('Wrong email or password')
			
			#print(login.email.data) #pythonilla ei tarvi requestista hakea dataa, vaan suoraan formilta
			#print(login.passw.data)
				return render_template('template_user.html',form=login, isLogged=False) # renderöidään template_user.html
		#form data was not valid
		else:
			flash('Give proper information to email and password fields!')
			return render_template('template_index.html',form=login,isLogged=False)			
	
@auth.route('/logout')
def logout():
	#delete user session (clear all values)
	session.clear()
	return redirect('/')
	
@auth.route('/user/<name>')
def user(name):
	print(request.headers.get('User-Agent'))
	return render_template('template_user.html',name=name)

#Example how you can define route methods
@auth.route('/user',methods=['GET','POST'])
def userParams():
	name = request.args.get('name') #url-attribuutin sisältö name-muuttujaan
	return render_template('template_user.html',name=name)	

@auth.route('/register',methods=['GET','POST'])
def registerUser():
	form = RegisterForm()
	if request.method == 'GET':
		return render_template('template_register.html',form=form)	
	else:
		if form.validate_on_submit():
			user = Users(form.email.data,form.passw.data)
			try:
				db.session.add(user)
				db.session.commit()
			except:
				db.session.rollback() #otetaan päivitetty tieto pois tietokannasta, ei tarvi välttis kutsua, tekee automaattisesti
				flash('Username allready in use')
				return render_template('template_register.html',form=form)
			flash("Name {0}".format(form.email.data)) #dynaaminen merkkijono, {0} korvataan form.email.data 
			return redirect('/')
		else:
			flash('Invalid email address or no password given')
			return render_template('template_register.html',form=form)			

