FILES = 'abcdefgh'
moves = ['c3', 'a4', 'e4', 'd3', 'd3', 'e3', 'e4', 'c3', 'h3', 'c3', 'b3', 'a3', 'c3', 'b3', 'h3', 'c3']

def digit(sq):
    f = FILES.index(sq[0])
    r = int(sq[1])
    return 2 * f + (r - 3)
nonce = ''.join((format(digit(sq), 'X') for sq in moves))
print('nonce:', nonce)
gen = []
for ch in nonce:
    d = int(ch, 16)
    f, bit = divmod(d, 2)
    rank = 3 + bit
    gen.append((rank == 3, FILES[f] + str(rank)))
print('regenerated moves:', ' '.join((('Nx' if p else '') + s for p, s in gen)))
print('matches PDF:', gen == [(s[1] == '3', s) for s in moves])
