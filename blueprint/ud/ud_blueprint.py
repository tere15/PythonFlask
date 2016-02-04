from flask import Blueprint, session, redirect, request, flash, url_for #render_template
from app.forms import FriendForm
from app import db
from app.db_models import Users,Friends
from werkzeug import secure_filename

#Create blueprint
#First argument is the name of the blueprint folder
#second is always __name__ attribute
#third parameter tells what folder contains your templates

ud = Blueprint('ud',__name__,template_folder='templates',url_prefix=('/app/'))
#url_prefix määritellään, niin ei tarvi laittaa joka routeen

#/app/delete
@ud.route('delete/<int:id>')
#@ud.route('delete/')
def delete(id):
	#pass
	return "Delete"

@ud.route('update')
def update():
	#pass
	return "Update"


@ud.route('/friends',methods=['GET','POST'])
def friends():
	#Check that user has logged in before you let execute this route
	#if not('isLogged in session') or (session['isLogged'] == False):
	#	return redirect('/')
	form = FriendForm()
	if request.method == 'GET':
		return render_template('template_friends.html',form=form, isLogged=True)
	else:
		if form.validate_on_submit():

			temp = Friends(form.name.data,form.address.data,form.age.data,session['user_id'])

			#Save the image if present
			if form.upload_file.data:
				filename = secure_filename(form.upload_file.data.filename)
				form.upload_file.data.save('app/static/images' + form.upload_file.data.filename)			
				temp.filename ='/static/images/' + filename
			
			db.session.add(temp)
			db.session.commit()	
			#tapa 2
			user = Users.query.get(session['user_id'])
			print(user.friends)
			return render_template('template_user.html',isLogged=True,friends=user.friends)			            
		else:
			flash('At least one field is empty')
			return render_template('template_friends.html',isLogged=True,form=form)			

def before_request():
	if not 'isLogged' in session:
		return redirect('/')
	
ud.before_request(before_request) #tehään ennen routeen siirtymistä	