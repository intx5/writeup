import asyncio, json, os, sys, time
import aiohttp
BASE = os.path.dirname(os.path.abspath(__file__))
URL = 'https://pointeroverflowctf.com/challenges/consulting-room/oracle'
TOKEN = open(os.path.join(BASE, '..', 'files', 'token.txt')).read().strip()
CIPHER = bytes.fromhex(open(os.path.join(BASE, '..', 'files', 'cipher.hex')).read().strip())
BLOCKS = [CIPHER[i:i + 16] for i in range(0, len(CIPHER), 16)]
STATE_PATH = os.path.join(BASE, 'state.json')
RATE = float(os.environ.get('RATE', '15.0'))
BURST = float(os.environ.get('BURST', '15'))
WINDOW = int(os.environ.get('WINDOW', '10'))
HDR = {'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json'}

class Limiter:

    def __init__(self, rate, burst):
        self.rate, self.burst, self.tokens = (rate, burst, burst)
        self.last = time.monotonic()
        self.lock = asyncio.Lock()

    async def acquire(self):
        async with self.lock:
            while True:
                now = time.monotonic()
                self.tokens = min(self.burst, self.tokens + (now - self.last) * self.rate)
                self.last = now
                if self.tokens >= 1.0:
                    self.tokens -= 1.0
                    return
                await asyncio.sleep((1.0 - self.tokens) / self.rate)
limiter = Limiter(RATE, BURST)
stats = {'req': 0, 'ok': 0, 'bad': 0, 'err': 0, '429': 0}
t_start = time.monotonic()

def log(msg):
    el = time.monotonic() - t_start
    print(f"[{el:7.1f}s req={stats['req']:5d} ok={stats['ok']:5d} bad={stats['bad']:3d} 429={stats['429']:2d} err={stats['err']:2d}] {msg}", flush=True)

async def oracle(session, blob: bytes):
    for attempt in range(6):
        await limiter.acquire()
        stats['req'] += 1
        try:
            async with session.post(URL, headers=HDR, json={'record': blob.hex()}, timeout=aiohttp.ClientTimeout(total=20)) as r:
                txt = await r.text()
                if r.status == 429:
                    stats['429'] += 1
                    log(f'429 rate-limited, sleeping ({attempt})')
                    await asyncio.sleep(3 + 2 * attempt)
                    continue
                try:
                    j = json.loads(txt)
                except Exception:
                    j = None
                if isinstance(j, dict) and 'padding' in j:
                    stats['ok'] += 1
                    return j['padding'] == 'valid'
                stats['bad'] += 1
                log(f'unexpected HTTP {r.status}: {txt[:100]!r}')
                await asyncio.sleep(1 + attempt)
        except Exception as e:
            stats['err'] += 1
            log(f'request error: {type(e).__name__}: {e}')
            await asyncio.sleep(1 + attempt)
    raise RuntimeError('oracle unavailable')

async def recover_byte(session, target: bytes, I, k: int):
    pad = 16 - k
    assert 1 <= pad <= 16
    X = bytearray(16)
    for t in range(k + 1, 16):
        X[t] = I[t] ^ pad

    async def probe(g):
        Xg = bytearray(X)
        Xg[k] = g
        ok = await oracle(session, bytes(Xg) + target)
        return (g, ok)
    for start in range(0, 256, WINDOW):
        chunk = list(range(start, min(start + WINDOW, 256)))
        results = await asyncio.gather(*(probe(g) for g in chunk))
        for g, ok in results:
            if not ok:
                continue
            if k == 15:
                Xv = bytearray(X)
                Xv[15] = g
                Xv[14] ^= 255
                if not await oracle(session, bytes(Xv) + target):
                    continue
            return g
    raise RuntimeError(f'no value found for byte {k}')

def load_state():
    if os.path.exists(STATE_PATH):
        with open(STATE_PATH) as f:
            return json.load(f)
    st = {'I': {}}
    for i in range(1, len(BLOCKS)):
        st['I'][str(i)] = [None] * 16
    return st

def save_state(st):
    tmp = STATE_PATH + '.tmp'
    with open(tmp, 'w') as f:
        json.dump(st, f)
    os.replace(tmp, STATE_PATH)

async def main():
    st = load_state()
    log(f'cipher: {len(CIPHER)}B, {len(BLOCKS)} blocks; recovering D(C1..C{len(BLOCKS) - 1})')
    conn = aiohttp.TCPConnector(limit=32, ttl_dns_cache=300)
    async with aiohttp.ClientSession(connector=conn) as session:
        for i in range(1, len(BLOCKS)):
            I = st['I'][str(i)]
            target = BLOCKS[i]
            for k in range(15, -1, -1):
                if I[k] is not None:
                    continue
                t0 = time.monotonic()
                g = await recover_byte(session, target, I, k)
                I[k] = g ^ 16 - k
                save_state(st)
                log(f'block C{i} byte {k:2d} = 0x{I[k]:02x}  ({time.monotonic() - t0:.1f}s)')
    out = bytearray()
    for i in range(1, len(BLOCKS)):
        I = bytes(st['I'][str(i)])
        prev = BLOCKS[i - 1]
        out += bytes((a ^ b for a, b in zip(I, prev)))
    log(f'raw padded plaintext ({len(out)}B): {out.hex()}')
    n = out[-1]
    if 1 <= n <= 16 and out[-n:] == bytes([n]) * n:
        body = bytes(out[:-n])
        log(f'padding length {n}; plaintext ({len(body)}B): {body!r}')
    else:
        body = bytes(out)
        log(f'!! invalid padding in recovered plaintext, last byte {n}')
if __name__ == '__main__':
    asyncio.run(main())
