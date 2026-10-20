import os, sys
from xdis.load import load_module
here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, 'program-team-1406.pyc')
res = load_module(path)
co = res[3]
check = next((c for c in co.co_consts if getattr(c, 'co_name', '') == 'check'))
consts = [c for c in check.co_consts if isinstance(c, (bytes, bytearray))]
enc1, _a, enc2, key2, _b = consts[:5]
assert len(enc1) == len(enc2) == len(key2)
expected = bytes((a ^ b ^ c for a, b, c in zip(enc1, enc2, key2)))
print('decoy _a unused:', _a != enc2 and _a not in (enc1, enc2, key2))
print('decoy _b unused:', _b not in (enc1, enc2, key2))
print('flag:', expected.decode('ascii'))
inner = expected.decode('ascii')[len('POCTF{'):-1]
print('nonce:', inner)
