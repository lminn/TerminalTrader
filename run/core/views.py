#!/usr/bin/env python3

import os

import model


def display_header(page):
	os.system('clear')
	print('\nTerminal Trader\n')
	print('\n {0} \n'.format(page))

def start_menu():
	display_header("")
	start = input("\n1. Login 2. Create Account\n")
	return start

def main_menu():
	display_header("Main Menu")
	user_input = input('\n1. Buy  \n2. Sell  \n3. Lookup Company  \n4. Quote  \n5. Portfolio  \n6. Exit \n')
	return user_input

def buy_menu():
	display_header("Buy")
	ticker_symbol = input("Ticker Symbol: ")
	trade_volume = input("Trade volume: ")
	return ticker_symbol, trade_volume

def sell_menu():
	display_header("Sell")
	ticker_symbol = input("Ticker Symbol: ")
	trade_volume = input("Trade volume: ")
	return ticker_symbol, trade_volume

def lookup_menu():
	display_header("Lookup")
	company_name = input('Company Name: ')
	return company_name

def quote_menu():
	display_header("Quote")
	ticker_symbol = input('Ticker Symbol: ')
	return ticker_symbol 

def portfolio_menu():
	display_header("Portfolio")

def admin_main_menu():
	display_header("Admin")
	user_input = input('\n1. View Leaderboard \n2. Users  \n3. Holdings  \n4. Transactions   \n5. Exit \n')
	return user_input
	
def users_menu():
	display_header("Users")
	user_input = input('\n1. View All Users   \n2. Update Username \n3. Update Password \n4. Delete User  \n5. Back to Main Menu \n')
	return user_input

def portfolios_menu():
	display_header("Holdings")
	user_input = input("""\n1. Search by User  \n2. Search by Ticker Symbol    \n3. View All Holdings  \n4. Back to Main Menu\n""")
	return user_input
	
def transactions_menu():
	display_header('Transactions')
	user_input = input("""\n1. Search by User  \n2. Search by Ticker Symbol  \n3. Search by Date   \n4. View All Transactions \n5. Back to Main Menu\n""")
	return user_input

def leader_board(): 
	os.system('clear')
	print('\nTerminal Trader\n')
	print('\nLeadboard\n')
	user_input = input("\n1. Highest Portfolio Value \n2. Highest Profit\n")
	return user_input

def exit_message():
	return 'Thanks for playing!'


if __name__ == '__main__':
	print(sell_menu())