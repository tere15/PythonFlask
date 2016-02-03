from app import app  #haetaan app moduulista app __init__.py tiedostosta
#render_template gives you access to Jinja2 template engine
#router-funktion pitää aina palauttaa jotakin : sisältö tai header-tieto
from flask import render_template, request, make_response, flash, redirect, session
from app.forms import LoginForm, RegisterForm, FriendForm
from app.db_models import Users,Friends
from app import db

@app.route('/',methods=['GET','POST'])
def index(): #instanssi login-formista
	login = LoginForm()
	#Check if get method
	if request.method == 'GET':
		return render_template('template_index.html',form=login,isLogged=False)
	else:
		#check if form data is valid
		if login.validate_on_submit(): #zekkaa onko validatoreilla tarkistettu data validia
			#Check id correct username and password
			user = Users.query.filter_by(email=login.email.data).filter_by(passw=login.passw.data)
			#muodostaa: Select email passw From User Where email="?" And Passw="?"
			#all()=[], first()=object
			if user.count() == 1:
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
	
@app.route('/logout')
def logout():
	#delete user session (clear all values)
	session.clear()
	return redirect('/')
	
@app.route('/user/<name>')
def user(name):
	print(request.headers.get('User-Agent'))
	return render_template('template_user.html',name=name)

#Example how you can define route methods
@app.route('/user',methods=['GET','POST'])
def userParams():
	name = request.args.get('name') #url-attribuutin sisältö name-muuttujaan
	return render_template('template_user.html',name=name)	

@app.route('/register',methods=['GET','POST'])
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


@app.route('/friends',methods=['GET','POST'])
def friends():
	#Check that user has logged in before you let execute this route
	if not('isLogged in session') or (session['isLogged'] == False):
		return redirect('/')
	form = FriendForm()
	if request.method == 'GET':
		return render_template('template_friends.html',form=form, isLogged=True)
	else:
		if form.validate_on_submit():
			temp = Friends(form.name.data,form.address.data,form.age.data,session['user_id'])
			db.session.add(temp)
			db.session.commit()	
			#tapa 2
			user = Users.query.get(session['user_id'])
			print(user.friends)
			return render_template('template_user.html',isLogged=True,friends=user.friends)			            
		else:
			flash('At least one field is empty')
			return render_template('template_friends.html',form=form,isLogged=True)			

    


print('This is not any more included in index() function')

"""This is comment
    you can use multiple lines"""
