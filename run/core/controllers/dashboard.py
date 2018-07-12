#!/usr/bin/env python3

from flask import Blueprint, render_template, request, g, session 

from core import model 

controller = Blueprint('dashboard',__name__,url_prefix='/dashboard')

@controller.route('/',methods=['GET'])
def show_dashboard():

	username = g.user
	user_login = model.get_username(username)


	leaderboard = model.get_leaderboard_by_portfolio_value()

	profitloss = model.get_leaderboard_by_profit_loss()

	top_stocks, shares, percentages = model.get_top_ten_stocks()

	return render_template('homepage.html',  user_login=user_login, leaderboard=leaderboard, profitloss=profitloss,top_stocks=sorted(zip(percentages,top_stocks,shares),reverse=True))




@controller.before_request
def before_request():
	g.user = None
	if 'user' in session:
		g.user = session['user']
