CT = 'GMAHI{2.1406.IVO6QBESSAVR6SQY.HLBKYQLUC5UURU5TJGOPSPXEWF}'
KEY = 'VACANT'
KEY_FROM_STARS = 'VACANT'

def beaufort_decrypt(ct: str, key: str, advance_on_all: bool=False) -> str:
    out, ki = ([], 0)
    for ch in ct:
        if ch.isalpha():
            k = ord(key[ki % len(key)]) - ord('A')
            c = ord(ch) - ord('A')
            out.append(chr((k - c) % 26 + ord('A')))
            ki += 1
        else:
            out.append(ch)
            if advance_on_all:
                ki += 1
    return ''.join(out)

def beaufort_encrypt(pt: str, key: str, advance_on_all: bool=False) -> str:
    out, ki = ([], 0)
    for ch in pt:
        if ch.isalpha():
            k = ord(key[ki % len(key)]) - ord('A')
            p = ord(ch) - ord('A')
            out.append(chr((k - p) % 26 + ord('A')))
            ki += 1
        else:
            out.append(ch)
            if advance_on_all:
                ki += 1
    return ''.join(out)
if __name__ == '__main__':
    assert KEY == KEY_FROM_STARS
    derived = ''.join((chr((ord(c) - 65 + (ord(p) - 65)) % 26 + 65) for c, p in zip([x for x in CT if x.isalpha()][:5], 'POCTF')))
    print(f'key stream from known prefix : {derived}  (star order starts at Violet)')
    print(f'hidden key                   : {KEY}')
    pt = beaufort_decrypt(CT, KEY)
    assert beaufort_encrypt(pt, KEY) == CT
    print(f'\nplaintext (classical/alpha alignment):\n{pt}')
    alt = beaufort_decrypt(CT, KEY, advance_on_all=True)
    print(f'\nnaive index alignment (fallback):\n{alt}')
