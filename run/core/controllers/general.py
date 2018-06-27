#!/usr/bin/env python3

from flask import Blueprint, render_template, request

from core import model


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
		
		try:
			admin, username = model.login(username,password)
			return render_template('dashboard.html')
		except Exception:
			error_message = "Incorrect username or password."
			return render_template('login.html')





