#!/usr/bin/env python3

import sqlite3

connection = sqlite3.connect('master.db', check_same_thread=False)
cursor = connection.cursor()

# Users
cursor.execute(
	"""CREATE TABLE IF NOT EXISTS users(
		pk INTEGER PRIMARY KEY AUTOINCREMENT,
		username VARCHAR(16),
		password VARCHAR(32),
		balance FLOAT
	);"""
)

# Admins
cursor.execute(
	"""CREATE TABLE IF NOT EXISTS admins(
		pk INTEGER PRIMARY KEY AUTOINCREMENT,
		username VARCHAR(16),
		password VARCHAR(32)
	);"""
)

# Portfolio 
cursor.execute(
	""" CREATE TABLE IF NOT EXISTS holdings(
		pk INTEGER PRIMARY KEY AUTOINCREMENT,
		ticker_symbol VARCHAR,
		number_of_shares INTEGER, 
		purchase_price FLOAT,
		volume_weighted_average_price FLOAT,
		portfolio_value FLOAT,
		username TEXT
	);"""
)

# Orders
cursor.execute(
	"""CREATE TABLE IF NOT EXISTS orders(
		pk INTEGER PRIMARY KEY AUTOINCREMENT,
		unix_time FLOAT,
		transaction_type BOOL,
		last_price FLOAT,
		trade_volume INTEGER
	);"""
)

# Transactions

cursor.execute(
	"""CREATE TABLE IF NOT EXISTS transactions(
	trans_date TEXT,
	trans_type TEXT,
	ticker_symbol TEXT,
	volume INTEGER,
	stock_price REAL,
	total_amount REAL,
	username TEXT
	);"""
)


connection.commit()
cursor.close()
connection.close() 