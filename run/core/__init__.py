#!/usr/bin/env python3

import os

from flask import Flask

from core.controllers.featured import controller as featured
from core.controllers.general import controller as general
from core.controllers.portfolio import controller as portfolio
from core.controllers.buy import controller as buy
from core.controllers.sell import controller as sell
from core.controllers.lookup import controller as lookup
from core.controllers.dashboard import controller as dashboard
from core.controllers.logout import controller as logout
from core.controllers.register import controller as register



def keymaker(omnibus,filename='secret_key'):
    pathname = os.path.join(omnibus.instance_path,filename)
    try:
        print('I\'m trying to find a directory labelled instance...')
        print('I\'m trying to find a file labelled secret_key...')
        omnibus.config['SECRET_KEY'] = open(pathname,'rb').read()
        print('I found a directory labelled instance,,')
        print('I found a file labelled secret_key...')

    except IOError:
        parent_directory = os.path.dirname(pathname)
        if not os.path.isdir(parent_directory):
            print('I can\'t find a directory labelled instance...')
            print('I\'m making a directory labelled instance...')
            os.system('mkdir -p {}'.format(parent_directory))
        print('I\'m writing to a file labelled secret_key')
        os.system('head -c 24 /dev/urandom > {}'.format(pathname))
        omnibus.config['SECRET_KEY'] = open(pathname,'rb').read()


omnibus = Flask(__name__)

omnibus.register_blueprint(featured)
omnibus.register_blueprint(general)
omnibus.register_blueprint(portfolio)
omnibus.register_blueprint(buy)
omnibus.register_blueprint(sell)
omnibus.register_blueprint(lookup)
omnibus.register_blueprint(dashboard)
omnibus.register_blueprint(logout)
omnibus.register_blueprint(register)





# TODO Write the following function
keymaker(omnibus)
