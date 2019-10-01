import subprocess
import queue
import threading

class Resampler:
    def __init__(self, from_sample_rate=32000, from_channels=1, to_sample_rate=48000, to_channels=2):
        self.to_sample_rate = to_sample_rate
        self.to_channels = to_channels

        command = ["ffmpeg",
            "-f", "s16le", "-ar", str(from_sample_rate), "-ac", str(from_channels),
            "-i", "-",
            "-f", "s16le", "-ar", str(to_sample_rate), "-ac", str(to_channels),
            "-"]
        self.proc = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.queue = queue.Queue()

        t = threading.Thread(target=self.listen)
        t.daemon = True
        t.start()

    def listen(self):
        while not self.proc.poll():
            self.queue.put(self.proc.stdout.read(48000 * 2 * 2))

    def read(self):
        if self.queue.qsize() > 0:
            return self.queue.get_nowait()

    def write(self, bytes):
        self.proc.stdin.write(bytes)
