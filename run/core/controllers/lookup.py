#!/usr/bin/env python3

from flask import Blueprint, render_template, request

from core import model 


controller = Blueprint('lookup',__name__,url_prefix='/lookup')

@controller.route('/',methods=['GET'])
def show_lookup():
	if request.method == 'GET':
		return render_template('lookup.html')
	else:
		return render_template('lookup.html')

