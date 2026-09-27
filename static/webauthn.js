/* Touch ID for the instructor lock (WebAuthn platform authenticator). Server side: auth.py. Works on http://localhost only. */
(function () {
  'use strict';
  function b64u(buf) {
    var s = '', b = new Uint8Array(buf);
    for (var i = 0; i < b.length; i++) s += String.fromCharCode(b[i]);
    return btoa(s).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
  }
  function unb64u(s) {
    s = s.replace(/-/g, '+').replace(/_/g, '/'); while (s.length % 4) s += '=';
    var bin = atob(s), out = new Uint8Array(bin.length);
    for (var i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
    return out.buffer;
  }
  function post(url, body) {
    return fetch(url, {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(body || {})})
      .then(function (r) { return r.json().then(function (j) { if (!r.ok || j.ok === false) throw new Error(j.error || 'Request failed'); return j; }); });
  }
  function supported() { return !!(window.PublicKeyCredential && navigator.credentials && window.isSecureContext); }

  window.TouchID = {
    supported: supported,
    signIn: function (base) {
      return post(base + 'auth-begin').then(function (o) {
        o.challenge = unb64u(o.challenge);
        o.allowCredentials = o.allowCredentials.map(function (c) { return {type: c.type, id: unb64u(c.id), transports: c.transports}; });
        return navigator.credentials.get({publicKey: o});
      }).then(function (cred) {
        return post(base + 'auth-finish', {id: b64u(cred.rawId), clientDataJSON: b64u(cred.response.clientDataJSON),
          authenticatorData: b64u(cred.response.authenticatorData), signature: b64u(cred.response.signature)});
      });
    },
    enroll: function (base) {
      return post(base + 'register-begin').then(function (o) {
        o.challenge = unb64u(o.challenge); o.user.id = unb64u(o.user.id);
        o.excludeCredentials = o.excludeCredentials.map(function (c) { return {type: c.type, id: unb64u(c.id)}; });
        return navigator.credentials.create({publicKey: o});
      }).then(function (cred) {
        return post(base + 'register-finish', {id: b64u(cred.rawId), clientDataJSON: b64u(cred.response.clientDataJSON),
          attestationObject: b64u(cred.response.attestationObject)});
      });
    }
  };
})();
