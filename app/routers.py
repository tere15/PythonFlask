from app import app  #haetaan app moduulista app __init__.py tiedostosta
#render_template gives you access to Jinja2 template engine
#router-funktion pitää aina palauttaa jotakin : sisältö tai header-tieto
from flask import render_template, request, make_response
from app.forms import LoginForm

@app.route('/',methods=['GET','POST'])
def index():
	login = LoginForm()
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


	
print('This is not any more included in index() function')

"""This is comment
    you can use multiple lines"""
