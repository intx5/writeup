import os, subprocess, sys
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BIN = os.path.join(HERE, 'files', 'panoptican')
TBL_OFF, TPL_OFF, N = (8304, 8432, 1024)
data = open(BIN, 'rb').read()
table = data[TBL_OFF:TBL_OFF + 128]
template = data[TPL_OFF:TPL_OFF + N]
auth = bytes((t ^ tpl for t, tpl in zip(table, template)))
code = auth.split(b'\x00', 1)[0].decode('ascii')
print('AUTH:', code)
pgm = os.path.join(HERE, 'work', 'enrolled.pgm')
with open(pgm, 'wb') as f:
    f.write(b'P5\n32 32\n255\n' + template)
print('wrote', pgm)
if '--run' in sys.argv:
    out = subprocess.run([BIN, pgm], capture_output=True, text=True, timeout=10)
    print('binary output:', out.stdout.strip(), '(exit', out.returncode, ')')
