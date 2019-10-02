import os
import threading
import time

from rtlweb.logmanager import LogManager
from rtlweb.dashboard import Dashboard
from rtlweb.storify import Storify
from rtlweb.config import Config
from rtlweb.radio import Radio

class Main:

	def __init__(self):
		# Initialize logging (comment if not needed )
		self.logManager = LogManager()
		self.log = self.logManager.getLogger("Main")

		# Configure configuration
		self.config = Config(path="data/config.json", template={
			"dashboard": {
				"bind": "127.0.0.1",
				"port": 4321
			}
		}, log=self.logManager.getLogger("Config"))
		self.config.save()

		# Configure data storage (comment if not needed)
		if not os.path.exists("data"):
			os.mkdir("data")

		self.storify = Storify(log=self.logManager.getLogger("Storify"))
		self.db = self.storify.getDB("main")

		self.radio = Radio(self.logManager)

		# Initialize dashboard
		self.dashboard = Dashboard(self, host=self.config["dashboard"]["bind"], port=self.config["dashboard"]["port"])

		self.threads = {}
		self.abort = False

	def start(self):
		# Start dashboard
		self.threads["dashboard"] = threading.Thread(target=self.dashboard.run, args=())
		self.threads["dashboard"].daemon = True
		self.threads["dashboard"].start()

		try:
			self.run()
		except KeyboardInterrupt:
			self.log.warning("Ctrl+C intercepted")
			self.storify.flush()

	def run(self):
		while not self.abort:
			# Tick
			self.radio.tick()

			# Storify tick
			self.storify.tick()

			time.sleep(.01)
