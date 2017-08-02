#!/usr/bin/python

from flask_socketio import SocketIO
sio = SocketIO()

import database
db = database.DatabaseHandler()

import app_config
import web_config

from server import *
