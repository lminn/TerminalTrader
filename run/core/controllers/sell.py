#!/usr/bin/env python3

from flask import Blueprint, render_template, request

from core import model 


controller = Blueprint('sell',__name__,url_prefix='/sell')

@controller.route('/',methods=['GET'])
def show_sell():
	if request.method == 'GET':
		return render_template('sell.html')
	else:
		return render_template('sell.html')

