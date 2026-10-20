import sys, os
MAGIC = bytes.fromhex('9ee1c721')
ITEMS = [(b'Rusted spirit-medallion', b'Illegible engraving. Legible weight.'), (b'Obsidian censer', b'Smells faintly of camphor.'), (b'Silver-thread bandage', b'Wound around a wound not yours.'), (b'Ivory dial-plate', b'Twelve marks. Only nine of them tick.'), (b'Lead-bound envelope', b'Sender uncertain. Recipient certain.'), (b'Doubling mirror', b'Shows you plus one, in bad light.'), (b'Jarful of teeth', b'Sorted. Cataloged. Undisturbed.'), (b'Ember-in-glass', b'Warm regardless of the room.'), (b'Vessel-key', b'Fits the mouth of every empty flask.'), ('Cracked séance disc'.encode(), b'The needle skips over the same phrase.'), (b'Marrow-quill pen', b'Writes in whatever ink you last saw.'), (b'Uncoiling rope', b"Never quite ends. You've measured."), (b'4-quadrant ephemeris', b'Missing the pages for the current year.'), (b'Needle of the Bureau', b'Points at your own signature.'), (b'Hair-braid amulet', b'Not yours. Old. Not old enough.'), (b'Talcum-stained token', b'Fingerprints of five different hands.')]

def recover_key(payload):
    votes = {}
    for name, desc in ITEMS:
        s = name + len(desc).to_bytes(2, 'little') + desc
        for p in range(len(payload) - len(s) + 1):
            key = [None] * 8
            ok = True
            for k, ch in enumerate(s):
                r = (p + k) % 8
                v = payload[p + k] ^ ch
                if key[r] is None:
                    key[r] = v
                elif key[r] != v:
                    ok = False
                    break
            if ok:
                kb = bytes(key)
                votes[kb] = votes.get(kb, 0) + 1
    if not votes:
        raise SystemExit('key recovery failed')
    return max(votes, key=votes.get)

def parse_items(plain):
    items, i = ([], 0)
    while i < len(plain):
        if plain[i] == 16 and i + 5 <= len(plain):
            name_len = plain[i + 4]
            if 0 < name_len < 64:
                try:
                    name = plain[i + 5:i + 5 + name_len].decode('utf-8')
                except UnicodeDecodeError:
                    name = None
                if name and all((c.isprintable() for c in name)):
                    dl = int.from_bytes(plain[i + 5 + name_len:i + 7 + name_len], 'little')
                    end = i + 7 + name_len + dl
                    if 0 < dl < 300 and end <= len(plain):
                        try:
                            desc = plain[i + 7 + name_len:end].decode('utf-8')
                        except UnicodeDecodeError:
                            desc = None
                        if desc and all((c.isprintable() for c in desc)):
                            items.append(name)
                            i = end
                            continue
        i += 1
    return items

def solve(path):
    data = open(path, 'rb').read()
    assert data[:4] == MAGIC, 'bad magic'
    total = int.from_bytes(data[8:12], 'little')
    payload = data[12:-4]
    key = recover_key(payload)
    plain = bytes((b ^ key[i % 8] for i, b in enumerate(payload)))
    items = parse_items(plain)
    initials = ''.join((n[0] for n in items))
    print(f'{os.path.basename(path)}: key={key.hex()} items={len(items)}')
    print(f"  items: {', '.join(items)}")
    print(f'  initials: {initials}')
    return initials
if __name__ == '__main__':
    for p in sys.argv[1:]:
        solve(p)
