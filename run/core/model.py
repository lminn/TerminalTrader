#!/usr/bin/env python3

import datetime
import getpass
import json
import os
import sqlite3 
import traceback
import sys

import numpy as np
import pandas as pd
import requests


from core import mapper
from core import wrapper 



width = os.get_terminal_size().columns


def get_price_by_company(company_name):
	""" Print ticker symbol and stock price.""" 

	try: 
		ticker_symbol = wrapper.get_ticker_symbol(company_name) 
		last_price = wrapper.get_last_price(ticker_symbol)
	
		last_price = ("%0.2f" % last_price)
		return last_price
	except:
		error_message = "No data for {0} was found.".format(company_name)
		return error_message
		

def get_ticker_symbol(company_name):
	""" Print ticker symbol and stock price.""" 

	try: 
		ticker_symbol = wrapper.get_ticker_symbol(company_name) 

		return ticker_symbol
	except:
		error_message = "No data for {0} was found.".format(company_name)
		return error_message


def get_price_by_ticker_symbol(ticker_symbol):
	""" Print ticker symbol and stock price.""" 

	try: 
		last_price = wrapper.get_last_price(ticker_symbol)
	
		last_price = ("%0.2f" % last_price)
		return last_price
	except:
		error_message = "No data for {0} was found.".format(ticker_symbol)



def buy(ticker_symbol, trade_volume, username):
	""" Buy stock(s) given the ticker symbol and amount. """

	try:
		trade_volume = int(trade_volume)
		brokerage_fee = 6.95
		last_price = wrapper.get_last_price(ticker_symbol)

		# Check to make sure the user has sufficient funds to process the transaction
		transaction_cost = float((last_price*float(trade_volume))-brokerage_fee)

		# Get balance
		user_balance = float(mapper.get_balance(username))

		if float(transaction_cost) <  float(user_balance):  

			holdings_record = mapper.get_holdings_record(username, ticker_symbol) 
			last_price = wrapper.get_last_price(ticker_symbol)


			# Check to see if there is already a record for the given ticker symbol
			if len(holdings_record) == 0:
				vwap = last_price    
				
				ticker_symbol = ticker_symbol.strip()
				mapper.add_holdings_record(ticker_symbol,trade_volume,last_price,username)  
				new_balance = float(user_balance) - float(transaction_cost)
				mapper.update_balance(username, new_balance)
																											
			else:
				# Get share volume 
				current_amount_of_shares = int(holdings_record[0][1])
				cumulative_shares = current_amount_of_shares + int(trade_volume)

				# Update the holdings record
				vwap = calculate_vwap(username, ticker_symbol)
				mapper.update_holdings_record(username,ticker_symbol,cumulative_shares,last_price,vwap)
				#mapper.update_holdings_record(username,ticker_symbol,cumulative_shares,last_price)
				#Update the user balance
				new_balance = float(user_balance) - float(transaction_cost)
				mapper.update_balance(username, new_balance)
								
			# Record the transaction
			trans_date = datetime.datetime.now()
			total = float(trade_volume) * float(last_price)
			mapper.add_transaction(username,trans_date,'Buy', ticker_symbol,trade_volume,last_price,total)
		
			new_balance = ("%0.2f" %  new_balance)
			return new_balance
		else:
			error_message = ('You do not have enough funds to execute the trade')
			return error_message 

	except Exception as ex:
		print(ex)

		

def sell(ticker_symbol, trade_volume, username):
	""" Sell the given amount of stock for the given company."""

	try:
		# Get balance
		balance = float(mapper.get_balance(username))

		# Assumes the brokerage_fee is required to sell
		brokerage_fee = 6.95
		last_price = wrapper.get_last_price(ticker_symbol)
		profit = (last_price*float(trade_volume))-brokerage_fee

		# Check if the user already has the stock in the holdings table
		holdings_record = mapper.get_holdings_record(username, ticker_symbol) 
		if len(holdings_record) > 0:
			amount_of_shares = int(holdings_record[0][1])
			# Check if the user has enough shares to sell
			if amount_of_shares >= int(trade_volume):
				new_balance = float(balance) + float(profit)
				mapper.update_balance(username, new_balance)

				# Get share volume 
				current_amount_of_shares = int(holdings_record[0][1])
				cumulative_shares = current_amount_of_shares - int(trade_volume)

				# Record Transaction
				trans_date = datetime.datetime.now()
				total = float(trade_volume) * float(last_price)
				mapper.add_transaction(username,trans_date,'Sell', ticker_symbol,trade_volume,last_price,total)
				vwap = calculate_vwap(username, ticker_symbol)

				# Update holdings 
				mapper.update_holdings_record(username,ticker_symbol,cumulative_shares,last_price,vwap)
				#mapper.update_holdings_record(username,ticker_symbol,cumulative_shares,last_price)


				new_balance = ("%0.2f" %  new_balance)
				return new_balance

			else:
				error_message = "You do not have enough shares of {0} to sell.".format(ticker_symbol)
				return error_message


		else:
			error_message = 'You do not own have any {0} shares to sell'.format(ticker_symbol)
			return error_message

	except Exception:
		print(ex)


def get_portfolio_value(username):
	""" Update the earnings on login
		
		Get the current value of each stock in the holdings table
		Get the product of the volume and current value of each stock in the holdings table
		Sum the products for all stocks and return the balance.
		
	"""
	#os.system('Clear')
	holdings = mapper.get_user_holdings(username)
	stock_values = []
	for record in holdings:
		ticker_symbol = record[0]
		number_of_shares = record[1]
		current_price = wrapper.get_last_price(ticker_symbol)
		current_value = int(number_of_shares) * float(current_price)
		stock_values.append(current_value)

	sum_of_stocks = (sum(stock_values))
	sum_of_stocks = "%0.2f" % sum_of_stocks
	
	return sum_of_stocks


def display_holdings_for_user(username):
	""" Return list of holdings for the given user."""
	
	holdings_record = mapper.get_user_holdings(username)

	ticker_symbols = []
	share_amounts = []
	purchase_prices = []
	last_prices = []
	for row in holdings_record:
		ticker_symbol = row[0]
		ticker_symbols.append(ticker_symbol)
		number_of_shares = row[1]
		share_amounts.append(number_of_shares)
		purchase_price = row[2]
		purchase_prices.append(purchase_price)
		last_price = wrapper.get_last_price(ticker_symbol)
		last_prices.append(last_price)
	

	#Organize accounts in dataframe
	data = [ticker_symbols, share_amounts, purchase_prices, last_prices]
	df = pd.DataFrame(data)
	if df.empty == True:
		print("\n","\nYou have not made any purchases.\n")
	else:
		df1 = df.transpose()
		df1.columns = ['Ticker Symbol', 'Volume', 'Purchase Price','Current Price']
		df1.set_index('Ticker Symbol')
		print("\n\n", df1.to_string(),"\n\n")
	

	next = input("1. Get ROI  2. Go Back to Main Menu")
	if next == str(1):
		get_portfolio_return(username)
		exit = input('\nPress enter to continue.')
	if next == 2:
		pass
	os.system('Clear')


def calculate_vwap(username, ticker_symbol):
	""" Return the vwap given a user and company."""
	### TODO: Do we need to remove sell transaction from the vwap calculation?
	try:
		transactions = mapper.get_transactions(username,ticker_symbol)
		volume = []
		for row in transactions:
			amount_purchased = row[1]
			volume.append(amount_purchased)

		last_amount = transactions[0][1]
		last_price = transactions[0][2]

		total_shares_bought = sum(volume)
		vwap = (last_amount * last_price) / total_shares_bought

		return vwap

	except Exception:
		vwap = 0.00 
		return vwap


# def get_ticker_symbol(company_name):
# 	""" Return ticker symbol given company name."""

# 	ticker_symbol = wrapper.get_ticker_symbol(company_name)
# 	else:
# 		pass


# 	return ticker_symbol


# def get_last_price(ticker_symbol):
# 	""" Return last price given the ticker symbol."""

# 	last_price = wrapper.get_last_price(ticker_symbol)
# 	else:
# 		pass
# 	return last_price


def display_balance(username):
	""" Return balance from users table."""
	balance = float(mapper.get_balance(username))
	#print("\nYour balance is: ", balance)

	return balance


def get_portfolio_return(username):
	""" Print ROI for given user."""
	holdings_record = mapper.get_user_holdings(username)

	ticker_symbols = []
	share_amounts = []
	purchase_prices = []
	last_prices = []
	rois = []

	price_changes = []

	for row in holdings_record:
		ticker_symbol = row[0]
		ticker_symbols.append(ticker_symbol)
		number_of_shares = row[1]
		share_amounts.append(number_of_shares)
		purchase_price = row[2]
		purchase_prices.append(purchase_price)
		last_price = wrapper.get_last_price(ticker_symbol)
		last_prices.append(last_price)

		price_difference = last_price - purchase_price
		price_changes.append(price_difference)
		roi = price_difference / purchase_price
		if price_difference ==0:
			roi = 0
		else: 
			roi = "%0.2f" % roi 
		rois.append(roi)

	#Organize accounts in dataframe
	data = [ticker_symbols, rois]
	df = pd.DataFrame(data)
	if df.empty == True:
		print("\n","\nYou have not made any purchases.\n")
	else:
		df1 = df.transpose()
		df1.columns = ['Ticker Symbol', 'ROI']
		df1.set_index('Ticker Symbol')
		print("\n\n", df1.to_string(),"\n\n")
	
	total_difference = sum(price_changes)
	return ("%.2f" % total_difference)


def calculate_profit_loss(username):
	""" Return profit/loss for given user."""

	holdings_record = mapper.get_user_holdings(username)

	share_amounts = []
	purchase_prices = []
	last_prices = []

	price_changes = []

	for row in holdings_record:
		ticker_symbol = row[0]
		number_of_shares = row[1]
		share_amounts.append(number_of_shares)
		purchase_price = row[2]
		purchase_prices.append(purchase_price)
		last_price = wrapper.get_last_price(ticker_symbol)
		last_prices.append(last_price)

		price_difference = (last_price - purchase_price) * number_of_shares
		price_changes.append(price_difference)


	total_difference = sum(price_changes)
	return ("%.2f" % total_difference)


def get_transactions(selection):
	""" Return transaction results for given selection."""

	if selection == "1":
		username = input("Enter username: ")
		transactions = mapper.get_transactions_by_user(username)
		return transactions
	if selection == "2":
		ticker_symbol = input("Enter ticker symbol: ")
		transactions = mapper.get_transactions_by_ticker_symbol(ticker_symbol)
		return transactions
	if selection == "3":
		date = input("Enter date: ") 
		transactions = mapper.get_transactions_by_date(date)
		return transactions
	if selection == "4":
		transactions = mapper.get_all_transactions()
		return transactions
	if selection == "5":
		pass


def get_holdings(selection):
	""" Return holdings results for given selection."""

	if selection == "1":
		username = input("Enter username: ")
		holdings = mapper.get_holdings_by_user(username)
		return holdings
	if selection == "2":
		ticker_symbol = input("Enter ticker symbol: ")
		holdings = mapper.get_holdings_by_ticker_symbol(ticker_symbol)
		return holdings
	if selection == "3":
		holdings = mapper.get_all_holdings()
		return holdings
	if selection == "4":
		pass

def get_current_user_holdings(username):
	""" Display holdings for the current user."""
	
	holdings = mapper.get_holdings_by_user(username)
	if not(holdings is None): 
		usernames = []
		ticker_symbols = []
		share_amounts = []
		purchase_prices = []
		portfolio_values = []
		vwaps = []

		for row in holdings:
			ticker_symbol= row[1]
			ticker_symbols.append(ticker_symbol)
			volume = row[2]
			share_amounts.append(volume)
			price = row[3]
			purchase_prices.append(price)
			vwap = row[4]
			vwaps.append(vwap)
			value = row[6]
			portfolio_values.append(value)
			username = row[5]
			usernames.append(username)
			
		#Organize accounts in dataframe
		data = [ticker_symbols, share_amounts, purchase_prices]
		df = pd.DataFrame(data)
		if df.empty == True:
			print("\n","\nThere are no items in your portfolio.\n")
		else:
			df1 = df.transpose()
			df1.columns = ['Ticker Symbol', 'Volume', 'Purchase Price']
			print("\n\nYour current holdings are:")
			print("\n", df1.to_string(),"\n\n")
		

	else:
		pass


def display_holdings(selection):
	""" Print all the holdings in the system."""

	holdings = get_holdings(selection)
	
	if not(holdings is None): 
		usernames = []
		ticker_symbols = []
		share_amounts = []
		purchase_prices = []
		portfolio_values = []
		vwaps = []

		for row in holdings:
			ticker_symbol= row[1]
			ticker_symbols.append(ticker_symbol)
			volume = row[2]
			share_amounts.append(volume)
			price = row[3]
			purchase_prices.append(price)
			vwap = row[4]
			vwaps.append(vwap)
			value = row[6]
			portfolio_values.append(value)
			username = row[5]
			usernames.append(username)
			
		#Organize accounts in dataframe
		data = [usernames, ticker_symbols, share_amounts, purchase_prices]
		df = pd.DataFrame(data)
		if df.empty == True:
			print("\n","\nThere are no portfolios.\n")
		else:
			df1 = df.transpose()
			df1.columns = ['Username', 'Ticker Symbol', 'Volume', 'Purchase Price']
			print("\n\n", df1.to_string(),"\n\n")
		
		exit = input("Press enter to return to main menu")

	else:
		pass
	

def display_transactions(selection):
	""" Print transaction results for given selection."""
	
	transactions = get_transactions(selection)

	if not(transactions is None): 


		usernames = []
		trans_dates = []
		trans_types = []
		ticker_symbols = []
		share_amounts = []
		purchase_prices = []

		for row in transactions:
			username = row[0]
			usernames.append(username)
			trans_date = row[1]
			trans_dates.append(trans_date)
			trans_type = row[2]
			trans_types.append(trans_type)
			ticker_symbol= row[3]
			ticker_symbols.append(ticker_symbol)
			volume = row[4]
			share_amounts.append(volume)
			price = row[5]
			purchase_prices.append(price)

		#Organize accounts in dataframe
		data = [usernames, trans_dates, trans_types, ticker_symbols, share_amounts, purchase_prices]
		df = pd.DataFrame(data)
		if df.empty == True:
			print("\n","\nThere are no transactions.\n")
		else:
			df1 = df.transpose()
			df1.columns = ['Username', 'Date', 'Type', 'Ticker Symbol', 'Volume', 'Price']
			df1.set_index('Ticker Symbol')
			print("\n\n", df1.to_string(index=False),"\n\n")
		
		exit = input("Press enter to return to main menu")

	else:
		pass
	

def display_users():
	""" Print all users non-admin userss."""
	
	users = mapper.get_users()
	usernames = []

	for row in users:
		username = row[0]
		usernames.append(username)


	#Organize accounts in dataframe
	data = [usernames]
	df = pd.DataFrame(data)
	if df.empty == True:
		print("\n","\nThere are no transactions.\n")
	else:
		df1 = df.transpose()
		df1.columns = ['Username']
		df1.set_index('Username')
		print("\n\n", df1.to_string(index=False),"\n\n")

	exit = input("Press enter to return to main menu")
	

def update_users(selection):
	""" Make an update to the users table given the selection."""
	if selection == "1":
		display_users()
	if selection == "2":
		username = input("Enter the username to update: ")
		new_username = input("Enter the new username: ")
		mapper.update_username(username, new_username)
	if selection == "3":
		username = input("Enter the username to update: ")
		new_password = input("Enter the new password: ")
		mapper.update_user_password(username, new_password)
	if selection == "4":
		username = input("Enter username for user to delete: ")
		verify_username = input("Reenter the username to delete: ")
		if username == verify_username:
			mapper.delete_user(username)
	if selection == "5":
		pass


def get_leaderboard_selection(selection):
	""" Return the leaderboard based on selection."""

	if selection == str(1):
		os.system('clear')
		print("\nTerminal Trader\n")
		print("\nLeaderboard\n")
		get_leaderboard_by_portfolio_value()
		exit = input("Press enter to continue to main menu..")
	if selection == str(2):
		os.system('clear')
		print("\nTerminal Trader\n")
		print("\nLeaderboard\n")
		get_leaderboard_by_profit_loss()
		exit = input("Press enter to continue to main menu..")

	else:
		pass
	



def get_leaderboard_by_portfolio_value():
	""" Displays the users by highest score.""" 

	leaders = []
	scores = []
	users = mapper.get_users()
	
	for row in users:
		user = row[0]
		leaders.append(user)
		portfolio_value = get_portfolio_value(user)
		portfolio_value = float(portfolio_value)
		scores.append(portfolio_value)

		
	#Organize accounts in dataframe
	data = [leaders, scores]
	df = pd.DataFrame(data)
	if df.empty == True:
		print("\n","\nNo leaders.\n")
	else:
		df1 = df.transpose()
		df1.columns = ['User','Score']
		df2 = df1.sort_values(by=['Score'],ascending=False)
		df2.shift()[1:]
		df3 = df2.head(10)
		df4 = df3.to_string(index=False).center(80)
		print("\n\n", df4,"\n\n")
	



def get_leaderboard_by_profit_loss():
	""" Displays the users by highest score.""" 

	leaders = []
	scores = []

	users = mapper.get_users()
	
	for row in users:
		user = row[0]
		leaders.append(user)
		scores.append(calculate_profit_loss(user))

		
	#Organize accounts in dataframe
	data = [leaders, scores]
	df = pd.DataFrame(data)
	if df.empty == True:
		print("\n","\nNo leaders.\n")
	else:
		df1 = df.transpose()
		df1.columns = ['User','Score']
		df2 = df1.sort_values(by=['Score'],ascending=False)
		df2.shift()[1:]
		df3 = df2.head(10)
		df4 = df3.to_string(index=False).center(80)
		print("\n\n", df4,"\n\n")
	



def make_dataframe(*arg):
	data = []
	for argument in arg:
		data.append(argument)

	df = pd.DataFrame(data)
	if df.empty == True:
		print("\n","\nNo data\n")
	else:
		df1 = df.transpose()
		for argument in arg:
			#TODO: Figure out how to assign column names
			df1.columns.append(argument)
		print("\n\n", df1.to_string(),"\n\n")


def login(username,password):
	""" Verify username matches password."""

	#username = input("\nEnter your username: ")
	#password = getpass.getpass("\nEnter your password: ")

	admin = check_for_admin(username,password)
	if admin == True:
		return admin,username 

	try: 
		stored_password = mapper.get_password(username)
		stored_password = stored_password[0][0]

	except Exception:
		login()


	if stored_password == password:
		pass
	else:
		login()

	return admin,username


def check_for_admin(username, password):
	users = mapper.get_admin(username)

	for user in users:
		admin_username = user[0]
		admin_password = user[1]

		if username == admin_username and admin_password == admin_password: 
			return True
			

def create_account():
	""" Create a new account. """

	username = input("\nEnter a username: ")
	password = getpass.getpass("\nEnter a password: ")
	usernames = mapper.get_username(username)

	if len(usernames) > 0:
		print("There is already an account with that name.")
		username = input("Enter a different username: ")
	else: 
		pass
		

	balance = 10000.00
	try:
		mapper.add_user(username,password,balance)
		print("New user created successfully")
		return username
	except Exception:
		print("There was an error creating the user account")

 

if __name__ == '__main__':
	#get_leaderboard()
	#login()
	#get_price_by_company("Facebook")
	print(get_portfolio_return('lindsayminnock'))