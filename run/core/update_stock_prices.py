
import json
import sqlite3
import datetime 

import requests 



def update_stock_prices():

	stocks = get_stocks()

	for stock in stocks:
		stock = stock[0]
		print(stock)

		last_price = get_last_price(stock)
		print(last_price)
		try:
			update_prices(stock,last_price)
		except Exception:
			try:
				insert_prices(last_price, stock)
			except Exception:
				print("Stock {0} could not be updated.".format(stock))




def get_stocks():
	connection = sqlite3.connect('master.db',check_same_thread=False)
	cursor = connection.cursor()
	cursor.execute("SELECT DISTINCT ticker_symbol FROM holdings;")
	stocks = cursor.fetchall()
	connection.commit()
	cursor.close()
	connection.close()

	return stocks
	


def get_last_price(ticker_symbol):
    """ Return the most recent price of a stock given the ticker symbol."""
    try:
        endpoint = 'http://dev.markitondemand.com/MODApis/Api/v2/Quote/json?symbol='+ ticker_symbol
        response = json.loads(requests.get(endpoint).text)
        last_price = response['LastPrice']
        return last_price 
    except Exception: 
        #print("\nThere are no results for {0}".format(ticker_symbol))
        return False 


def insert_prices(last_price, ticker_symbol):

	last_updated = datetime.datetime.now()
	connection = sqlite3.connect('master.db',check_same_thread=False)
	cursor = connection.cursor()

	cursor.execute("INSERT INTO stocks(ticker_symbol,stock_price,last_update) VALUES('{0}',{1},'{2}');".format(ticker_symbol,last_price,last_updated))
	connection.commit()
	cursor.close()
	connection.close()

def update_prices(ticker_symbol,last_price):

	last_updated = datetime.datetime.now()
	connection = sqlite3.connect('master.db',check_same_thread=False)
	cursor = connection.cursor()
	cursor.execute("UPDATE stocks SET stock_price={1},last_update='{2}' WHERE ticker_symbol='{0}');".format(ticker_symbol,last_price,last_updated))
	connection.commit()
	cursor.close()
	connection.close()


if __name__ == '__main__':
	update_stock_prices()
    