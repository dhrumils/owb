#!/usr/bin/env python

from flask import Flask, jsonify, render_template, request, redirect, url_for, Blueprint
from flask import Flask, render_template
from .. import db
webcfg = Flask(__name__)
webcfg.debug = False

import web_cfg
