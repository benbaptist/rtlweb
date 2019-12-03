from scipy.fftpack import fft

SAMPLE_RATE = (2 * 1000) * 1000
BIT_DEPTH = 1

RESOLUTION = 32

print(SAMPLE_RATE, BIT_DEPTH)

with open("/tmp/dick.iq", "rb") as f:
    buff = f.read(SAMPLE_RATE * BIT_DEPTH)
