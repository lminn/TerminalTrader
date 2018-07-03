#!/usr/bin/env python3

import json

from flask import Blueprint, render_template, request

from core import model 


controller = Blueprint('portfolio',__name__,url_prefix='/portfolio')

@controller.route('/',methods=['GET'])
def show_portfolio():
		

		# Get portfolio data
		ticker_symbols, share_amounts, purchase_prices, last_prices = model.display_holdings_for_user('lindsay@aol.com')
		user_holdings = zip(ticker_symbols, share_amounts, purchase_prices, last_prices)

		# Get portfolfio data over time to graph value 
		dates, portfolio_values = model.get_portfolio_value_over_time('lindsay@aol.com')
		highest_price = max(portfolio_values)
		dates.sort()
		earliest_date = dates[0]
		last_date = dates[-1]
		middle_date = dates[int(len(dates)/2)]
		labels = [last_date, middle_date, earliest_date]
		mylist = zip(dates, portfolio_values)
		percentages = model.get_portfolio_percentage('lindsay@aol.com')


		# Get transaction data
		trans_dates, ticker_symbols, trans_types, volumes, stock_prices = model.get_user_transactions('lindsay@aol.com')
		user_transactions = zip(trans_dates, ticker_symbols, trans_types, volumes, stock_prices)


		return render_template('portfolio.html', dates=dates, portfolio_values=portfolio_values,user_holdings=user_holdings, 
			user_transactions=user_transactions, highest_price=highest_price, labels=labels, percentages=percentages)



@controller.route('/',methods=['POST'])
def show_user_portfolio():
		return render_template('portfolio.html')

