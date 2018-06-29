#!/usr/bin/env python3

from flask import Blueprint, render_template, request

from core import model 


controller = Blueprint('sell',__name__,url_prefix='/sell')


@controller.route('/',methods=['GET'])
def show_sell():

	return render_template('sell.html')


@controller.route('/company',methods=['POST'])
def search_form():
	company = request.form["company"]
	ticker_symbol = model.get_ticker_symbol(company)
	last_price = model.get_price_by_company(company)
	return render_template('sell.html', company=company,ticker_symbol=ticker_symbol, last_price=last_price)

@controller.route('/',methods=['POST'])
def sell_form():
	ticker_symbol = request.form["ticker"]
	volume = request.form["volume"]
	last_price = model.get_price_by_ticker_symbol(ticker_symbol)
	result = model.sell(ticker_symbol, volume, 'lindsay@aol.com')

	if "." not in result: 
		pass
	else: 
		if int(volume) > 1:
			result = "You have sold {0} shares of {1}.\nYour new balance is ${2}".format(volume,ticker_symbol,result)
		else:
			result = "You have sold {0} share of {1}.\nYour new balance is ${2}".format(volume,ticker_symbol,result)


	return render_template('sell.html',result=result)

