#!/usr/bin/env python3

from flask import Blueprint, render_template, request

from core import model 


controller = Blueprint('buy',__name__,url_prefix='/buy')

@controller.route('/',methods=['GET','POST'])
def show_buy():
	if request.method == 'POST':
		ticker_symbol = request.form["ticker"]
		volume = request.form["volume"]
		model.buy(ticker_symbol, volume, 'lindsay@aol.com')
		print("Got some results!")
		return render_template('buy.html', volume=volume, ticker_symbol=ticker_symbol)
	else:
		return render_template('buy.html')

