#!/usr/bin/env python3

from flask import Blueprint, render_template, request


controller = Blueprint('general',__name__,url_prefix='/')
#controller = Blueprint('general',__name__,url_prefix='')


@controller.route('/',methods=['GET','POST'])
def show_login():
	if request.method == 'GET':
		return render_template('login.html')
	else:
		# Assuming it's a POST request
		username = request.form['email']
		password = request.form['password']
		if username != 'lindsay@aol.com' or password != 'pass':
			return render_template('login.html')
		else:
			return render_template('dashboard.html')

		#print(username, password)