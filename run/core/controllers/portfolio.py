#!/usr/bin/env python3

from flask import Blueprint, render_template, request

from core import model 


controller = Blueprint('portfolio',__name__,url_prefix='/portfolio')

@controller.route('/',methods=['GET'])
def show_portfolio():
	if request.method == 'GET':
		return render_template('portfolio.html')
	else:
		return render_template('portfolio.html')

