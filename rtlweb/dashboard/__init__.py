from flask import Flask, g, redirect, url_for, render_template, request, make_response, Response, Markup
from flask_socketio import SocketIO, send, emit, join_room, leave_room
# from flask.ext_htmlmin import HTMLMIN
from flask_htmlmin import HTMLMIN

import os
import signal
import time
import random
import json
import traceback
import datetime
import requests

from rtlweb.dashboard.hls import HLS

class Dashboard:
	def __init__(self, main, host="127.0.0.1", port=4321, portDebug=5432, debugMode=False):
		self.main = main
		self.host = host
		self.port = port
		self.portDebug = portDebug
		self.debugMode = debugMode

		self.app = Flask(__name__)
		self.app.config['SECRET_KEY'] = ""
		self.app.config['MINIFY_PAGE'] = True
		self.app.config['TEMPLATES_AUTO_RELOAD'] = True

		self.socketio = SocketIO(self.app)

		self.radio = main.radio

		self.hls = HLS(self)
	def generateKey(self, length):
		a = None

		while not a:
			a = ""
			symbols = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-!@#$%^&*()"
			for i in range(length):
				a += random.choice(symbols)
		return a
	def add_decorators(self):
		# Pages
		@self.app.route("/")
		def index():
			if "freq" in request.args:
				self.main.radio.freq = int(request.args["freq"])

			return render_template("index.html", radio=self.main.radio)

		# Custom filters
		@self.app.template_filter()
		def dt(ts):
			date = datetime.datetime.utcfromtimestamp(ts)
			return date.strftime('%Y-%m-%d @ %H:%M:%S')

		# Error handling
		@self.app.errorhandler(AssertionError)
		def all_exception_handler(error):
			try:
				msg = str(error)

				if request.headers.getlist("X-Forwarded-For"):
				   ip = request.headers.getlist("X-Forwarded-For")[0]
				else:
				   ip = request.remote_addr

				errorInfo = {
					"errorMsg": msg,
					"time": time.time(),
					"headers": str(request.headers),
					"ip": ip
				}

				print("ERROR: %s" % str(errorInfo))

				return "<h1>Internal Server Error</h1>", 500
			except:
				traceback.print_exc()
				return "<h1>Stuff went VERY south. Contact an administrator, please.</h1>", 500
	def run(self):
		self.add_decorators()
		if self.debugMode:
			self.socketio.run(self.app, host=self.host, port=self.portDebug, debug=True, use_reloader=False)
		else:
			self.socketio.run(self.app, host=self.host, port=self.port, debug=False, use_reloader=False)
