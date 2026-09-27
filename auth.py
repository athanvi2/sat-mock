"""Instructor lock: a 6-digit PIN plus Touch ID (WebAuthn platform authenticator) on the tutor's Mac.

Why hand-rolled WebAuthn: the only credential type a Mac's Touch ID produces is ES256 (ECDSA on P-256 with SHA-256),
with attestation "none". Verifying that needs a small CBOR reader and one ECDSA check, which is less code (and fewer
moving parts on Python 3.8) than pulling in a WebAuthn library plus a crypto backend. Attestation statements are not
verified; we only need "the same Touch ID sensor that enrolled is present and the finger matched".

Browsers only allow WebAuthn on a secure origin. http://localhost counts; a LAN address like http://192.168.1.5 does not.
That matches the design: instructor view is only reachable from the tutor's own Mac (see app.py: local_request()).
"""
import base64
import hashlib
import hmac
import json
import os
import struct
import time

from werkzeug.security import check_password_hash, generate_password_hash

import db

PIN_METHOD = 'pbkdf2:sha256:600000'
RP_ID = 'localhost'
MAX_FAILS, LOCK_SEC = 5, 300
_fails = {}  # key -> [count, locked_until]


# ------------------------------------------------------------------ PINs
def hash_pin(pin):
    return generate_password_hash(pin, method=PIN_METHOD)


def check_pin(stored, pin):
    if not stored or not pin: return False
    if len(stored) == 64 and '$' not in stored:  # legacy unsalted student PIN hash from the first release
        return hmac.compare_digest(stored, hashlib.sha256(('sat-mock:' + pin).encode('utf-8')).hexdigest())
    return check_password_hash(stored, pin)


def locked_for(key):
    """Seconds left on a lockout after too many wrong PINs (0 if not locked)."""
    c = _fails.get(key)
    return max(0, int(c[1] - time.time())) if c and c[1] else 0


def note_fail(key):
    c = _fails.setdefault(key, [0, 0])
    c[0] += 1
    if c[0] >= MAX_FAILS:
        c[0], c[1] = 0, time.time() + LOCK_SEC


def note_ok(key):
    _fails.pop(key, None)


def instructor_pin_set():
    return bool(db.setting('instructor_pin'))


def set_instructor_pin(pin):
    db.set_setting('instructor_pin', hash_pin(pin))


def check_instructor_pin(pin):
    return check_pin(db.setting('instructor_pin'), pin)


def secret_key():
    """Random per-install key for signing session cookies. A fixed key in the source would let anyone on the Wi-Fi
    forge an instructor session."""
    k = db.setting('secret_key')
    if not k:
        k = base64.b64encode(os.urandom(32)).decode('ascii')
        db.set_setting('secret_key', k)
    return k


# ------------------------------------------------------------------ encoding helpers
def b64u(b):
    return base64.urlsafe_b64encode(b).rstrip(b'=').decode('ascii')


def unb64u(s):
    s = str(s)
    return base64.urlsafe_b64decode(s + '=' * (-len(s) % 4))


def challenge():
    return b64u(os.urandom(32))


# ------------------------------------------------------------------ CBOR (the subset WebAuthn uses)
def cbor_decode(data):
    val, _ = _cbor(data, 0)
    return val


def _cbor(d, i):
    ib = d[i]; i += 1
    major, ai = ib >> 5, ib & 31
    if ai < 24: arg = ai
    elif ai == 24: arg = d[i]; i += 1
    elif ai == 25: arg = struct.unpack('>H', d[i:i + 2])[0]; i += 2
    elif ai == 26: arg = struct.unpack('>I', d[i:i + 4])[0]; i += 4
    elif ai == 27: arg = struct.unpack('>Q', d[i:i + 8])[0]; i += 8
    else: raise ValueError('indefinite-length CBOR is not used by WebAuthn')
    if major == 0: return arg, i
    if major == 1: return -1 - arg, i
    if major == 2: return bytes(d[i:i + arg]), i + arg
    if major == 3: return d[i:i + arg].decode('utf-8'), i + arg
    if major == 4:
        out = []
        for _ in range(arg):
            v, i = _cbor(d, i); out.append(v)
        return out, i
    if major == 5:
        out = {}
        for _ in range(arg):
            k, i = _cbor(d, i); v, i = _cbor(d, i); out[k] = v
        return out, i
    if major == 7:
        return {20: False, 21: True, 22: None}.get(arg), i
    raise ValueError('unsupported CBOR major type %d' % major)


# ------------------------------------------------------------------ ECDSA P-256 verify
P = 2 ** 256 - 2 ** 224 + 2 ** 192 + 2 ** 96 - 1
A = P - 3
B = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
N = 0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551
G = (0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296,
     0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5)


def on_curve(x, y):
    return 0 <= x < P and 0 <= y < P and (y * y - (x * x * x + A * x + B)) % P == 0


def _dbl(p):
    X, Y, Z = p
    if not Y: return (0, 1, 0)
    S = 4 * X * Y * Y % P
    M = (3 * X * X + A * pow(Z, 4, P)) % P
    X2 = (M * M - 2 * S) % P
    return (X2, (M * (S - X2) - 8 * pow(Y, 4, P)) % P, 2 * Y * Z % P)


def _add(p, q):
    if not p[2]: return q
    if not q[2]: return p
    U1, U2 = p[0] * q[2] ** 2 % P, q[0] * p[2] ** 2 % P
    S1, S2 = p[1] * q[2] ** 3 % P, q[1] * p[2] ** 3 % P
    if U1 == U2:
        return _dbl(p) if S1 == S2 else (0, 1, 0)
    H, R = (U2 - U1) % P, (S2 - S1) % P
    H2 = H * H % P; H3 = H * H2 % P; U1H2 = U1 * H2 % P
    X3 = (R * R - H3 - 2 * U1H2) % P
    return (X3, (R * (U1H2 - X3) - S1 * H3) % P, H * p[2] * q[2] % P)


def _mul(k, pt):
    res, add = (0, 1, 0), (pt[0], pt[1], 1)
    while k:
        if k & 1: res = _add(res, add)
        add = _dbl(add); k >>= 1
    return res


def _affine_x(p):
    return p[0] * pow(pow(p[2], 2, P), P - 2, P) % P


def der_sig(sig):
    """(r, s) from a DER-encoded ECDSA signature."""
    if sig[0] != 0x30: raise ValueError('not a DER sequence')
    i = 2
    if sig[1] & 0x80: i = 2 + (sig[1] & 0x7f)
    out = []
    for _ in range(2):
        if sig[i] != 0x02: raise ValueError('not a DER integer')
        ln = sig[i + 1]; out.append(int.from_bytes(sig[i + 2:i + 2 + ln], 'big')); i += 2 + ln
    return out[0], out[1]


def ecdsa_verify(x, y, msg, sig_der):
    try:
        r, s = der_sig(sig_der)
    except (ValueError, IndexError):
        return False
    if not (1 <= r < N and 1 <= s < N) or not on_curve(x, y): return False
    e = int.from_bytes(hashlib.sha256(msg).digest(), 'big')
    w = pow(s, N - 2, N)
    pt = _add(_mul(e * w % N, G), _mul(r * w % N, (x, y)))
    if not pt[2]: return False
    return _affine_x(pt) % N == r


# ------------------------------------------------------------------ WebAuthn ceremonies
def registration_options(chal):
    have = [dict(type='public-key', id=r['id']) for r in db.q('SELECT id FROM creds')]
    return dict(challenge=chal, rp=dict(name='Mock SAT instructor', id=RP_ID),
                user=dict(id=b64u(b'instructor'), name='instructor', displayName='Instructor'),
                pubKeyCredParams=[dict(type='public-key', alg=-7)], timeout=60000, attestation='none',
                authenticatorSelection=dict(authenticatorAttachment='platform', userVerification='required', residentKey='discouraged'),
                excludeCredentials=have)


def auth_options(chal):
    return dict(challenge=chal, rpId=RP_ID, timeout=60000, userVerification='required',
                allowCredentials=[dict(type='public-key', id=r['id'], transports=['internal']) for r in db.q('SELECT id FROM creds')])


def _client_data(b64, kind, chal, origin):
    raw = unb64u(b64)
    cd = json.loads(raw.decode('utf-8'))
    if cd.get('type') != kind: raise ValueError('wrong ceremony type')
    if not hmac.compare_digest(str(cd.get('challenge', '')), chal): raise ValueError('challenge mismatch')
    if cd.get('origin') != origin: raise ValueError('origin mismatch: %s' % cd.get('origin'))
    return raw


def _auth_data(ad):
    if ad[:32] != hashlib.sha256(RP_ID.encode('ascii')).digest(): raise ValueError('wrong relying party')
    flags = ad[32]
    if not flags & 0x01: raise ValueError('user presence missing')
    if not flags & 0x04: raise ValueError('Touch ID (user verification) was not performed')
    return flags, struct.unpack('>I', ad[33:37])[0]


def finish_registration(body, chal, origin, label):
    _client_data(body['clientDataJSON'], 'webauthn.create', chal, origin)
    att = cbor_decode(unb64u(body['attestationObject']))
    ad = att['authData']
    flags, count = _auth_data(ad)
    if not flags & 0x40: raise ValueError('no credential data')
    ln = struct.unpack('>H', ad[53:55])[0]
    cred_id, key = ad[55:55 + ln], cbor_decode(ad[55 + ln:])
    if key.get(1) != 2 or key.get(3) != -7 or key.get(-1) != 1: raise ValueError('only ES256 (P-256) keys are supported')
    x, y = int.from_bytes(key[-2], 'big'), int.from_bytes(key[-3], 'big')
    if not on_curve(x, y): raise ValueError('public key is not on P-256')
    db.x('INSERT OR REPLACE INTO creds(id, x, y, sign_count, label, created) VALUES (?,?,?,?,?,?)',
         (b64u(cred_id), '%x' % x, '%x' % y, count, label, time.time()))
    return b64u(cred_id)


def finish_auth(body, chal, origin):
    cred = db.q('SELECT * FROM creds WHERE id=?', (body.get('id', ''),), one=True)
    if not cred: raise ValueError('unknown credential')
    cd_raw = _client_data(body['clientDataJSON'], 'webauthn.get', chal, origin)
    ad = unb64u(body['authenticatorData'])
    _, count = _auth_data(ad)
    msg = ad + hashlib.sha256(cd_raw).digest()
    if not ecdsa_verify(int(cred['x'], 16), int(cred['y'], 16), msg, unb64u(body['signature'])):
        raise ValueError('signature did not verify')
    # Apple's platform authenticator always reports 0; only enforce the counter when the authenticator uses one
    if count and cred['sign_count'] and count <= cred['sign_count']: raise ValueError('signature counter went backwards')
    db.x('UPDATE creds SET sign_count=? WHERE id=?', (count, cred['id']))
    return True
