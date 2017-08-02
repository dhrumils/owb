#!/usr/bin/env python

################################################################################
# file      web_cfg.py
#           This script provides functions for web gui config
#
# author    Glide Technology Pvt. Ltd. <www.glidemtech.com>
# version   1.0
# date      29, Jul, 2017
################################################################################

################################################################################
# dependencies
################################################################################

from flask import Flask, jsonify, render_template, request, redirect, url_for, Blueprint
from . import webcfg
from .. import database

################################################################################
# constants
################################################################################

#none

################################################################################
# private variables
################################################################################

# none

################################################################################
# public variables
################################################################################

#none

################################################################################
# private classes
################################################################################

# none

################################################################################
# public classes
################################################################################

#none

################################################################################
# private methods
################################################################################

#none

################################################################################
# public methods
################################################################################

@webcfg.route('/')
def index():
    return redirect('static/webpages/login.html')

################################################################################
# script
################################################################################

# none

################################################################################
# end of file
################################################################################
