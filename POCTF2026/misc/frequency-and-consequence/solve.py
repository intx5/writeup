import os, sys, wave
import numpy as np
ALPHA = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567'
FREQS = [500 + 50 * i for i in range(32)]
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'signal-team-1406.wav')
w = wave.open(path, 'rb')
fs, n = (w.getframerate(), w.getnframes())
x = np.frombuffer(w.readframes(n), dtype='<i2').astype(np.float64) / 32768.0
w.close()

def goertzel(seg, f):
    n = len(seg)
    c = 2.0 * np.cos(2.0 * np.pi * f / fs)
    s1 = s2 = 0.0
    for v in seg:
        s1, s2 = (v + c * s1 - s2, s1)
    return s1 * s1 + s2 * s2 - c * s1 * s2
start = 0.5
msg = []
for i in range(16):
    a = int(round((start + 0.5 * i) * fs))
    b = int(round((start + 0.5 * (i + 1)) * fs))
    seg = x[a:b] - x[a:b].mean()
    mags = [goertzel(seg, f) for f in FREQS]
    msg.append(ALPHA[int(np.argmax(mags))])
nonce = ''.join(msg)
print('nonce:', nonce)
print('flag:  POCTF{%s}' % nonce)
