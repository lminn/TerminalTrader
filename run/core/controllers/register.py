#!/usr/bin/env python3

from flask import Blueprint, render_template, request, g, session

from core import model


controller = Blueprint('register',__name__,url_prefix='/register')


@controller.route('/',methods=['GET'])
def load():
	session.pop('user', None)
	return render_template('register.html')


@controller.route('/',methods=['POST'])
def sumbit():
		print('Trying to submit 1')
		session.pop('user', None)
		email = request.form['email']
		username = request.form['username']
		password = request.form['password']
		gender = request.form['gender']
		country = request.form['country']
		
		validation, message = model.new_user(username, email, password, country, gender)
		print('Trying to submit 2 ')

		
		return render_template('register.html', message=message, validation=validation)


