#!/usr/bin/env python3

from flask import Blueprint, render_template, request

from core import model 


controller = Blueprint('buy',__name__,url_prefix='/buy')

@controller.route('/',methods=['GET','POST'])
def show_buy():
	if request.method == 'POST':
		company = request.form["company"]
		ticker_symbol = request.form["ticker"]
		volume = request.form["volume"]

		last_price = model.get_price_by_company(company)
		result = model.buy(ticker_symbol, volume, 'lindsay@aol.com')

		if "." not in result: 
			pass
		else: 
			if int(volume) > 1:
				result = "You have purchased {0} shares of {1}.\nYour new balance is ${2}".format(volume,ticker_symbol,result)
			else:
				result = "You have purchased {0} share of {1}.\nYour new balance is ${2}".format(volume,ticker_symbol,result)


		return render_template('buy.html',result=result, ticker_symbol=ticker_symbol, last_price=last_price)
	else:
		return render_template('buy.html')

