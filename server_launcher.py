#!/usr/bin/env python

################################################################################
# file      server_launcher.py
#           This script runs flask server
#
# author    Glide Technology Pvt. Ltd. <www.glidemtech.com>
# version   1.0
# date      29, Jul, 2017
################################################################################

################################################################################
# dependencies
################################################################################
import server

################################################################################
# constants
################################################################################

HOST = '0.0.0.0'
PORT = 80

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

#none

################################################################################
# script
################################################################################

server.init()
server.run(HOST, PORT)

################################################################################
# end of file
################################################################################
