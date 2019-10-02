Python-based SDR receiver, controlled entirely over the web. All processing performed server-side, for minimum bandwidth impact.

# Dependencies
rtlweb is written on top of Python 3.x, and was intended for use under a Linux system.

- Linux
- rx_tools (`https://github.com/rxseger/rx_tools`)
- redsea
- ffmpeg (requires HLS & libaac support)
- msgpack (`pip3 install msgpack`)
- flask (`pip3 install flask`)
- flask_socketio (`pip3 install flask_socketio`)
- flask_htmlmin (`pip3 install flask_htmlmin`)
- flask_htmlmin (`pip3 install flask_htmlmin`)

# Quick Start

A simple guide to get up and running. Assumes an Ubuntu/Debian-like environment.

- Run this to install the Python modules.
```pip3 install msgpack flask flask_socketio flask_htmlmin eventlet```

- Compile and install rx-tools

Install dependency for rx_tools.
```sudo apt install libsoapysdr-dev```

Grab rx_tools' latest source.
```
git clone https://github.com/rxseger/rx_tools.git
cd rx_tools
cmake .
make
```

Install it. It may require root to run this command.
```
make install
```

- Compile and install red-sea

```
# Install dependencies for redsea
sudo apt install git build-essential autoconf libsndfile1-dev libliquid-dev

# Build in /tmp
cd /tmp/
git clone https://github.com/windytan/redsea.git
cd redsea
 ./autogen.sh && ./configure && make

# This final command may need to be run as root
make install
```

- Install ffmpeg.
Ensure HLS & AAC support is enabled. Usually, ffmpeg from the Debian/ffmpeg repositories are good.

5. Clone this repository.
```
git clone https://github.com/benbaptist/rtlweb.git
cd rtlweb
```

6. Start, and enjoy!
```python3 start-rtlweb.py```
