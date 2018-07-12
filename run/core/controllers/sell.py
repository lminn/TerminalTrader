#!/usr/bin/env python3

from flask import Blueprint, render_template, request, g, session

from core import model 


controller = Blueprint('sell',__name__,url_prefix='/sell')


@controller.route('/',methods=['GET'])
def show_sell():

	username = g.user
	user_login = model.get_username(username)


	return render_template('sell.html',  user_login=user_login)


@controller.route('/company',methods=['POST'])
def search_form():

	username = g.user
	user_login = model.get_username(username)

	company = request.form["company"]
	ticker_symbol = model.get_ticker_symbol(company)
	last_price = model.get_price_by_company(company)
	return render_template('sell.html',  user_login=user_login,company=company,ticker_symbol=ticker_symbol, last_price=last_price)

@controller.route('/',methods=['POST'])
def sell_form():

	username = g.user
	user_login = model.get_username(username)

	ticker_symbol = request.form["ticker"]
	print("Tickeer: ",ticker_symbol)
	volume = request.form["volume"]
	print("Volume",volume)
	last_price = model.get_price_by_ticker_symbol(ticker_symbol)
	print("Last Price",last_price)
	result = model.sell(ticker_symbol, volume, username)
	print("Result",result)

	if "." not in result: 
		pass
	else: 
		if int(volume) > 1:
			result = "You have sold {0} shares of {1}.\nYour new balance is ${2}".format(volume,ticker_symbol,result)
		else:
			result = "You have sold {0} share of {1}.\nYour new balance is ${2}".format(volume,ticker_symbol,result)


	return render_template('sell.html', user_login=user_login,result=result)



@controller.before_request
def before_request():
	g.user = None
	if 'user' in session:
		g.user = session['user']
