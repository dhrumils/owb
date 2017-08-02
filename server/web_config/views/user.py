#!/usr/bin/env python

################################################################################
# file      user.py
#           This script handles requests related to user from web gui
#
# author    Glide Technology Pvt. Ltd. <www.glidemtech.com>
# version   1.0
# date      29, Jul, 2017
################################################################################

################################################################################
# dependencies
################################################################################

import os
from flask import Flask, jsonify, request, Blueprint
from . import db
import traceback

################################################################################
# constants
################################################################################

# none

################################################################################
# private variables
################################################################################

# none

################################################################################
# public variables
################################################################################

user_app = Blueprint('user_app', __name__)

################################################################################
# private classes
################################################################################

# none

################################################################################
# public classes
################################################################################

# none

################################################################################
# private methods
################################################################################

#none

################################################################################
# public methods
################################################################################

@user_app.route('/user_save_details', methods=['GET', 'POST'])
def user_save_details():
    result={'result':False}
    try:
        firstname = request.args.get('firstname')
        lastname = request.args.get('lastname')
        emailid = request.args.get('emailid')

        db.db_update_user('admin','firstname',firstname)
        db.db_update_user('admin','lastname',lastname)
        db.db_update_user('admin','emailid',emailid)
        result['result'] = True
    except:
        print "Coulnt save info"
        result['result'] = False
    return jsonify(result)

################################################################################

@user_app.route('/user_save_credentials', methods=['GET', 'POST'])
def user_save_credentials():
    result={'result':False}
    try:
        pwd = db.db_get_user('admin')
        presentpwd = request.args.get('cuurent_password')
        newpwd = request.args.get('new_password')
        db_pwd=None
        for row in pwd:
            if len(row) != 0:
                db_pwd=row[1]
                break
        if db_pwd == presentpwd:
            db.db_update_user('admin', 'password', newpwd)
            result['result'] = True
        else:
            print "Present password incorrect"
    except:
        print str(traceback.format_exc())
        print "coulnt save info"
        result['result'] = False
    return jsonify(result)

################################################################################
# script
################################################################################

# none

################################################################################
# end of file
################################################################################
