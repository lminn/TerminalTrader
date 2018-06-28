#!/usr/bin/env python3

from flask import Blueprint, render_template, request

from core import model 


controller = Blueprint('lookup',__name__,url_prefix='/lookup')

@controller.route('/',methods=['GET', 'POST'])
def show_lookup():
	if request.method == 'POST':
		company = request.form["company"]

		ticker_symbol = model.get_ticker_symbol(company)
		last_price = model.get_price_by_company(company)

		return render_template('lookup.html', company=company,ticker_symbol=ticker_symbol, last_price=last_price)
	else:
		return render_template('lookup.html')
