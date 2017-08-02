#!/usr/bin/env python

################################################################################
# file      login.py
#           This script handles requests related to login from web gui
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
import smtplib

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

login_app = Blueprint('login_app', __name__)

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

@login_app.route('/login_verify_credentials',methods=['GET','POST'])
def login_verify_credentials():
    result={'result':False}
    try:
        username = request.args.get('username')
        password = request.args.get('password')

        db_user = db.db_get_user(username)
        for row in db_user:
            if len(row) != 0:
                db_username = row[0]
                db_password = row[1]
                break
        if db_username == username and db_password == password:
            result['result'] = True
    except:
        print str(traceback.format_exc())
        print "Credentials incorrect"
        result['result'] = False
    return jsonify(result)


@login_app.route('/forgot_password',methods=['GET','POST'])
def forgot_password():
    result={'result':False}
    try:
        user_db = db.db_get_user('admin')
        for row in user_db:
            if len(row) != 0:
                username_db = row[0]
                password_db = row[1]
                firstname = row[2]
                lastname = row[3]
                email_db = row[4]
                break
        gmail_user = 'testingowb@gmail.com'
        gmail_password = 'abcd1234@'
        send_to = email_db

        SUBJECT = "Forgot Password"

        line_start = "Hi " + firstname + " " + lastname + "," + "\n" + "\n" + "Your Credentials are as follows: " +"\n" + "\n" + "------------------" + "\n"
        username = "User Name: " + username_db + "\n"
        password = "Password: " + password_db + "\n"
        line_end = "------------------" + "\n" + "\n" + "Sincerely," + "\n" + "Lumenux" + "\n"

        body = line_start + username + password + line_end
        mail_text = 'Subject: {}\n\n{}'.format(SUBJECT, body)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, send_to, mail_text)
        server.close()
    except:
        print str(traceback.format_exc())
        result['result'] = False
    return jsonify(result)
################################################################################
# script
################################################################################

# none

################################################################################
# end of file
################################################################################
