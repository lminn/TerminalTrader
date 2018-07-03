#!/usr/bin/env python3

from flask import Blueprint, render_template, request, g, session


controller = Blueprint('logout',__name__,url_prefix='/logout')


@controller.route('/',methods=['GET'])
def logout():
	session.pop('user', None)
	return render_template('login.html')

