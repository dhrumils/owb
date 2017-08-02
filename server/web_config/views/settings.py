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

Gateway_UPLOAD_DIR = 'server/web_config/static/upload/gateway/'
PDM_UPLOAD_DIR = 'server/web_config/static/upload/pdm/'

################################################################################
# private variables
################################################################################

# none

################################################################################
# public variables
################################################################################

settings_app = Blueprint('settings_app', __name__)

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

@settings_app.route('/get_memory_usage_gateway', methods=['GET', 'POST'])
def get_memory_usage_gateway():
    try:
        memory_usage_gateway = 0
        for dirpath, dirnames, filenames in os.walk(Gateway_UPLOAD_DIR):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                memory_usage_gateway += os.path.getsize(fp)
            print memory_usage_gateway
        return jsonify(memory_usage_gateway)
    except:
        print str(traceback.format_exc())
    return jsonify(memory_usage_gateway)

@settings_app.route('/get_memory_usage_pdm', methods=['GET', 'POST'])
def get_memory_usage_pdm():
    result={'result':False}
    try:
        memory_usage_pdm= 0
        for dirpath, dirnames, filenames in os.walk(PDM_UPLOAD_DIR):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                memory_usage_pdm += os.path.getsize(fp)
            print memory_usage_pdm
        return jsonify(memory_usage_pdm)
    except:
        print str(traceback.format_exc())
    return jsonify(memory_usage_pdm)

################################################################################
# script
################################################################################

# none

################################################################################
# end of file
################################################################################
