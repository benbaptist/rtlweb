import os
import threading
import time

from example.logmanager import LogManager
from example.dashboard import Dashboard
from example.storify import Storify
from example.config import Config
# from example.gui import GUI # uncomment if needed

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

		# Initialize dashboard (comment if not needed)
		self.dashboard = Dashboard(self, host=self.config["dashboard"]["bind"], port=self.config["dashboard"]["port"])

		# Initialize GUI (uncomment if needed)
		# self.gui = GUI("http://127.0.0.1:%s" % self.dashboard.port, self)

		self.threads = {}
		self.abort = False

	def start(self):
		# Put stuff here

		# Start dashboard (comment if not needed)
		self.threads["dashboard"] = threading.Thread(target=self.dashboard.run, args=())
		self.threads["dashboard"].daemon = True
		self.threads["dashboard"].start()

		# Start GUI (uncomment if needed)
		# time.sleep(1)
		# self.gui.run()

		try:
			self.run()
		except KeyboardInterrupt:
			self.log.warning("Ctrl+C intercepted")
			self.storify.flush()

	def run(self):
		while not self.abort:
			# Tick

			# Storify tick
			self.storify.tick()

			time.sleep(1)
