N = 7
initial = [1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1]
assert len(initial) == N * N

def idx(r, c):
    return r * N + c
rows = []
for r in range(N):
    for c in range(N):
        mask = 0
        for dr, dc in ((0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = (r + dr, c + dc)
            if 0 <= nr < N and 0 <= nc < N:
                mask |= 1 << idx(nr, nc)
        rows.append([mask, initial[idx(r, c)]])
pivots = []
row = 0
for col in range(N * N):
    piv = None
    for rr in range(row, len(rows)):
        if rows[rr][0] >> col & 1:
            piv = rr
            break
    if piv is None:
        continue
    rows[row], rows[piv] = (rows[piv], rows[row])
    for rr in range(len(rows)):
        if rr != row and rows[rr][0] >> col & 1:
            rows[rr][0] ^= rows[row][0]
            rows[rr][1] ^= rows[row][1]
    pivots.append(col)
    row += 1
for mask, b in rows:
    if mask == 0 and b == 1:
        raise SystemExit('inconsistent system')
sol = 0
for rr, col in enumerate(pivots):
    if rows[rr][1]:
        sol |= 1 << col

def apply(bits, presses):
    s = bits[:]
    for i in presses:
        r, c = divmod(i, N)
        for dr, dc in ((0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = (r + dr, c + dc)
            if 0 <= nr < N and 0 <= nc < N:
                s[idx(nr, nc)] ^= 1
    return s
presses = [i for i in range(N * N) if sol >> i & 1]
print('nullity (free variables):', N * N - len(pivots))
print('press cells (1-indexed row,col):')
for i in presses:
    r, c = divmod(i, N)
    print(f'  ({r + 1},{c + 1})')
print('count:', len(presses))
final = apply(initial, presses)
print('final board all dark:', all((x == 0 for x in final)))
coords = ', '.join((f'[{i // N},{i % N}]' for i in presses))
print('\nconsole snippet:')
print(f"const N=7,cells=[...document.querySelectorAll('.cell')];[{coords}].forEach(([r,c])=>cells[r*N+c].click());")
