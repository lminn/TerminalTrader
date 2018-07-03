#!/usr/bin/env python3

from flask import Blueprint, render_template, request

from core import model 


controller = Blueprint('lookup',__name__,url_prefix='/lookup')

@controller.route('/',methods=['GET', 'POST'])
def show_lookup():
	if request.method == 'POST':
		company = request.form["company"]

		#ticker_symbol = model.get_ticker_symbol(company)
		#last_price = model.get_price_by_company(company)
		
		company_details = model.lookup_stock_details(company)
		series_data = model.get_time_series(company)
		try:
			open_prices = series_data[1]
			labels = series_data[2]
		except Exception: 
			pass

		return render_template('lookup.html', company_details=company_details, open_prices=open_prices, labels=labels)
	else:
		return render_template('lookup.html')
