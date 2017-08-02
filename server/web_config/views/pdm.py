#!/usr/bin/env python

################################################################################
# file      pdm.py
#           This script handles requests related to pdm from web gui
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
from flask import Flask, jsonify, render_template, request, redirect, url_for, send_from_directory, Blueprint
from werkzeug.utils import secure_filename
from datetime import datetime
from . import db

################################################################################
# constants
################################################################################

ALLOWED_EXTENSIONS = set(['zip'])
PDM_UPLOAD_DIR = 'server/web_config/static/upload/pdm/'

################################################################################
# private variables
################################################################################

# none

################################################################################
# public variables
################################################################################

pdm_app = Blueprint('pdm_app', __name__)

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

def _pdm_get_file_info(filename):
    try:
        json_decode={}
        pdm_schema = db.db_pdm_schema()
        zf=zipfile.ZipFile(filename, 'r')
        for file in zf.namelist():
            if file == "file_info.json":
                json_decode=json.loads(zf.read(file))
                pdm_schema['filename'] =  json_decode.get('filename')
                pdm_schema['major_version'] = json_decode.get('major_version')
                pdm_schema['minor_version'] = json_decode.get('minor_version')
                pdm_schema['modified_date'] = json_decode.get('modified_date')
                pdm_schema['commit_number'] = json_decode.get('commit_number')
                pdm_schema['commit_date'] = json_decode.get('commit_date')
                pdm_schema['remarks'] = json_decode.get('remarks')
                pdm_schema['latest'] = json_decode.get('latest')
    except:
        print str(traceback.format_exc())
    return pdm_schema

################################################################################

def _pdm_verify_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

################################################################################
# public methods
################################################################################

@pdm_app.route('/pdm_get_all_files', methods=['GET', 'POST'])
def gw_get_all_files():
    try:
        file_info={}
        filelist = {'files':[]}
        file_path = glob.glob(PDM_UPLOAD_DIR+"*.zip")

        for i in range(0,len(file_path)):
            head,tail = os.path.split(file_path[i])
            data = db.db_get_pdm_file(tail)
            for row in data:
                file_info = file_info.copy()
                file_info['filename'] = row[0]
                file_info['major_version'] = row[1]
                file_info['minor_version'] = row[2]
                file_info['modified_date'] = row[3]
                file_info['commit_number'] = row[4]
                file_info['commit_date'] = row[5]
                file_info['remarks'] = row[6]
                file_info['latest'] = row[7]
                filelist['files'].append(file_info)
    except:
        print str(traceback.format_exc())
    return jsonify(filelist)

################################################################################

@pdm_app.route('/pdm_upload_file', methods=['GET', 'POST'])
def pdm_upload_file():

    result={'result':False}
    try:
        if 'filePDM' not in request.files:
            print 'No file part'
            result['result'] = False
        pdm_file = request.files['filePDM']
        if pdm_file.filename == '':
            print 'No selected file'
            result['result'] = False
        elif pdm_file and _pdm_verify_file(pdm_file.filename):
            filename = secure_filename(pdm_file.filename)
            pdm_file.save(os.path.join(PDM_UPLOAD_DIR, filename))
            file_info=_pdm_get_file_info(os.path.join(PDM_UPLOAD_DIR, filename))
            db.db_add_pdm_file(file_info)
            result['result'] = True
    except:
        print str(traceback.format_exc())
    return jsonify(result)

################################################################################

@pdm_app.route('/pdm_delete_file', methods=['GET', 'POST'])
def pdm_delete_file():
    result={'result':False}
    try:
        filename = request.args.get('filename')
        os.remove(os.path.join(PDM_UPLOAD_DIR, filename))
        db.db_delete_pdm_file(filename)
        result['result'] = True
    except:
        print str(traceback.format_exc())
        result['result'] = False
    return jsonify(result)

################################################################################

@pdm_app.route('/pdm_save_remarks', methods=['GET', 'POST'])
def pdm_save_remarks():
    result={'result':False}
    try:
        filename = request.args.get('filename')
        remarks = request.args.get('remarks')
        db.db_update_pdm_file(filename,'remarks',remarks)
        result['result'] = True
    except:
        print str(traceback.format_exc())
        result['result'] = False
    return jsonify(result)

################################################################################

@pdm_app.route('/pdm_save_latest', methods=['GET','POST'])
def pdm_save_latest():
    result={'result':False}
    try:
        filename = request.args.get('filename')
        data = db.db_get_all_pdm_files()

        for row in data:
            db_filename = row[0]
            if (filename == db_filename):
                db.db_update_pdm_file(db_filename,'latest','1')
            else:
                db.db_update_pdm_file(db_filename,'latest','0')
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
