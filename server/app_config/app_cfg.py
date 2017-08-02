#!/usr/bin/env python

################################################################################
# file      app_cfg.py
#           This script handles requests from Android App
#
# author    Glide Technology Pvt. Ltd. <www.glidemtech.com>
# version   1.0
# date      29, Jul, 2017
################################################################################

################################################################################
# dependencies
################################################################################

import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'server'))
sys.path.append('/opt/cwhb-server/server')

from .. import sio
from . import db
import traceback
import zipfile

################################################################################
# constants
################################################################################

FIRMWARE_FILE="firmware.bin"
GATEWAY_UPLOAD_PATH="server/web_config/static/upload/gateway/"
PDM_UPLOAD_PATH="server/web_config/static/upload/pdm/"

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

# none

################################################################################
# private methods
################################################################################

#none

################################################################################
# public methods
################################################################################

######################### Gateway Page Requests ################################
@sio.on('update_gateway_eth', namespace= '/APP')
def on_update_gateway_eth(details):
    url=None
    try:
        firmware_buffer = bytearray()
        zf = db.db_get_latest_gateway_file()
        url = 'http://2.2.2.178/gw_download_file/'+zf
    except:
        print str(traceback.format_exc())
    return url

######################### PDM Page Requests ####################################

@sio.on('update_pdm_eth', namespace= '/APP')
def on_update_pdm_eth():
    url=None
    try:
        firmware_buffer = bytearray()
        zf = db.db_get_latest_pdm_file()
        url = 'http://2.2.2.178/pdm_download_file/'+zf
    except:
        print str(traceback.format_exc())
    return url

@sio.on('update_pdm_usb', namespace= '/APP')
def on_update_pdm_usb():
    try:
        firmware_buffer = bytearray()
        zf = db.db_get_latest_pdm_file()
        zf = PDM_UPLOAD_PATH+zf
        if zf != None:
            archive = zipfile.ZipFile(zf, 'r')
            firmware_buffer = bytearray(archive.read(FIRMWARE_FILE))
    except:
        print str(traceback.format_exc())
    return firmware_buffer


################################################################################
# script
################################################################################

# none

################################################################################
# end of file
################################################################################
