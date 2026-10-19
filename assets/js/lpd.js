// Lake poster renderer v3: OpenFreeMap vector tiles (OpenMapTiles schema, OSM data) + Nominatim lookup.
// Runs in any tab without a strict CSP. Same look as the first 6 posters. Output 5400x7200 PNG.
window.LPD = (() => {
  // Displate variant: 4200x5880 (1.4:1), full-bleed map, no frame line, text kept away from edges
  const W = 4200, H = 5880, M = 0, FB = 4620, FW = W, FH = FB, K = 0.78, SAFE = 260;
  const status = {}, out = {};
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  // ---------- minimal protobuf / MVT decoder ----------
  function reader(buf) {
    let p = 0; const u = new Uint8Array(buf);
    const varint = () => { let r = 0, s = 0, b; do { b = u[p++]; r += (b & 0x7f) * Math.pow(2, s); s += 7; } while (b & 0x80); return r; };
    return {
      get pos() { return p; }, set pos(v) { p = v; }, len: u.length, u, varint,
      tag() { const t = varint(); return [Math.floor(t / 8), t & 7]; },
      bytes() { const l = varint(); const s = p; p += l; return [s, p]; },
      skip(w) { if (w === 0) varint(); else if (w === 1) p += 8; else if (w === 2) { const l = varint(); p += l; } else if (w === 5) p += 4; },
    };
  }
  const td = new TextDecoder();
  function decodeValue(r, end) {
    let v = null; const dv = new DataView(r.u.buffer, r.u.byteOffset);
    while (r.pos < end) {
      const [f, w] = r.tag();
      if (f === 1) { const [s, e] = r.bytes(); v = td.decode(r.u.subarray(s, e)); }
      else if (f === 2) { v = dv.getFloat32(r.pos, true); r.pos += 4; }
      else if (f === 3) { v = dv.getFloat64(r.pos, true); r.pos += 8; }
      else if (f === 4 || f === 5) v = r.varint();
      else if (f === 6) { const z = r.varint(); v = (z % 2) ? -(z + 1) / 2 : z / 2; }
      else if (f === 7) v = !!r.varint();
      else r.skip(w);
    }
    return v;
  }
  function packed(r) { const [s, e] = r.bytes(); const a = []; const save = r.pos; r.pos = s; while (r.pos < e) a.push(r.varint()); r.pos = e; return a; }
  function geom(cmds) { // -> array of rings/lines (arrays of [x,y])
    const parts = []; let cur = null, x = 0, y = 0, i = 0;
    while (i < cmds.length) {
      const c = cmds[i++], id = c & 7, n = c >> 3;
      if (id === 1 || id === 2) {
        for (let k = 0; k < n; k++) {
          const dx = cmds[i++], dy = cmds[i++];
          x += (dx % 2) ? -(dx + 1) / 2 : dx / 2; y += (dy % 2) ? -(dy + 1) / 2 : dy / 2;
          if (id === 1) { cur = [[x, y]]; parts.push(cur); } else cur.push([x, y]);
        }
      } else if (id === 7) { if (cur) cur.push(cur[0].slice()); }
    }
    return parts;
  }
  function decodeTile(buf, want) {
    const r = reader(buf); const layers = {};
    while (r.pos < r.len) {
      const [f, w] = r.tag();
      if (f !== 3) { r.skip(w); continue; }
      const [ls, le] = r.bytes(); const save = le;
      r.pos = ls;
      let name = '', extent = 4096; const keys = [], vals = [], feats = [];
      while (r.pos < le) {
        const [lf, lw] = r.tag();
        if (lf === 1) { const [s, e] = r.bytes(); name = td.decode(r.u.subarray(s, e)); }
        else if (lf === 2) { const [s, e] = r.bytes(); feats.push([s, e]); }
        else if (lf === 3) { const [s, e] = r.bytes(); keys.push(td.decode(r.u.subarray(s, e))); }
        else if (lf === 4) { const [s, e] = r.bytes(); const sp = r.pos; r.pos = s; vals.push(decodeValue(r, e)); r.pos = e; }
        else if (lf === 5) extent = r.varint();
        else r.skip(lw);
      }
      if (want.includes(name)) {
        const fs = [];
        for (const [s, e] of feats) {
          r.pos = s; let tags = [], type = 0, cmds = [];
          while (r.pos < e) {
            const [ff, fw] = r.tag();
            if (ff === 2) tags = packed(r); else if (ff === 3) type = r.varint(); else if (ff === 4) cmds = packed(r); else r.skip(fw);
          }
          const props = {}; for (let k = 0; k < tags.length; k += 2) props[keys[tags[k]]] = vals[tags[k + 1]];
          fs.push({ type, props, parts: geom(cmds) });
        }
        layers[name] = { extent, feats: fs };
      }
      r.pos = save;
    }
    return layers;
  }
  // ---------- data ----------
  let tileURL = null;
  async function tilejson() {
    if (tileURL) return tileURL;
    const j = await (await fetch('https://tiles.openfreemap.org/planet')).json();
    tileURL = j.tiles[0]; return tileURL;
  }
  async function nominatim(q) {
    const u = 'https://nominatim.openstreetmap.org/search?format=jsonv2&limit=5&q=' + encodeURIComponent(q);
    const j = await (await fetch(u)).json();
    return j;
  }
  // web mercator in "world units" 0..1
  const mx = lon => (lon + 180) / 360;
  const my = lat => { const s = Math.sin(lat * Math.PI / 180); return 0.5 - Math.log((1 + s) / (1 - s)) / (4 * Math.PI); };
  const unlat = y => (Math.atan(Math.sinh(Math.PI * (1 - 2 * y))) * 180 / Math.PI);
  function view(bbox, fit) { // bbox [S,N,W,E]
    const x0 = mx(bbox[2]), x1 = mx(bbox[3]), y0 = my(bbox[1]), y1 = my(bbox[0]);
    const s = Math.min(fit * FW / (x1 - x0), fit * FH / (y1 - y0));
    const cx = (x0 + x1) / 2, cy = (y0 + y1) / 2;
    return { s, cx, cy, X0: cx - FW / 2 / s, X1: cx + FW / 2 / s, Y0: cy - FH / 2 / s, Y1: cy + FH / 2 / s };
  }
  async function getTiles(v, zmax) {
    let z = zmax;
    const n = zz => { const t = 2 ** zz; return (Math.floor(v.X1 * t) - Math.floor(v.X0 * t) + 1) * (Math.floor(v.Y1 * t) - Math.floor(v.Y0 * t) + 1); };
    while (n(z) > 260 && z > 8) z--;
    const t = 2 ** z, url = await tilejson(); const list = [];
    for (let x = Math.floor(v.X0 * t); x <= Math.floor(v.X1 * t); x++) for (let y = Math.floor(v.Y0 * t); y <= Math.floor(v.Y1 * t); y++) list.push([x, y]);
    const tiles = []; let i = 0;
    const worker = async () => {
      while (i < list.length) {
        const [x, y] = list[i++];
        for (let a = 0; a < 4; a++) {
          try {
            const r = await fetch(url.replace('{z}', z).replace('{x}', x).replace('{y}', y));
            if (r.status === 204 || r.status === 404) break;
            if (!r.ok) throw new Error(r.status);
            tiles.push({ z, x, y, L: decodeTile(await r.arrayBuffer(), ['water', 'waterway', 'transportation', 'place']) });
            break;
          } catch (e) { await sleep(1500); }
        }
        status.__tiles = tiles.length + '/' + list.length + ' z' + z;
      }
    };
    await Promise.all([worker(), worker(), worker(), worker(), worker(), worker()]);
    return { z, tiles };
  }
  // ---------- fonts ----------
  async function fonts() {
    if (window.__lpFonts) return;
    const css = await (await fetch('https://fonts.googleapis.com/css2?family=Lora:wght@400;500&family=Poppins:wght@400;500;600&display=swap')).text();
    const seen = new Set();
    for (const m of css.matchAll(/@font-face\s*{([^}]*)}/g)) {
      const f = m[1]; const fam = f.match(/font-family:\s*'([^']+)'/)[1], wt = f.match(/font-weight:\s*(\d+)/)[1];
      const uni = (f.match(/unicode-range:\s*([^;]+)/) || [])[1] || '';
      if (uni && !/U\+0000-00FF/.test(uni)) continue;
      if (seen.has(fam + wt)) continue; seen.add(fam + wt);
      const ff = new FontFace(fam, `url(${f.match(/url\(([^)]+)\)/)[1]})`, { weight: wt }); await ff.load(); document.fonts.add(ff);
    }
    window.__lpFonts = true;
  }
  // ---------- render ----------
  const ROAD = { motorway: 11*0.78, trunk: 10*0.78, primary: 8*0.78, secondary: 6.5*0.78, tertiary: 5*0.78, minor: 2.4*0.78 };
  const MAJOR = new Set(['motorway', 'trunk', 'primary', 'secondary']);
  function render(v, data, o) {
    const C = document.createElement('canvas'); C.width = W; C.height = H; const g = C.getContext('2d');
    g.fillStyle = '#EDE8DE'; g.fillRect(0, 0, W, H);
    g.save(); g.beginPath(); g.rect(M, M, FW, FH); g.clip();
    g.fillStyle = '#F4F0E8'; g.fillRect(M, M, FW, FH);
    g.lineJoin = 'round'; g.lineCap = 'round';
    const t = 2 ** data.z; const rs = o.roadScale || 1;
    const each = (fn) => {
      for (const tl of data.tiles) {
        const x0 = M + (tl.x / t - v.X0) * v.s, y0 = M + (tl.y / t - v.Y0) * v.s, sz = v.s / t;
        g.save(); g.beginPath(); g.rect(x0, y0, sz, sz); g.clip();
        fn(tl, (layer) => { const e = layer.extent; return ([px, py]) => [x0 + px / e * sz, y0 + py / e * sz]; });
        g.restore();
      }
    };
    const path = (parts, P, close) => { g.beginPath(); for (const pt of parts) { pt.forEach((q, i) => { const [x, y] = P(q); i ? g.lineTo(x, y) : g.moveTo(x, y); }); if (close) g.closePath(); } };
    // waterways
    each((tl, PF) => { const L = tl.L.waterway; if (!L) return; const P = PF(L);
      for (const f of L.feats) { if (f.props.brunnel === 'tunnel') continue; if (!o.streams && !/^(river|canal)$/.test(f.props.class)) continue; g.strokeStyle = '#9FC0CF'; g.lineWidth = (f.props.class === 'river' ? 10 : 5)*K; path(f.parts, P, false); g.stroke(); } });
    // water
    each((tl, PF) => { const L = tl.L.water; if (!L) return; const P = PF(L);
      for (const f of L.feats) { if (f.type !== 3 || f.props.class === 'swimming_pool') continue; path(f.parts, P, true); g.fillStyle = '#9FC0CF'; g.fill('evenodd'); g.strokeStyle = '#3F6B7D'; g.lineWidth = 3*K; g.stroke(); } });
    // roads, minor first
    for (const pass of ['minor', 'tertiary', 'secondary', 'primary', 'trunk', 'motorway']) {
      each((tl, PF) => { const L = tl.L.transportation; if (!L) return; const P = PF(L);
        for (const f of L.feats) {
          let c = f.props.class; if (c === 'service' && false) c = 'minor';
          if (c !== pass || f.type !== 2) continue;
          if (f.props.brunnel === 'tunnel') continue;
          g.strokeStyle = MAJOR.has(c) ? 'rgba(43,38,34,0.85)' : 'rgba(43,38,34,0.55)';
          g.lineWidth = ROAD[c] * (MAJOR.has(c) ? 1 : rs) * (f.props.ramp ? 0.6 : 1);
          path(f.parts, P, false); g.stroke();
        } });
    }
    // places
    const places = new Map();
    for (const tl of data.tiles) { const L = tl.L.place; if (!L) continue;
      for (const f of L.feats) { if (!/^(city|town)$/.test(f.props.class)) continue; const name = f.props['name:latin'] || f.props.name; if (!name || places.has(name)) continue;
        const [px, py] = f.parts[0][0]; if (px < 0 || py < 0 || px > L.extent || py > L.extent) continue;
        places.set(name, { name, cls: f.props.class, rank: f.props.rank || 99, X: (tl.x + px / L.extent) / t, Y: (tl.y + py / L.extent) / t }); } }
    const pl = [...places.values()].sort((a, b) => (a.cls === b.cls ? 0 : a.cls === 'city' ? -1 : 1) || a.rank - b.rank);
    const boxes = []; g.font = '600 50px Poppins'; g.letterSpacing = '6px'; g.textAlign = 'center'; g.textBaseline = 'middle';
    for (const p of pl.slice(0, 24)) {
      if (boxes.length >= (o.maxLabels || 9)) break;
      const x = M + (p.X - v.X0) * v.s, y = M + (p.Y - v.Y0) * v.s, tx = p.name.toUpperCase();
      const w = g.measureText(tx).width + 32, h = 70, bx = [x - w / 2, y - h / 2, x + w / 2, y + h / 2];
      if (bx[0] < SAFE || bx[2] > W - SAFE || bx[1] < SAFE || bx[3] > FB - 60) continue;
      if (boxes.some(b => !(bx[2] < b[0] || bx[0] > b[2] || bx[3] < b[1] || bx[1] > b[3]))) continue;
      boxes.push(bx); g.lineWidth = 12; g.strokeStyle = 'rgba(244,240,232,0.92)'; g.strokeText(tx, x, y); g.fillStyle = '#2B2622'; g.fillText(tx, x, y);
    }
    g.restore();
        g.textAlign = 'center'; g.textBaseline = 'alphabetic'; g.fillStyle = '#2B2622';
    let size = 260; const title = o.title.toUpperCase();
    do { g.font = `400 ${size}px Lora`; g.letterSpacing = Math.round(size * 0.12) + 'px'; size -= 10; } while (g.measureText(title).width > W - 2 * SAFE - 200 && size > 120);
    g.fillText(title, W / 2, 5040);
    let ss = 72; const sub = o.sub.toUpperCase();
    do { g.font = `500 ${ss}px Poppins`; g.letterSpacing = Math.round(ss * 0.2) + 'px'; ss -= 4; } while (g.measureText(sub).width > W - 2 * SAFE - 300 && ss > 40);
    g.fillStyle = '#6E6259'; g.fillText(sub, W / 2, 5240);
    g.fillStyle = '#C0806A'; g.fillRect(W / 2 - 94, 5310, 188, 6);
    g.font = '400 62px Poppins'; g.letterSpacing = '5px'; g.fillStyle = '#4A423C'; g.fillText(o.coords, W / 2, 5440);
    g.font = '400 38px Poppins'; g.letterSpacing = '1px'; g.fillStyle = '#8A8079'; g.textAlign = 'right';
    g.fillText('Map data © OpenStreetMap contributors', W - SAFE, 5640);
    return C;
  }
  const fmt = (lat, lon) => `${Math.abs(lat).toFixed(4)}° ${lat >= 0 ? 'N' : 'S'}  ·  ${Math.abs(lon).toFixed(4)}° ${lon >= 0 ? 'E' : 'W'}`;
  // job: {q (nominatim query) | bbox [S,N,W,E], title, sub, fit, zmax, roadScale, maxLabels}
  async function make(job) {
    const T = job.key || job.title; status[T] = 'fonts'; await fonts();
    let bbox = job.bbox, hit = null;
    if (!bbox) {
      status[T] = 'lookup';
      const res = await nominatim(job.q);
      hit = res.find(r => /water|reservoir|lake/.test((r.type || '') + (r.category || '') + (r.addresstype || ''))) || res[0];
      if (!hit) throw new Error('not found ' + job.q);
      bbox = hit.boundingbox.map(Number);
    }
    const v = view(bbox, job.fit || 0.82);
    status[T] = 'tiles'; const data = await getTiles(v, job.zmax || 13);
    status[T] = 'render';
    const lat = unlat(v.cy), lon = v.cx * 360 - 180;
    const C = render(v, data, { title: job.title, sub: job.sub, coords: fmt(lat, lon), roadScale: job.roadScale, maxLabels: job.maxLabels, streams: job.streams });
    const blob = await new Promise(r => C.toBlob(r, 'image/jpeg', 0.95));
    const s = document.createElement('canvas'); s.width = 900; s.height = 1260; s.getContext('2d').drawImage(C, 0, 0, 900, 1260);
    out[T] = { blob, prev: s.toDataURL('image/jpeg', 0.85), hit: hit && { name: hit.display_name, type: hit.type, bbox }, z: data.z, n: data.tiles.length, v, data, job };
    status[T] = 'done ' + (blob.size / 1e6).toFixed(1) + 'MB z' + data.z + ' tiles ' + data.tiles.length;
    return out[T];
  }
  function show(T) { // put preview on page for screenshot
    let im = document.getElementById('lp_prev'); if (!im) { im = document.createElement('img'); im.id = 'lp_prev'; im.style = 'position:fixed;left:0;top:0;height:100vh;z-index:99999;background:#fff'; document.body.appendChild(im); }
    im.src = out[T].prev; return 'shown';
  }
  function send(T) { window.__pw.postMessage({ lp: true, title: T, blob: out[T].blob, prev: out[T].prev }, 'https://printify.com'); return 'sent ' + T; }
  async function rerender(T, patch) { const o0 = out[T]; const job = Object.assign({}, o0.job, patch || {}); const lat = unlat(o0.v.cy), lon = o0.v.cx * 360 - 180; const C = render(o0.v, o0.data, { title: job.title, sub: job.sub, coords: fmt(lat, lon), roadScale: job.roadScale, maxLabels: job.maxLabels, streams: job.streams }); o0.blob = await new Promise(r => C.toBlob(r, 'image/jpeg', 0.95)); const s = document.createElement('canvas'); s.width = 900; s.height = 1260; s.getContext('2d').drawImage(C, 0, 0, 900, 1260); o0.prev = s.toDataURL('image/jpeg', 0.85); o0.job = job; return 'ok'; }
  return { make, rerender, show, send, status, out, nominatim, decodeTile, fonts };
})();
'LPD ready';
