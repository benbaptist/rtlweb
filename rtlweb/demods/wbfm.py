from rtlweb.demods import Demods

import subprocess
import json
import time

from rtlweb.resampler import Resampler

class WBFM(Demods):
    def __init__(self, radio):
        super().__init__(radio, "wbfm")

        self.reset()

        self.resampler = Resampler(from_sample_rate=171000)

    def reset(self):

        try:
            self.rtlproc.kill()
            self.redsea.kill()

            self.log.info("Killed old procs")
        except:
            pass

        self.rtlproc = None
        self.redsea = None
        self.redsea_queue = None

        self.rds = {
            "callsign": None,
            "ps": None,
            "genre": None,
            "radiotext": None,
            "bler": None
        }

        self.stats = {
            "rds": self.rds
        }

    def tick(self):
        if self.current_freq != self.radio.freq:
            self.log.info("Frequency changed, resetting wbfm...")
            self.current_freq = self.radio.freq
            self.reset()

        if not self.rtlproc:
            self.log.info("Initiating rtlproc...")

            command = "rtl_fm -M fm -l 0 -A std -p 0 -s 171k -g 20 -F 9 -f %s" % self.radio.freq
            self.rtlproc = subprocess.Popen(command.split(" "), stdout=subprocess.PIPE)

        if not self.redsea:
            self.log.info("Initiating redsea...")

            command = "redsea -uE"
            self.redsea = subprocess.Popen(command.split(" "), stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            self.redsea_queue = self.radio.setup_stdout_queue(self.redsea)

        if self.rtlproc.poll():
            self.log.error("RTL command died")
            self.reset()
            return

        frame = self.rtlproc.stdout.read(1024 * 4)

        self.resampler.write(frame)
        audio_frame = self.resampler.read()

        if audio_frame:
            self.radio.audio_frame = audio_frame

        self.redsea.stdin.write(frame)

        if self.redsea_queue.qsize() > 0:
            lines = self.redsea_queue.get_nowait().decode("utf8").split("\n")
            for line in lines:
                if len(line) > 0:
                    data = json.loads(line)

                    if "callsign" in data:
                        callsign = data["callsign"]

                        if callsign != self.rds["callsign"]:
                            self.log.info("Callsign: %s" % callsign)

                        self.rds["callsign"] = callsign

                    if "prog_type" in data:
                        prog_type = data["prog_type"]

                        if prog_type != self.rds["genre"]:
                            self.log.info("Genre: %s" % prog_type)

                        self.rds["genre"] = prog_type

                    if "ps" in data:
                        ps = data["ps"]

                        if ps != self.rds["ps"]:
                            self.log.info("PS: %s" % ps)

                        self.rds["ps"] = ps

                    if "bler" in data:
                        self.rds["bler"] = data["bler"]

                    if "radiotext" in data:
                        ps = data["radiotext"]

                        if ps != self.rds["radiotext"]:
                            self.log.info("Radio Text: %s" % ps)

                        self.rds["radiotext"] = ps
