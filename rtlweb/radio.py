import threading
import queue

from rtlweb.demods.wbfm import WBFM

class Radio:
    def __init__(self, log_manager):
        self.log_manager = log_manager
        self.log = self.log_manager.getLogger("Radio")

        self.freq = 98.3 * 1000 * 1000 # 98.3MHz
        self.demod = WBFM(self) # off

        self.audio_frame = bytes(48000 * 2 * 2)

    def tick(self):
        if self.demod:
            self.demod.tick()

    def setup_stdout_queue(self, proc):
        q = queue.Queue()

        def listener():
            for line in proc.stdout:
                q.put(line)

        threading.Thread(target=listener).start()

        return q
        # print(type(self._current), type(self.mode))
        # if type(self._current) != self.mode:
        #     # self._current.shutdown()
        #
        #     if self.mode == None:
        #         self._current = None
        #     elif self.mode == "wbfm":
        #         print("Making wbfm instance")
        #         self._current = self.mode(self)
        #
        # if self._current:
        #     self._current.tick()
