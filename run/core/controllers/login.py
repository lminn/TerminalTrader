#!/usr/bin/env python3

import secrets 

from flask import Blueprint, render_template, request, make_response, g, session, redirect, url_for

from core import model




controller = Blueprint('login',__name__,url_prefix='/login')
controller.secret_key = secrets.token_hex(16) 

# app = Flask('general',__name__,url_prefix='/')
# controller.secret_key = secrets.token_hex(16) 

@controller.route('/',methods=['GET','POST'])
def show_login():
	if request.method == 'POST':
		# Assuming it's a POST request
		session.pop('user', None)
		username = request.form['email']
		password = request.form['password']

		try:
			admin, username = model.login(username,password)
			session['user'] = request.form['email']
			user_login = model.get_username(username)
			return render_template('dashboard.html', user_login=user_login)
		except Exception:
			error_message = "Incorrect username or password."
			return render_template('login.html')

	return render_template('login.html')



@controller.route('/home')
def show_home():
	if g.user:
		return render_template('dashboard.html')	
	return render_template('login.html')



@controller.before_request
def before_request():
	g.user = None
	if 'user' in session:
		g.user = session['user']



@controller.route('/logout')
def logout():
	session.pop('user', None)
	return render_template('login.html')



if __name__ == '__main__':
	app.run(debug=True)