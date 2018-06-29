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
        #print("There are not results for {0}".format(company_name))
        return False


def get_time_series(ticker_symbol):
    """ Return the ticker symbol of the given company name."""
    try:
        endpoint = 'http://dev.markitondemand.com/MODApis/Api/Timeseries/json?symbol=' + ticker_symbol
        response = json.loads(requests.get(endpoint).text)
        ticker_symbol = response['Data']['Symbol']
        open_prices = response['Data']['Series']['close']['values']
        labels = response['Data']['SeriesLabels']['x']['text']
        return [ticker_symbol, open_prices, labels]
    except Exception:
        #print("There are not results for {0}".format(company_name))
        return False


def get_company_details(ticker_symbol):
        endpoint = 'http://dev.markitondemand.com/MODApis/Api/v2/Quote/json?symbol='+ ticker_symbol
        response = json.loads(requests.get(endpoint).text)
        name = response['Name']
        symbol = response['Symbol']
        change = response['Change']
        changePercent = response['ChangePercent']
        market_cap = response['MarketCap']
        changeYTD = response['ChangeYTD']
        changePercentYTD = response['ChangePercentYTD']
        last_price = response['LastPrice']
        high = response['High']
        low = response['Low']
        open_price = response['Open']
        volume = response['Volume']

        company_details = [name, symbol, change, changePercent, market_cap, changeYTD, changePercentYTD, last_price, high, low, open_price, volume]

        return company_details 


def get_company_name(ticker_symbol):
    """ Return the company name for the given ticker symbol"""
    try:
        endpoint = 'http://dev.markitondemand.com/MODApis/Api/v2/Quote/json?input=' + ticker_symbol
        response = json.loads(requests.get(endpoint).text)[0]
        name = response['Name']
        return name
    except Exception:
        return False

def get_change(ticker_symbol):
    """ Return the change of price for a stock given a ticker symbol."""
    try:
        endpoint = 'http://dev.markitondemand.com/MODApis/Api/v2/Quote/json?symbol=' + ticker_symbol
        response = json.loads(requests.get(endpoint).text)[0]
        change = response['Change']
        return change 
    except Exception:
        #print("There are not results for {0}".format(company_name))
        return False

def get_change_percent(ticker_symbol):
    """ Return the change percent of a stock given the ticker symbol."""
    try:
        endpoint = 'http://dev.markitondemand.com/MODApis/Api/v2/Quote/json?input=' + ticker_symbol
        response = json.loads(requests.get(endpoint).text)[0]
        ticker_symbol = response['ChangePercent']
        return ticker_symbol 
    except Exception:
        #print("There are not results for {0}".format(company_name))
        return False

def get_market_cap(ticker_symbol):
    """ Return the market cap of a stock given the ticker symbol."""
    try:
        endpoint = 'http://dev.markitondemand.com/MODApis/Api/v2/Quote/json?input=' + ticker_symbol
        response = json.loads(requests.get(endpoint).text)[0]
        market_cap = response['MarketCap']
        return market_cap 
    except Exception:
        #print("There are not results for {0}".format(company_name))
        return False



def get_market_cap(ticker_symbol):
    """ Return the change YTD of a stock given the ticker symbol."""
    try:
        endpoint = 'http://dev.markitondemand.com/MODApis/Api/v2/Quote/json?input=' + ticker_symbol
        response = json.loads(requests.get(endpoint).text)[0]
        changeYTD = response['ChangeYTD']
        return changeYTD
    except Exception:
        #print("There are not results for {0}".format(company_name))
        return False

def get_change_percentYTD(ticker_symbol):
    """ Return the change YTD of a stock given the ticker symbol."""
    try:
        endpoint = 'http://dev.markitondemand.com/MODApis/Api/v2/Quote/json?input=' + ticker_symbol
        response = json.loads(requests.get(endpoint).text)[0]
        change_percentYTD = response['ChangePercentYTD']
        return change_precentYTD
    except Exception:
        #print("There are not results for {0}".format(company_name))
        return False


def get_change_percentYTD(ticker_symbol):
    """ Return the change YTD of a stock given the ticker symbol."""
    try:
        endpoint = 'http://dev.markitondemand.com/MODApis/Api/v2/Quote/json?input=' + ticker_symbol
        response = json.loads(requests.get(endpoint).text)[0]
        change_percentYTD = response['ChangePercentYTD']
        return change_precentYTD
    except Exception:
        #print("There are not results for {0}".format(company_name))
        return False


def get_change_percentYTD(ticker_symbol):
    """ Return the change YTD of a stock given the ticker symbol."""
    try:
        endpoint = 'http://dev.markitondemand.com/MODApis/Api/v2/Quote/json?input=' + ticker_symbol
        response = json.loads(requests.get(endpoint).text)[0]
        change_percentYTD = response['ChangePercentYTD']
        return change_precentYTD
    except Exception:
        #print("There are not results for {0}".format(company_name))
        return False


def get_high(ticker_symbol):
    """ Return the high of a stock given the ticker symbol."""
    try:
        endpoint = 'http://dev.markitondemand.com/MODApis/Api/v2/Quote/json?input=' + ticker_symbol
        response = json.loads(requests.get(endpoint).text)[0]
        high = response['High']
        return high
    except Exception:
        #print("There are not results for {0}".format(company_name))
        return False


def get_low(ticker_symbol):
    """ Return the low of a stock given the ticker symbol."""
    try:
        endpoint = 'http://dev.markitondemand.com/MODApis/Api/v2/Quote/json?input=' + ticker_symbol
        response = json.loads(requests.get(endpoint).text)[0]
        low = response['Low']
        return high
    except Exception:
        #print("There are not results for {0}".format(company_name))
        return False


def get_open(ticker_symbol):
    """ Return the low of a stock given the ticker symbol."""
    try:
        endpoint = 'http://dev.markitondemand.com/MODApis/Api/v2/Quote/json?input=' + ticker_symbol
        response = json.loads(requests.get(endpoint).text)[0]
        open = response['Open']
        return high
    except Exception:
        #print("There are not results for {0}".format(company_name))
        return False


if __name__ == '__main__':

    print(get_time_series('tsla'))

