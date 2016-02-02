from app import app  #haetaan app moduulista app __init__.py tiedostosta
#render_template gives you access to Jinja2 template engine
#router-funktion pitää aina palauttaa jotakin : sisältö tai header-tieto
from flask import render_template, request, make_response, flash, redirect
from app.forms import LoginForm, RegisterForm, FriendsForm
from app.db_models import Users
from app import db

@app.route('/',methods=['GET','POST'])
def index(): #instanssi login-formista
	login = LoginForm()
	#Check if get method
	if request.method == 'GET':
		return render_template('template_index.html',form=login)
	else:
		#check if form data is valid
		if login.validate_on_submit(): #zekkaa onko validatoreilla tarkistettu data validia
			print(login.email.data) #pythonilla ei tarvi requestista hakea dataa, vaan suoraan formilta
			print(login.passw.data)
			return render_template('template_user.html',form=login) # renderöidään template_user.html
		else:
			flash('Give proper information to email and password fields!')
			return render_template('template_index.html',form=login)			
	
	
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
            db.session.add(user)
            db.session.commit()			
            flash("Name {0}".format(form.email.data)) #dynaaminen merkkijono, {0} korvataan form.email.data 
            return redirect('/')
        else:
            flash('Invalid email address or no password given')
            return render_template('template_register.html',form=form)			


@app.route('/friends',methods=['GET','POST'])
def saveFriend():
    form = FriendsForm()
    if request.method == 'GET':
        return render_template('template_friends.html',form=form)
    else:
        if form.validate_on_submit():
            friend = Friends(form.name.data,form.address.data,form.age.data)
            db.session.add(friend)
            db.session.commit()			
            flash("Name {0}".format(form.name.data)) #dynaaminen merkkijono, {0} korvataan form.email.data 
            return redirect('/')
        else:
            flash('At least one field is empty')
            return render_template('template_friends.html',form=form)			

    


print('This is not any more included in index() function')

"""This is comment
    you can use multiple lines"""
