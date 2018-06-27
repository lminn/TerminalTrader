#!/usr/bin/env python3

from flask import Blueprint, render_template, request

from core import model 


controller = Blueprint('buy',__name__,url_prefix='/buy')

@controller.route('/',methods=['GET'])
def show_buy():
	if request.method == 'GET':
		return render_template('buy.html')
	else:
		return render_template('buy.html')

