#!/usr/bin/env python3

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

def get_ticker_symbol(company_name):
    """ Return the ticker symbol of the given company name."""
    try:
        endpoint = 'http://dev.markitondemand.com/MODApis/Api/v2/Lookup/json?input=' + company_name
        response = json.loads(requests.get(endpoint).text)[0]
        ticker_symbol = response['Symbol']
        return ticker_symbol 
    except Exception:
        print("There are not results for {0}".format(company_name))
        return False
