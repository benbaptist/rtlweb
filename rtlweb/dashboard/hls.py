import subprocess
import threading
import os
import time

# ffmpeg -f alsa -i pulse -c:a aac -b:a 192k  -hls_flags delete_segments -segment_list_size 40 -segment_time 10 -f hls /tmp/dank.m3u8


class HLS:
    def __init__(self, dashboard):
        self.dashboard = dashboard
        self.radio = dashboard.radio

        t = threading.Thread(target=self.run, args=())
        t.daemon = True
        t.start()
    def run(self):
        print("starting run")
        while True:
            print("Starting ffmpeg...")
            commands = ["ffmpeg", "-f", "s16le", "-ac", "2", "-ar", "48000", "-i", "-", "-c:a", "aac", "-b:a", "192k", "-hls_flags", "delete_segments", "-segment_list_size", "40", "-segment_time", "10", "-f", "hls", "rtlweb/dashboard/static/hls/stream.m3u8"]

            proc = subprocess.Popen(commands, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            print("Beginning write cycle")

            while not proc.poll():
                print("Write ", len(self.radio.audio_frame))
                proc.stdin.write(self.radio.audio_frame)
                time.sleep(1)

            print("End, killing ffmpeg")

            try:
                proc.kill()
            except:
                pass
