
import json

import requests 

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