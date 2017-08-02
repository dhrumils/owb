#!/usr/bin/env python

################################################################################
# file      gateway.py
#           This script handles requests related to gateway from web gui
#
# author    Glide Technology Pvt. Ltd. <www.glidemtech.com>
# version   1.0
# date      29, Jul, 2017
################################################################################

################################################################################
# dependencies
################################################################################
import os
import glob
import ntpath
import time
import json
import zipfile
import MySQLdb
from flask import Flask, jsonify, render_template, request, redirect, url_for, send_from_directory, Blueprint, Response
from werkzeug.utils import secure_filename
from datetime import datetime
from . import db
import traceback


################################################################################
# constants
################################################################################

ALLOWED_EXTENSIONS = set(['zip'])
GATEWAY_UPLOAD_DIR = 'server/web_config/static/upload/gateway/'

################################################################################
# private variables
################################################################################

# none

################################################################################
# public variables
################################################################################

gateway_app = Blueprint('gateway_app', __name__)

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
def _gw_get_file_info(filename):
    try:
        json_decode={}
        gateway_schema = db.db_gateway_schema()
        zf=zipfile.ZipFile(filename, 'r')
        for file in zf.namelist():
            if file == "file_info.json":
                json_decode=json.loads(zf.read(file))
                gateway_schema['filename'] = json_decode.get('filename')
                gateway_schema['major_version'] = json_decode.get('major_version')
                gateway_schema['minor_version'] = json_decode.get('minor_version')
                gateway_schema['modified_date'] = json_decode.get('modified_date')
                gateway_schema['commit_number'] = json_decode.get('commit_number')
                gateway_schema['commit_date'] = json_decode.get('commit_date')
                gateway_schema['remarks'] = json_decode.get('remarks')
                gateway_schema['latest'] = json_decode.get('latest')
    except:
        print str(traceback.format_exc())
    return gateway_schema

################################################################################

def _gw_verify_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

################################################################################
# public methods
################################################################################
@gateway_app.route('/gw_download_file/<filename>', methods=['GET', 'POST'])
def gw_download_file(filename):
    try:
        path='static/upload/gateway/'
        response = send_file(path+filename)
    except:
        print str(traceback.format_exc())
    return response

@gateway_app.route('/gw_get_all_files', methods=['GET', 'POST'])
def gw_get_all_files():
    try:
        file_info={}
        file_list = {'files':[]}

        file_path = glob.glob(GATEWAY_UPLOAD_DIR+"*.zip")
        for i in range(0,len(file_path)):
            path,file = os.path.split(file_path[i])
            data = db.db_get_gateway_file(file)

            for row in data:
                file_info = file_info.copy()
                file_info['filename'] = row[0]
                file_info['major_version'] = row[1]
                file_info['minor_version'] = row[2]
                file_info['modified_date'] = str(row[3])
                file_info['commit_number'] = row[4]
                file_info['commit_date'] = str(row[5])
                file_info['remarks'] = row[6]
                file_info['latest'] = row[7]
                file_list['files'].append(file_info)
    except:
        print str(traceback.format_exc())

    return jsonify(file_list)

################################################################################

@gateway_app.route('/gw_upload_file', methods=['GET', 'POST'])
def gw_upload_file():
    result={'result':False}
    try:
        if 'fileGateway' not in request.files:
            result['result'] = False
        gateway_file = request.files['fileGateway']
        if gateway_file.filename == '':
            print 'No selected file'
            result['result'] = False
        elif gateway_file and _gw_verify_file(gateway_file.filename):
            filename = secure_filename(gateway_file.filename)
            gateway_file.save(os.path.join(GATEWAY_UPLOAD_DIR, filename))
            file_info=_gw_get_file_info(os.path.join(GATEWAY_UPLOAD_DIR, filename))
            db.db_add_gateway_file(file_info)
            result['result'] = True
    except:
        print str(traceback.format_exc())
        result['result'] = False
    return jsonify(result)

################################################################################

@gateway_app.route('/gw_delete_file', methods=['GET', 'POST'])
def gw_delete_file():
    result={'result':False}
    try:
        filename = request.args.get('filename')
        os.remove(os.path.join(GATEWAY_UPLOAD_DIR, filename))
        db.db_delete_gateway_file(filename)
        result['result'] = True
    except:
        print str(traceback.format_exc())
        result['result'] = False
    return jsonify(result)

################################################################################

@gateway_app.route('/gw_save_remarks', methods=['GET', 'POST'])
def gw_save_remarks():
    result={'result':False}
    try:
        filename = request.args.get('filename')
        remarks = request.args.get('remarks')
        db.db_update_gateway_file(filename,'remarks',remarks)
        result['result'] = True
    except:
        print str(traceback.format_exc())
        result['result'] = False
    return jsonify(result)

################################################################################

@gateway_app.route('/gw_save_latest', methods=['GET','POST'])
def gw_save_latest():
    result={'result':False}
    try:
        filename = request.args.get('filename')
        data = db.db_get_all_gateway_files()

        for row in data:
            db_filename = row[0]
            if (filename == db_filename):
                db.db_update_gateway_file(db_filename,'latest','1')
            else:
                db.db_update_gateway_file(db_filename,'latest','0')
        result['result'] = True
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
