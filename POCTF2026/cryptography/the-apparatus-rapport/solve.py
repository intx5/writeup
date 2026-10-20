ALPHA_LO, ALPHA_HI = (32, 126)
KEY = 'BAIGECH'
K = [ord(c) - ord('A') for c in KEY]
PRIMARY_CT = 'QOKZJ}</1<6:0_TEY^^\\UWDNN\\5MG.VIVU[HBMW6VKTI_UEIYCLSS6P=~'
SECONDARY_SHOWN = 'Cy(yen{!avj$d!!a{n0"iz |ni"iseizl"ksa t$d|u vux"yft}xrgk- k$qwfn(zlg\'xa"4'
SECONDARY_SRC = SECONDARY_SHOWN[:58] + ' ' + SECONDARY_SHOWN[58:]

def decrypt(text, key):
    m = ALPHA_HI - ALPHA_LO + 1
    return ''.join((chr((ord(c) - ALPHA_LO - key[i % len(key)]) % m + ALPHA_LO) for i, c in enumerate(text)))

def encrypt(text, key):
    m = ALPHA_HI - ALPHA_LO + 1
    return ''.join((chr((ord(c) - ALPHA_LO + key[i % len(key)]) % m + ALPHA_LO) for i, c in enumerate(text)))

def check_board(moves):
    board = {}
    lines = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
    for i, label in enumerate(moves):
        board[ord(label) - 65] = 'X' if i % 2 == 0 else 'O'
        if i % 2 == 0:
            for a, b, c in lines:
                if board.get(a) == board.get(b) == board.get(c) == 'X':
                    return (board, i)
    return (board, None)
if __name__ == '__main__':
    board, win = check_board(KEY)
    shown = ''.join((board.get(i, '.') for i in range(9)))
    print('board from moves A..I:', ' '.join((f'{chr(65 + i)}={shown[i]}' for i in range(9))))
    assert shown == 'OXO.X.OXX', shown
    assert win == 6, f'X should win on move 7, got index {win}'
    print(f'moves: {KEY}  -> X completes B-E-H on move 7 (index {win})')
    pt = decrypt(PRIMARY_CT, K)
    assert encrypt(pt, K) == PRIMARY_CT
    print(f'\nprimary plaintext:\n{pt}')
    sec = decrypt(SECONDARY_SRC, K)
    assert encrypt(sec, K) == SECONDARY_SRC
    print(f'\nsecondary plaintext:\n{sec}')
    print(f"\nsecondary as displayed (collapsed space) re-encrypts to the shown string: {encrypt(sec, K).replace('  ', ' ') == SECONDARY_SHOWN}")
