#!/usr/bin/env python3

from flask import Blueprint, render_template, request

from core import model 


controller = Blueprint('sell',__name__,url_prefix='/sell')

@controller.route('/',methods=['GET','POST'])
def show_sell():
	if request.method == 'POST':
		
		ticker_symbol = request.form["ticker"]
		volume = request.form["volume"]

		result = model.sell(ticker_symbol, volume, 'lindsay@aol.com')

		if "." not in result: 
			pass
		else: 
			if int(volume) > 1:
				result = "You have sold {0} shares of {1}.\nYour new balance is ${2}".format(volume,ticker_symbol,result)
			else:
				result = "You have sold {0} share of {1}.\nYour new balance is ${2}".format(volume,ticker_symbol,result)


		return render_template('sell.html',result=result)
	else:
		return render_template('sell.html')

