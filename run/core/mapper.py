#!/usr/bin/env python3

import sqlite3

from core import model


def add_new_user(username,email,password,country,gender):
    """Insert new user account into users table."""

    connection, cursor = connect_db()
    cursor.execute("""INSERT INTO users(username,
                            email,
                            password,
                            balance,
                            country,
                            gender) VALUES(
                            '{username}',
                            '{email}',
                            '{password}',
                            {balance},
                            '{country}',
                            '{gender}');""".format(
                                username=username,
                                email=email,
                                password=password,
                                balance=10000,
                                country=country,
                                gender=gender
                                ))
    disconnect_db(connection,cursor)



def get_holdings_record(username, ticker_symbol):
    """ Return a record for the given company from the holdings table."""

    connection, cursor = connect_db()
    cursor.execute("""SELECT ticker_symbol, 
                    number_of_shares 
                    FROM holdings 
                    WHERE ticker_symbol='{0}' 
                    AND username='{1}';""".format(ticker_symbol, username))
                    
    holdings_record = cursor.fetchall()
    disconnect_db(connection,cursor)

    return holdings_record



def get_user_holdings(username):
    """ Return all records for the current user from the holdings table."""

    connection, cursor = connect_db()
    cursor.execute("""SELECT ticker_symbol, 
                    number_of_shares,
                    purchase_price
                    FROM holdings
                    WHERE username='{0}' AND number_of_shares > 0;""".format(username))
    holdings_record = cursor.fetchall()
    disconnect_db(connection,cursor)

    return holdings_record


def add_holdings_record(ticker_symbol,trade_volume,purchase_price,username):
    """ Insert new record into holding table.

        Assumes there is no existing record for the stock for the given user.
    """

    connection, cursor = connect_db()
    cursor.execute("""INSERT INTO holdings(ticker_symbol,
                            number_of_shares,
                            purchase_price,
                            username) VALUES(
                            '{ticker_symbol}',
                            {trade_volume},
                            {purchase_price},
                            '{username}');""".format(
                                ticker_symbol=ticker_symbol,
                                trade_volume=trade_volume,
                                purchase_price=purchase_price,
                                username=username))
    disconnect_db(connection,cursor)


# def update_holdings_record(username,ticker_symbol,trade_volume,purchase_price):
#     """ Update a record in the holdings table for given user name an company. """

#     connection, cursor = connection, cursor = connect_db()
#     cursor.execute("""UPDATE holdings SET number_of_shares={trade_volume},
#                         purchase_price={purchase_price},
#                         WHERE ticker_symbol='{ticker_symbol}'
#                         AND username='{username}';""".format(
#                             trade_volume=trade_volume,
#                             ticker_symbol=ticker_symbol,
#                             username=username,
#                             purchase_price=purchase_price))
#     disconnect_db(connection,cursor)


def update_holdings_record(username,ticker_symbol,trade_volume,purchase_price,vwap):
    """ Update a record in the holdings table for given user name an company. """

    connection, cursor = connection, cursor = connect_db()
    cursor.execute("""UPDATE holdings SET number_of_shares={trade_volume},
                        purchase_price={purchase_price},
                        volume_weighted_average_price={vwap}
                        WHERE ticker_symbol='{ticker_symbol}'
                        AND username='{username}';""".format(
                            trade_volume=trade_volume,
                            ticker_symbol=ticker_symbol,
                            username=username,
                            purchase_price=purchase_price,
                            vwap=vwap))
    disconnect_db(connection,cursor)


def get_transactions(username,ticker_symbol):
    """ Return transactions for a given user and company."""

    connection, cursor = connect_db()
    cursor.execute("""SELECT trans_date, 
                            volume, 
                            stock_price 
                            FROM transactions 
                            WHERE username='{0}' 
                            and ticker_symbol='{1}' 
                            ORDER BY trans_date DESC;""".format(
                                username, 
                                ticker_symbol))
    transactions = cursor.fetchall()
    disconnect_db(connection,cursor)

    return transactions


def get_all_transactions():
    """ Return all transactions."""

    connection, cursor = connect_db()
    cursor.execute("""SELECT username,
                            trans_date,
                            ticker_symbol, 
                            trans_type,
                            volume, 
                            stock_price 
                            FROM transactions 
                            ORDER BY trans_date DESC;""")
    transactions = cursor.fetchall()
    disconnect_db(connection,cursor)

    return transactions


def get_transactions_by_user(username):
    """ Return transactions for a given user."""
    
    connection, cursor = connect_db()
    cursor.execute("""SELECT username,
                            trans_date,
                            ticker_symbol,
                            trans_type, 
                            volume, 
                            stock_price,
                            portfolio_value
                            FROM transactions 
                            WHERE username='{0}'  
                            ORDER BY trans_date DESC;""".format(
                                username))
    transactions = cursor.fetchall()
    disconnect_db(connection,cursor)

    return transactions


def get_transactions_by_ticker_symbol(ticker_symbol):
    """ Return transactions for a given ticker_symbol."""

    connection, cursor = connect_db()
    cursor.execute("""SELECT username,
                            trans_date,
                            ticker_symbol,
                            trans_type, 
                            volume, 
                            stock_price
                            FROM transactions 
                            WHERE ticker_symbol='{0}'  
                            ORDER BY trans_date DESC;""".format(
                                ticker_symbol))
    transactions = cursor.fetchall()
    disconnect_db(connection,cursor)

    return transactions


def get_transactions_by_date(date):
    """ Return transactions for a given ticker_symbol."""

    connection, cursor = connect_db()
    cursor.execute("""SELECT username,
                            trans_date,
                            ticker_symbol,
                            trans_type, 
                            volume, 
                            stock_price 
                            FROM transactions 
                            WHERE trans_date LIKE '%{0}%'  
                            ORDER BY trans_date DESC;""".format(
                                date))
    transactions = cursor.fetchall()
    disconnect_db(connection,cursor)

    return transactions


def add_transaction(username,trans_date,trans_type,ticker_symbol,volume,stock_price,total_amount,new_balance):
    """ Insert a new record into the transaction table."""

    connection, cursor = connect_db()
    cursor.execute("""INSERT INTO transactions(
                        trans_date,
                        trans_type,
                        ticker_symbol,
                        volume,
                        stock_price,
                        total_amount,
                        username,
                        portfolio_value) VALUES(
						'{trans_date}', 
                        '{trans_type}',
                        '{ticker_symbol}',
                        {volume},
                        {stock_price},
                        {total_amount},
                        '{username}',
                        {new_balance});""".format(trans_date=trans_date,
                            trans_type=trans_type,
                            ticker_symbol=ticker_symbol,
                            volume=volume,
                            stock_price=stock_price,
                            total_amount=total_amount,
                            username=username,
                            new_balance=new_balance))
    disconnect_db(connection,cursor)


def get_all_holdings():
    """ Return all holdings in the system."""

    connection, cursor = connect_db()
    cursor.execute("SELECT * FROM holdings ORDER BY username ASC")
    holdings = cursor.fetchall()
    disconnect_db(connection,cursor)

    return holdings



def get_holdings_by_user(username):
    """ Return holdings for the given user."""

    connection, cursor = connect_db()
    cursor.execute("SELECT * FROM holdings WHERE username='{0}'".format(username))
    holdings = cursor.fetchall()
    disconnect_db(connection,cursor)

    return holdings


def get_holdings_by_ticker_symbol(ticker_symbol):
    """ Return holdings for a given ticker symbol."""

    connection, cursor = connect_db()
    cursor.execute("SELECT * FROM holdings WHERE ticker_symbol='{0}'".format(ticker_symbol))
    holdings = cursor.fetchall()
    disconnect_db(connection,cursor)

    return holdings


def get_balance(username):
	""" Reuturn the current balance for the user."""
	try:
		connection, cursor = connect_db()
		cursor.execute("SELECT balance FROM users WHERE username='{username}';".format(username=username))
		user_balance = cursor.fetchall()[0][0]
		user_balance = "%0.2f" % user_balance
		disconnect_db(connection,cursor)
	
		if user_balance is None:
			user_balance = 10000

		return user_balance 

	except Exception:
		print("There was an error fetching the balance")


def update_balance(username, new_balance):
    """ Update the balance in the users table."""

    connection, cursor = connect_db()
    cursor.execute("UPDATE users SET balance = {0} WHERE username='{1}';".format(new_balance,username))
    disconnect_db(connection,cursor)


def get_password(username):
    """ Return the password for the given user from the users table."""

    connection, cursor = connect_db()
    cursor.execute("SELECT password FROM users WHERE email='{username}';".format(username=username))
    password = cursor.fetchall()
    disconnect_db(connection,cursor)

    return password


def get_username(username):
    """ Check if there is already an account with that username."""

    connection, cursor = connect_db()
    cursor.execute("SELECT * FROM users WHERE username='{username}';".format(username=username))
    username = cursor.fetchall()
    disconnect_db(connection,cursor)

    return username


def get_email(email):
    """ Check if there is already an account with that email."""

    connection, cursor = connect_db()
    cursor.execute("SELECT * FROM users WHERE email='{email}';".format(email=email))
    username = cursor.fetchall()
    disconnect_db(connection,cursor)

    return username


def get_users():
    """ Returns all users in the table."""
    
    connection, cursor = connect_db()
    cursor.execute("SELECT username FROM users;")
    usernames = cursor.fetchall()
    disconnect_db(connection,cursor)

    return usernames


def get_username(email):
    """ Returns username for a user given the login email."""
    
    connection, cursor = connect_db()
    cursor.execute("SELECT username FROM users where email='{email}';".format(email=email))
    username = cursor.fetchall()
    disconnect_db(connection,cursor)

    return username


def add_user(username, password, balance):
    """ Insert row into users table."""

    connection, cursor = connect_db()
    cursor.execute("INSERT INTO users(username, password, balance) VALUES('{username}', '{password}', {balance});".format(username=username,password=password,balance=balance))
    disconnect_db(connection,cursor)


def delete_user(username):
    """ Delete the given user from the relevant tables."""

    connection, cursor = connect_db()
    cursor.execute("DELETE FROM users where username='{0}';".format(username))
    cursor.execute("DELETE FROM holdings where username='{0}';".format(username))
    cursor.execute("DELETE FROM transactions where username='{0}';".format(username))

    disconnect_db(connection,cursor)


def update_user_password(username, new_password):
    """ Update the password of a given user."""

    connection, cursor = connect_db()
    cursor.execute("UPDATE users SET password='{0}' WHERE username='{1}';".format(new_password,username))
    disconnect_db(connection,cursor)
    

def update_username(username, new_username):
    """ Update the username of a given user in all relevant tables."""

    connection, cursor = connect_db()
    cursor.execute("UPDATE users SET username='{0}' WHERE username='{1}';".format(new_username,username))
    cursor.execute("UPDATE holdings SET username='{0}' WHERE username='{1}';".format(new_username,username))
    cursor.execute("UPDATE transactions SET username='{0}' WHERE username='{1}';".format(new_username,username))
    disconnect_db(connection,cursor)




def get_admin(username):
    """ Return list of amdmin users."""
     
    connection, cursor = connect_db()
    cursor.execute("SELECT username, password FROM admins WHERE username='{username}'".format(username=username))
    usernames = cursor.fetchall()
    disconnect_db(connection,cursor)

    return usernames


def connect_db():
    """ Connect to the master database."""
    
    connection = sqlite3.connect('run/core/master.db',check_same_thread=False)
    cursor = connection.cursor()
    return connection, cursor


def disconnect_db(connection,cursor):
    """ Connect to the master database."""
    
    connection.commit()
    cursor.close()
    connection.close()
    

if __name__ == '__main__':
    pass