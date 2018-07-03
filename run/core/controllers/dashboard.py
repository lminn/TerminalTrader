#!/usr/bin/env python3

from flask import Blueprint, render_template, request, g, session 

from core import model 

controller = Blueprint('dashboard',__name__,url_prefix='/dashboard')

@controller.route('/',methods=['GET'])
def show_dashboard():

	username = g.user
	user_login = model.get_username(username)


	leaders, scores = model.get_leaderboard_by_portfolio_value()


	leaderbord = zip(leaders, scores)

	return render_template('homepage.html', leaderbord=leaderbord, user_login=user_login)



@controller.before_request
def before_request():
	g.user = None
	if 'user' in session:
		g.user = session['user']
