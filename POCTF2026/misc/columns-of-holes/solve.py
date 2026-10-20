import os, re, subprocess, sys
import numpy as np
from PIL import Image
from scipy import ndimage
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(HERE, 'work')
PDF = os.path.join(HERE, 'job-ticket-1406.pdf')
imgs = [os.path.join(WORK, f'card-{i:03d}.png') for i in (0, 1)]
if not all((os.path.exists(p) for p in imgs)):
    os.makedirs(WORK, exist_ok=True)
    subprocess.run(['pdfimages', '-png', PDF, os.path.join(WORK, 'card')], check=True)
ROWS = ['12', '11', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
B32 = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ234567')

def extract_grid(path):
    im = np.array(Image.open(path).convert('RGB'))
    gray = im.max(axis=2)
    mask = gray < 45
    lbl, _ = ndimage.label(mask)
    grid = {c: set() for c in range(1, 81)}
    for i, sl in enumerate(ndimage.find_objects(lbl), 1):
        if sl is None:
            continue
        area = (lbl[sl] == i).sum()
        h = sl[0].stop - sl[0].start
        w = sl[1].stop - sl[1].start
        if not (200 < area < 400 and 8 <= w <= 16 and (20 <= h <= 32)):
            continue
        cy, cx = ndimage.center_of_mass(mask, lbl, i)
        col = round((cx - 59.5) / 19) + 1
        ri = round((cy - 111.0) / ((579.0 - 111.0) / 11))
        if 1 <= col <= 80 and 0 <= ri < 12:
            grid[col].add(ROWS[ri])
    return grid

def decode(rows):
    s = set(rows)
    if not s:
        return ' '
    if len(s) == 1:
        r = next(iter(s))
        if r in '0123456789':
            return r
        return {'12': '&', '11': '-'}[r]
    if '12' in s and len(s) == 2:
        r = (s - {'12'}).pop()
        return chr(ord('A') + int(r) - 1) if r in '123456789' else '{'
    if '11' in s and len(s) == 2:
        r = (s - {'11'}).pop()
        return chr(ord('J') + int(r) - 1) if r in '123456789' else '}'
    if '0' in s and len(s) == 2:
        r = (s - {'0'}).pop()
        if r in '23456789':
            return chr(ord('S') + int(r) - 2)
        return '/'
    if s == {'2', '8'}:
        return ':'
    if s == {'3', '8'}:
        return '#'
    return '?'
texts = []
for p in imgs:
    grid = extract_grid(p)
    texts.append(''.join((decode(sorted(grid[c], key=ROWS.index)) for c in range(1, 81))))
fragments = []
for text in texts:
    m = re.search('PAT#(\\d+)', text)
    pat = m.group(1)
    start, stride = (int(pat[0]), int(pat[1]))
    payload = text[44:80]
    fragment = ''.join((payload[start + k * stride] for k in range(8)))
    print(f'{text[:9]}  PAT#{pat}  start={start} stride={stride}')
    print(f'          payload={payload}')
    print(f'          fragment={fragment}')
    fragments.append(fragment)
nonce = ''.join(fragments)
print()
print('NONCE:', nonce)
print('FLAG:  POCTF{%s}' % nonce)
