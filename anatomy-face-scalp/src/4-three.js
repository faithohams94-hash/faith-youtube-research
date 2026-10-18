// ================= 3D tracer =================
// Real head scan (Lee Perry-Smith, Infinite Realities, CC BY 3.0). Every structure from the
// atlas is projected from the lateral drawing onto the scan surface and pushed in to its depth.
const T3 = { started: false, ready: false, side2: false, skin: 0.35, hide: new Set(["derm"]), sel: null, trace: null, S: {}, labels: [], pick: [] };

function chainList(list) {
  const pts = d => (d.replace(/^~/, "").match(/-?\d*\.?\d+/g) || []).map(Number);
  const out = [list[0]];
  for (let i = 1; i < list.length; i++) {
    const a = pts(out[out.length - 1]), b = pts(list[i]);
    if (/Z\s*$/.test(list[i])) break;
    if (Math.hypot(a[a.length - 2] - b[0], a[a.length - 1] - b[1]) < 6) out.push(list[i]); else break;
  }
  return out;
}
function chainD(list) { return chainList(list).map((d, i) => (i ? d.replace(/^~?M/, "L") : d.replace(/^~/, ""))).join(" "); }

// hidden svg used to sample path geometry
let _sampPath = null;
function sampEl() {
  if (_sampPath) return _sampPath;
  const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  svg.setAttribute("aria-hidden", "true"); svg.style.cssText = "position:absolute;width:0;height:0;overflow:hidden";
  document.body.appendChild(svg);
  _sampPath = document.createElementNS("http://www.w3.org/2000/svg", "path"); svg.appendChild(_sampPath);
  return _sampPath;
}
function samplePath(d, step = 3) {
  const _sampPath = sampEl();
  _sampPath.setAttribute("d", d);
  const L = _sampPath.getTotalLength(), n = Math.max(2, Math.ceil(L / step)), out = [];
  for (let i = 0; i <= n; i++) { const p = _sampPath.getPointAtLength(L * i / n); out.push([p.x, p.y]); }
  return out;
}
function pathBBox(d) { const p = sampEl(); p.setAttribute("d", d); return p.getBBox(); }

// ---------- surface height maps (lateral rays along x) ----------
const HM = { R: 0.02, Y0: -4.1, Z0: -2.75 };
function buildHeightmap(geo) {
  const pos = geo.attributes.position.array, idx = geo.index ? geo.index.array : null;
  const { R, Y0, Z0 } = HM, NY = Math.ceil(8.3 / R), NZ = Math.ceil(5.5 / R);
  const mx = new Float32Array(NY * NZ).fill(-1e9), mn = new Float32Array(NY * NZ).fill(1e9);
  const ntri = idx ? idx.length / 3 : pos.length / 9;
  for (let t = 0; t < ntri; t++) {
    const a = idx ? idx[t * 3] : t * 3, b = idx ? idx[t * 3 + 1] : t * 3 + 1, c = idx ? idx[t * 3 + 2] : t * 3 + 2;
    const ax = pos[a * 3], ay = pos[a * 3 + 1], az = pos[a * 3 + 2], bx = pos[b * 3], by = pos[b * 3 + 1], bz = pos[b * 3 + 2], cx = pos[c * 3], cy = pos[c * 3 + 1], cz = pos[c * 3 + 2];
    if (Math.abs(ax) > 1.95 || Math.abs(bx) > 1.95 || Math.abs(cx) > 1.95) continue; // ignore shoulders
    const det = (by - ay) * (cz - az) - (cy - ay) * (bz - az);
    if (Math.abs(det) < 1e-12) continue;
    const i0 = Math.max(0, Math.ceil((Math.min(ay, by, cy) - Y0) / R)), i1 = Math.min(NY - 1, Math.floor((Math.max(ay, by, cy) - Y0) / R));
    const j0 = Math.max(0, Math.ceil((Math.min(az, bz, cz) - Z0) / R)), j1 = Math.min(NZ - 1, Math.floor((Math.max(az, bz, cz) - Z0) / R));
    for (let i = i0; i <= i1; i++) for (let j = j0; j <= j1; j++) {
      const py = Y0 + i * R, pz = Z0 + j * R;
      const l1 = ((py - ay) * (cz - az) - (cy - ay) * (pz - az)) / det, l2 = ((by - ay) * (pz - az) - (py - ay) * (bz - az)) / det;
      if (l1 < -1e-6 || l2 < -1e-6 || l1 + l2 > 1 + 1e-6) continue;
      const x = ax + l1 * (bx - ax) + l2 * (cx - ax), k = i * NZ + j;
      if (x > mx[k]) mx[k] = x;
      if (x < mn[k]) mn[k] = x;
    }
  }
  Object.assign(HM, { NY, NZ, mx, mn });
}
function hAt(side, i, j) {
  if (i < 0 || j < 0 || i >= HM.NY || j >= HM.NZ) return null;
  const v = (side > 0 ? HM.mx : HM.mn)[i * HM.NZ + j];
  return Math.abs(v) > 1e8 ? null : v;
}
function hNear(side, i, j) {
  const v = hAt(side, i, j); if (v != null) return v;
  for (let r = 1; r <= 4; r++) for (let di = -r; di <= r; di++) for (let dj = -r; dj <= r; dj++) { const w = hAt(side, i + di, j + dj); if (w != null) return w; }
  return null;
}
function surf(side, y, z) {
  const fi = (y - HM.Y0) / HM.R, fj = (z - HM.Z0) / HM.R, i = Math.floor(fi), j = Math.floor(fj), u = fi - i, v = fj - j;
  const a = hNear(side, i, j), b = hNear(side, i + 1, j), c = hNear(side, i, j + 1), d = hNear(side, i + 1, j + 1);
  if (a == null || b == null || c == null || d == null) return null;
  const x = a * (1 - u) * (1 - v) + b * u * (1 - v) + c * (1 - u) * v + d * u * v;
  const k = 2, fy = ((hNear(side, i + k, j) ?? x) - (hNear(side, i - k, j) ?? x)) / (2 * k * HM.R), fz = ((hNear(side, i, j + k) ?? x) - (hNear(side, i, j - k) ?? x)) / (2 * k * HM.R);
  const n = new THREE.Vector3(side, -side * fy, -side * fz).normalize();
  return { x, n };
}
// lateral drawing (600 x 720) -> model space
const map2D = (X, Y) => ({ y: 3.97 - (Y - 58) * 0.0101, z: 2.59 - (X - 70) * 0.00958 });
function to3D(X, Y, depth, side) {
  if (Y > 655) return null;
  const { y, z } = map2D(X, Y), s = surf(side, y, z);
  if (!s) return null;
  const p = new THREE.Vector3(s.x, y, z);
  if (depth <= 0.16) p.addScaledVector(s.n, -depth);
  else { p.addScaledVector(s.n, -0.1); p.x -= side * (depth - 0.1); }
  return { p, n: s.n };
}

const DEEP = { ica: .55, ijv: .5, maxillary_a: .42, maxillary_v: .4, pterygoid_plexus: .42, middle_meningeal_a: .5, inf_alveolar_a: .24, inf_alveolar_n: .25, lingual_a: .55, sup_ophthalmic_v: .45, deep_facial_v: .2, buccal_n: .28, auriculotemporal_n: .3, infraorbital_n: .22, infraorbital_a: .22, cavernous_sinus: 1.0, emissary_v: .14, occipital_v: .16, cca: .32, cn12: .3, cn11: .28, sphenomandibular_lig: .38 };
const SUPER = { cn11: .07, eca: .2, cn7: .12, rmv: .13, post_auricular_n: .07, occipital_a: .075, greater_occipital_n: .08, ejv: .05, scm: .06, common_facial_v: .14, sup_thyroid_a: .2, parotid_duct: .07, cn7_temporal: .06, cn7_zygomatic: .07, cn7_buccal: .075, cn7_marginal: .08, cn7_cervical: .07, lesser_occipital_n: .07, great_auricular_n: .06 };
const PATCH = { frontalis: .03, occipitalis: .03, galea: .028, auricularis: .03, orb_oculi: .03, corrugator: .05, procerus: .03, nasalis: .03, llsan: .035, lls: .035, zyg_minor: .032, zyg_major: .034, lao: .085, risorius: .03, buccinator: .1, orb_oris: .045, dao: .03, dli: .035, mentalis: .04, platysma: .022, temporalis: .13, masseter: .11, scm: .06, digastric_post: .26, parotid: .045, submand_gland: .12, mandible: .16, zyg_arch: .1, mastoid: .1, skull: .2, styloid: .3, hyoid: .2, thyroid_cart: .15, stylohyoid: .24, mylohyoid: .3, hyoglossus: .4, sup_constrictor: .5, lat_pterygoid: .4, med_pterygoid: .34, buccal_fat: .13, trapezius: .045, splenius: .12, semispinalis: .2, inf_oblique: .3 };
function depthOf(id, deep) {
  const o = S[id];
  if (deep) return DEEP[id] ?? .25;
  if (SUPER[id] != null) return SUPER[id];
  return { artery: .055, vein: .045, nerve: .065 }[o.sys] ?? .05;
}
const COL3 = { artery: 0xc41e2c, vein: 0x2a58cc, nerve: 0xf0c020, muscle: 0xb24a40, ref: 0xa4554a, gland: 0xe0c070, bone: 0xece2c6 };

function fiberTexture() {
  const c = document.createElement("canvas"); c.width = c.height = 64;
  const g = c.getContext("2d");
  g.fillStyle = "#b5503f"; g.fillRect(0, 0, 64, 64);
  for (let y = 0; y < 64; y += 8) { g.fillStyle = "rgba(90,20,15,.55)"; g.fillRect(0, y, 64, 2); g.fillStyle = "rgba(255,210,190,.22)"; g.fillRect(0, y + 4, 64, 1); }
  const t = new THREE.CanvasTexture(c); t.wrapS = t.wrapT = THREE.RepeatWrapping; return t;
}

// ---------- geometry builders ----------
function buildTube(id, raw, side, mat) {
  const deep = raw[0] === "~", d = raw.replace(/^~/, "");
  const closed = /Z\s*$/.test(d);
  const pts = [], nrm = [];
  for (const [X, Y] of samplePath(d, 3)) { const r = to3D(X, Y, depthOf(id, deep), side); if (r) { pts.push(r.p); nrm.push(r.n); } }
  if (pts.length < 3) return null;
  const curve = new THREE.CatmullRomCurve3(pts, closed, "centripetal");
  const rad = (S[id].wd || 2.4) * 0.0105;
  const geo = new THREE.TubeGeometry(curve, Math.min(220, pts.length * 2), rad, 8, closed);
  const m = new THREE.Mesh(geo, mat);
  m.userData = { id, pts, nrm };
  return m;
}
function subpaths(d) { return d.replace(/^~/, "").split(/(?=M)/).map(x => x.trim()).filter(Boolean); }
function bboxOf(pts) { let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9; pts.forEach(([x, y]) => { x0 = Math.min(x0, x); y0 = Math.min(y0, y); x1 = Math.max(x1, x); y1 = Math.max(y1, y); }); return { x0, y0, x1, y1 }; }
function triangulate2D(d, maxEdge) {
  // outline polygons; a subpath inside the previous one is a hole (ring muscles)
  const polys = subpaths(d).map(sp => { const p = samplePath(sp, 2.5); p.pop(); return p; }).filter(p => p.length > 2);
  const shapes = [];
  polys.forEach(p => {
    const b = bboxOf(p), last = shapes[shapes.length - 1];
    if (last && b.x0 > last.b.x0 && b.x1 < last.b.x1 && b.y0 > last.b.y0 && b.y1 < last.b.y1) last.holes.push(p);
    else shapes.push({ c: p, holes: [], b });
  });
  const V = [], T = [];
  shapes.forEach(sh => {
    const contour = sh.c.map(([x, y]) => new THREE.Vector2(x, y)), holes = sh.holes.map(h => h.map(([x, y]) => new THREE.Vector2(x, y)));
    if (THREE.ShapeUtils.isClockWise(contour)) contour.reverse();
    holes.forEach(h => { if (!THREE.ShapeUtils.isClockWise(h)) h.reverse(); });
    const all = contour.concat(...holes), base = V.length;
    all.forEach(v => V.push([v.x, v.y]));
    THREE.ShapeUtils.triangulateShape(contour, holes).forEach(t => T.push([t[0] + base, t[1] + base, t[2] + base]));
  });
  // split long edges so the sheet follows the curve of the face
  const mid = new Map();
  const midpoint = (a, b) => { const k = a < b ? a + "_" + b : b + "_" + a; if (!mid.has(k)) { V.push([(V[a][0] + V[b][0]) / 2, (V[a][1] + V[b][1]) / 2]); mid.set(k, V.length - 1); } return mid.get(k); };
  const len = (a, b) => Math.hypot(V[a][0] - V[b][0], V[a][1] - V[b][1]);
  let out = T, guard = 0;
  while (guard++ < 12) {
    let changed = false; const next = [];
    for (const [a, b, c] of out) {
      const e = [[len(a, b), a, b, c], [len(b, c), b, c, a], [len(c, a), c, a, b]].sort((x, y) => y[0] - x[0])[0];
      if (e[0] <= maxEdge) { next.push([a, b, c]); continue; }
      const m = midpoint(e[1], e[2]); next.push([e[1], m, e[3]], [m, e[2], e[3]]); changed = true;
    }
    out = next; if (!changed) break;
  }
  return { V, T: out };
}
function buildPatch(id, raw, side, mat, ang) {
  const depth = PATCH[id] ?? .04, { V, T } = triangulate2D(raw, 4.5);
  const ca = Math.cos((ang || 0) * Math.PI / 180), sa = Math.sin((ang || 0) * Math.PI / 180);
  const pos = [], uv = [], map = new Array(V.length).fill(-1), pts = [], nrm = [], index = [];
  V.forEach(([X, Y], i) => {
    const r = to3D(X, Y, depth, side); if (!r) return;
    map[i] = pos.length / 3; pos.push(r.p.x, r.p.y, r.p.z); uv.push((ca * X + sa * Y) / 7, (-sa * X + ca * Y) / 7); pts.push(r.p); nrm.push(r.n);
  });
  T.forEach(([a, b, c]) => { if (map[a] >= 0 && map[b] >= 0 && map[c] >= 0) index.push(map[a], map[b], map[c]); });
  if (!index.length) return null;
  const geo = new THREE.BufferGeometry();
  geo.setAttribute("position", new THREE.Float32BufferAttribute(pos, 3));
  geo.setAttribute("uv", new THREE.Float32BufferAttribute(uv, 2));
  geo.setIndex(index); geo.computeVertexNormals();
  const m = new THREE.Mesh(geo, mat);
  const step = Math.max(1, Math.floor(pts.length / 60));
  m.userData = { id, pts: pts.filter((_, i) => i % step === 0), nrm: nrm.filter((_, i) => i % step === 0), patch: true };
  return m;
}

function buildStructures(scene) {
  const fib = fiberTexture();
  for (const id in S) {
    const o = S[id]; if (!o.lat || id === "skull") continue;
    const rec = { id, sys: o.sys, groups: {}, mats: [], meshes: [] };
    let mat;
    if (["artery", "vein", "nerve"].includes(o.sys) || o.line) {
      const c = o.line ? COL3.gland : COL3[o.sys];
      mat = new THREE.MeshStandardMaterial({ color: c, roughness: o.sys === "nerve" ? .5 : .32, metalness: .05, emissive: 0x000000, transparent: true, opacity: 1 });
    } else if (o.sys === "muscle" || o.sys === "ref") {
      const gland = id === "parotid" || id === "submand_gland";
      mat = new THREE.MeshStandardMaterial({ color: gland ? COL3.gland : (id === "galea" ? 0xd8cdb4 : 0xffffff), map: gland || id === "galea" ? null : fib, roughness: .75, side: THREE.DoubleSide, transparent: true, opacity: id === "platysma" ? .55 : o.sys === "ref" ? .82 : .9, emissive: 0x000000, depthWrite: true, polygonOffset: true, polygonOffsetFactor: 1 });
    } else if (o.sys === "bone") {
      mat = new THREE.MeshStandardMaterial({ color: COL3.bone, roughness: .85, side: THREE.DoubleSide, transparent: true, opacity: .95, emissive: 0x000000 });
    } else if (o.sys === "derm") {
      mat = new THREE.MeshBasicMaterial({ color: new THREE.Color(o.col), transparent: true, opacity: .35, side: THREE.DoubleSide, depthWrite: false });
    }
    rec.mats.push(mat); rec.base = { opacity: mat.opacity, color: new THREE.Color(o.sys === "derm" ? o.col : (["artery", "vein", "nerve"].includes(o.sys) ? COL3[o.sys] : 0xd06050)) };
    for (const side of [1, -1]) {
      const grp = new THREE.Group(); grp.userData.side = side;
      for (const raw of o.lat) {
        let m = null;
        if (o.sys === "bone" && o.pt) {
          const c = raw.match(/-?\d*\.?\d+/g).map(Number); const r = to3D(c[0] + 4.5, c[1], .1, side);
          if (r) { m = new THREE.Mesh(new THREE.SphereGeometry(.05, 12, 8), new THREE.MeshStandardMaterial({ color: 0x222222, emissive: 0x000000, transparent: true })); m.position.copy(r.p); m.userData = { id, pts: [r.p], nrm: [r.n] }; rec.mats.push(m.material); }
        } else if (["artery", "vein", "nerve"].includes(o.sys) || o.line) m = buildTube(id, raw, side, mat);
        else if (o.sys === "derm") m = buildPatch(id, raw, side, mat, 0);
        else m = buildPatch(id, raw, side, mat, o.ang);
        if (m) { m.renderOrder = o.sys === "derm" ? 5 : (o.sys === "muscle" || o.sys === "ref" ? 1 : 2); grp.add(m); rec.meshes.push(m); }
      }
      rec.groups[side] = grp; scene.add(grp);
    }
    if (o.sys === "derm") rec.meshes.forEach(m => { // lift sensory map just outside the skin
      const p = m.geometry.attributes.position, side = m.parent.userData.side;
      for (let i = 0; i < p.count; i++) { const y = p.getY(i), z = p.getZ(i), s = surf(side, y, z); if (s) { p.setX(i, s.x + side * .012); } }
      p.needsUpdate = true;
    });
    T3.S[id] = rec;
  }
}

// ---------- scene ----------
function init3D() {
  if (T3.started) return; T3.started = true;
  const load = $("#t3load");
  if (!window.THREE || !THREE.OrbitControls || !THREE.GLTFLoader) { load.innerHTML = "The 3D viewer could not load. Check your connection and reopen the page."; return; }
  if (!window.HEAD_ASSETS) { load.textContent = "The 3D head data is missing from this copy."; return; }
  const stage = $("#t3stage");
  let renderer;
  try { renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true }); }
  catch (e) { load.textContent = "This device's browser does not support 3D (WebGL)."; return; }
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  renderer.outputEncoding = THREE.sRGBEncoding;
  renderer.domElement.style.touchAction = "none";
  stage.insertBefore(renderer.domElement, stage.firstChild);
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(32, 1, .1, 100);
  camera.position.set(10, 1.6, 1.2);
  const controls = new THREE.OrbitControls(camera, renderer.domElement);
  controls.target.set(0, 1, .3); controls.enableDamping = true; controls.dampingFactor = .08;
  controls.addEventListener("start", () => { if (T3.trace && T3.trace.anim) T3.trace.anim.cam = null; });
  controls.minDistance = 1.6; controls.maxDistance = 22; controls.rotateSpeed = .7;
  scene.add(new THREE.HemisphereLight(0xfff4ea, 0x3a2a28, .85));
  const key = new THREE.DirectionalLight(0xffffff, .9); key.position.set(6, 6, 7); scene.add(key);
  const fill = new THREE.DirectionalLight(0xbfd8ff, .45); fill.position.set(-7, 2, 3); scene.add(fill);
  const rim = new THREE.DirectionalLight(0xffffff, .5); rim.position.set(0, 4, -8); scene.add(rim);
  Object.assign(T3, { renderer, scene, camera, controls });
  const resize = () => { const w = stage.clientWidth, h = stage.clientHeight; renderer.setSize(w, h, false); renderer.domElement.style.width = w + "px"; renderer.domElement.style.height = h + "px"; camera.aspect = w / h; camera.updateProjectionMatrix(); };
  new ResizeObserver(resize).observe(stage); resize();

  const tl = new THREE.TextureLoader();
  const skinMap = tl.load(HEAD_ASSETS.skin); skinMap.flipY = false; skinMap.encoding = THREE.sRGBEncoding;
  const nMap = tl.load(HEAD_ASSETS.normal); nMap.flipY = false;
  const bin = Uint8Array.from(atob(HEAD_ASSETS.glb), c => c.charCodeAt(0)).buffer;
  new THREE.GLTFLoader().parse(bin, "", g => {
    const head = g.scene.getObjectByName("LeePerrySmith") || g.scene.children.find(c => c.isMesh);
    head.material = new THREE.MeshStandardMaterial({ map: skinMap, normalMap: nMap, normalScale: new THREE.Vector2(.7, .7), roughness: .6, transparent: true, opacity: T3.skin, depthWrite: false });
    head.renderOrder = 10;
    scene.add(head); T3.head = head;
    load.textContent = "Placing vessels, nerves and muscles…";
    setTimeout(() => {
      buildHeightmap(head.geometry);
      buildStructures(scene);
      T3.ready = true; load.remove();
      applyLayers3D(); setSkin3D(T3.skin);
      fill3DSelect();
      const first = (location.hash.slice(1) in S && S[location.hash.slice(1)].steps) ? location.hash.slice(1) : "facial_a";
      select3D(first, true);
    }, 30);
  }, () => { load.textContent = "The 3D head could not be read on this device."; });

  // picking: tap without dragging
  let down = null;
  renderer.domElement.addEventListener("pointerdown", e => { down = { x: e.clientX, y: e.clientY, t: Date.now(), n: (down && down.n) || 0 }; });
  renderer.domElement.addEventListener("pointerup", e => {
    if (!down || Math.hypot(e.clientX - down.x, e.clientY - down.y) > 7 || Date.now() - down.t > 600) return;
    const id = pick3D(e.clientX, e.clientY); if (id) select3D(id, !!S[id].steps);
  });
  const loop = t => {
    requestAnimationFrame(loop);
    if ($("#tab-t3d").hidden) return;
    tick3D(t); controls.update(); renderer.render(scene, camera); placeLabels3D();
  };
  requestAnimationFrame(loop);
}

function visibleMeshes() {
  const out = [];
  for (const id in T3.S) {
    const r = T3.S[id]; if (T3.hide.has(r.sys)) continue;
    r.meshes.forEach(m => { if (m.parent.visible) out.push(m); });
  }
  return out;
}
function pick3D(cx, cy) {
  const rect = T3.renderer.domElement.getBoundingClientRect();
  const ndc = new THREE.Vector2(((cx - rect.left) / rect.width) * 2 - 1, -((cy - rect.top) / rect.height) * 2 + 1);
  const rc = new THREE.Raycaster(); rc.setFromCamera(ndc, T3.camera);
  const hits = rc.intersectObjects(visibleMeshes().filter(m => !m.userData.patch || S[m.userData.id].sys !== "derm" || !T3.hide.has("derm")), false);
  const lines = hits.find(h => ["artery", "vein", "nerve"].includes(S[h.object.userData.id].sys));
  if (lines) return lines.object.userData.id;
  // screen-space nearest line within 22px (thin tubes are hard to hit by finger)
  let best = null, bd = 22 * 22; const v = new THREE.Vector3();
  for (const m of visibleMeshes()) {
    if (!["artery", "vein", "nerve"].includes(S[m.userData.id].sys)) continue;
    for (const p of m.userData.pts) {
      v.copy(p).project(T3.camera); if (v.z > 1) continue;
      const sx = rect.left + (v.x + 1) / 2 * rect.width, sy = rect.top + (1 - v.y) / 2 * rect.height, d = (sx - cx) ** 2 + (sy - cy) ** 2;
      if (d < bd) { bd = d; best = m.userData.id; }
    }
  }
  return best || (hits[0] && hits[0].object.userData.id) || null;
}

// ---------- layers, skin, highlight ----------
function setSkin3D(v) { T3.skin = v; if (T3.head) { T3.head.material.opacity = v; T3.head.material.depthWrite = v > .97; T3.head.visible = v > .01; } }
function applyLayers3D() {
  for (const id in T3.S) {
    const r = T3.S[id], show = !T3.hide.has(r.sys) || id === T3.sel || (T3.ctx && T3.ctx.has(id));
    r.groups[1].visible = show; r.groups[-1].visible = show && T3.side2;
  }
}
function focus3D() {
  const sel = T3.sel, ctx = T3.ctx || new Set();
  for (const id in T3.S) {
    const r = T3.S[id];
    r.mats.forEach(m => {
      const isSel = id === sel, isCtx = ctx.has(id);
      m.opacity = sel ? (isSel || isCtx ? Math.max(r.base.opacity, .95) : (r.sys === "derm" ? .12 : .14)) : r.base.opacity;
      if (m.emissive) m.emissive.setHex(0x000000);
      m.depthWrite = !sel || isSel || isCtx;
    });
  }
  applyLayers3D();
}
function tick3D(t) {
  const k = .5 + .5 * Math.sin(t / 260);
  const sel = T3.sel && T3.S[T3.sel];
  if (sel) sel.mats.forEach(m => m.emissive && m.emissive.copy(sel.base.color).multiplyScalar(.25 + .45 * k));
  if (T3.ctx) T3.ctx.forEach(id => { const r = T3.S[id]; if (r && id !== T3.sel) r.mats.forEach(m => m.emissive && m.emissive.copy(r.base.color).multiplyScalar(.12 + .3 * k)); });
  if (T3.ring) { T3.ring.scale.setScalar(1 + .25 * k); T3.ring.material.opacity = .5 + .5 * k; }
  const tr = T3.trace;
  if (tr && tr.anim) {
    const a = tr.anim, f = Math.min(1, (t - (a.t0 ?? (a.t0 = t))) / a.dur), e = f < .5 ? 2 * f * f : 1 - (-2 * f + 2) ** 2 / 2;
    tr.u = a.from + (a.to - a.from) * e;
    const p = tr.curve.getPointAt(tr.u);
    tr.marker.position.copy(p); tr.halo.position.copy(p);
    tr.trail.geometry.setDrawRange(0, Math.floor(tr.u * tr.segs) * 8 * 6);
    T3.controls.target.lerp(p, .12);
    if (a.cam) T3.camera.position.lerp(a.cam, .06);
    if (f >= 1 && !a.cam) tr.anim = null;
    if (f >= 1 && a.cam && T3.camera.position.distanceTo(a.cam) < .05) tr.anim = null;
  }
}

// ---------- labels ----------
function nearestPt(id, ref) {
  const r = T3.S[id]; if (!r) return null; let best = null, bd = Infinity;
  for (const m of r.meshes) { if (!m.parent.visible) continue; for (const p of m.userData.pts) { const d = ref ? p.distanceToSquared(ref) : 0; if (d < bd) { bd = d; best = p; } if (!ref) return p; } }
  return best;
}
function setLabels3D(ids, types = {}) {
  const box = $("#t3labels"); box.innerHTML = ""; T3.labels = [];
  ids.forEach((id, i) => {
    const el = h("div", { class: "t3lbl" + (i === 0 ? " main" : "") + (types[id] ? " rel-" + types[id] : "") }, esc(S[id] ? S[id].n.replace(/ \((V1|V2|V3|C2|C3|C2, C3|mastication)\)$/, "") : id));
    box.appendChild(el); T3.labels.push({ id, el });
  });
}
function placeLabels3D() {
  if (!T3.labels.length) return;
  const rect = T3.renderer.domElement.getBoundingClientRect(), v = new THREE.Vector3();
  const ref = T3.trace ? T3.trace.marker.position : null;
  T3.labels.forEach((L, i) => {
    const p = i === 0 && ref ? ref : nearestPt(L.id, ref);
    if (!p) { L.el.style.display = "none"; return; }
    v.copy(p).project(T3.camera);
    if (v.z > 1 || Math.abs(v.x) > 1.05 || Math.abs(v.y) > 1.05) { L.el.style.display = "none"; return; }
    L.el.style.display = "";
    L.x = (v.x + 1) / 2 * rect.width; L.y = (1 - v.y) / 2 * rect.height;
  });
  // push overlapping labels apart vertically
  const shown = T3.labels.filter(L => L.el.style.display !== "none").sort((a, b) => a.y - b.y);
  for (let i = 1; i < shown.length; i++) for (let j = 0; j < i; j++) {
    const a = shown[j], b = shown[i];
    const gap = isPhone() ? 17 : 22; if (Math.abs(a.x - b.x) < 150 && b.y - a.y < gap) b.y = a.y + gap;
  }
  shown.forEach(L => { L.el.style.transform = `translate(${L.x}px, ${L.y}px)`; });
}

// ---------- selection & tracing ----------
function relHTML(id, i) {
  const r = (REL[id] || [])[i]; if (!r) return "";
  return ["p", "d", "s", "w"].filter(k => r[k] && r[k].length).map(k => `<div class="rel rel-${k}"><b>${REL_LABEL[k]}</b>${r[k].map(x => { const q = relParts(x); return q.id ? `<button class="relchip" data-go3="${q.id}">${esc(q.text)}</button>` : `<span class="relchip plain">${esc(q.text)}</span>`; }).join("")}</div>`).join("");
}
function fill3DSelect() {
  const sel = $("#t3sel"); sel.innerHTML = "";
  const groups = {};
  for (const id in S) if (S[id].lat && ["artery", "vein", "nerve"].includes(S[id].sys) || S[id].line || S[id].sys === "muscle") (groups[S[id].sys === "muscle" ? "Muscles: " + S[id].grp : S[id].grp] = groups[S[id].sys === "muscle" ? "Muscles: " + S[id].grp : S[id].grp] || []).push(id);
  for (const g in groups) {
    const og = h("optgroup", { label: g });
    groups[g].forEach(id => og.appendChild(h("option", { value: id }, esc(S[id].n) + (S[id].steps ? " ▸" : ""))));
    sel.appendChild(og);
  }
  sel.onchange = () => select3D(sel.value, true);
}
function select3D(id, trace) {
  stopTrace3D();
  T3.sel = id; T3.ctx = new Set();
  const o = S[id];
  $("#t3sel").value = id;
  $("#t3name").textContent = o.n;
  $("#t3sum").textContent = o.sum || "";
  $("#t3kind").innerHTML = `<i style="background:${o.sys === "derm" ? o.col : SYS[o.sys].col}"></i>${SYS[o.sys].label}`;
  $("#t3steps").innerHTML = o.steps ? o.steps.map((s, i) => `<li data-i="${i}">${esc(s[2])}</li>`).join("") : "";
  $$("#t3steps li").forEach(li => li.onclick = () => { if (!T3.trace) startTrace3D(id); goStep3D(+li.dataset.i); });
  $("#t3now").innerHTML = o.steps ? "" : `<p class="note">No step-by-step course for this one. ${o.f && o.f.r ? "<b>Relations:</b> " + esc(o.f.r) : ""}</p>`;
  $("#t3notes").onclick = () => { showTab("explore"); select(id, { trace: !!o.steps }); window.scrollTo({ top: 0 }); };
  $(".t3bar").hidden = !o.steps;
  setLabels3D([id]);
  focus3D();
  if (o.steps && trace) startTrace3D(id); else flyTo3D(nearestPt(id), id);
}
function flyTo3D(p, id) {
  if (!p) return;
  const r = T3.S[id]; const m = r && r.meshes[0]; let n = new THREE.Vector3(1, 0, 0);
  if (m) { const i = m.userData.pts.indexOf(p); if (i >= 0) n = m.userData.nrm[i].clone(); }
  T3.controls.target.copy(p);
  T3.camera.position.copy(p).addScaledVector(n.setY(n.y * .5).normalize(), 7).add(new THREE.Vector3(0, .6, 0));
}
function startTrace3D(id) {
  stopTrace3D();
  const o = S[id], list = chainList(o.lat);
  const pts = [], nrm = [];
  list.forEach((raw, si) => {
    const deep = raw[0] === "~";
    samplePath(raw.replace(/^~/, ""), 3).forEach(([X, Y], k) => { if (si && !k) return; const r = to3D(X, Y, depthOf(id, deep) - .015, 1); if (r) { pts.push(r.p); nrm.push(r.n); } });
  });
  if (pts.length < 3) return;
  const curve = new THREE.CatmullRomCurve3(pts, false, "centripetal");
  const segs = Math.min(300, pts.length * 2), rad = (o.wd || 2.4) * .0105 * 1.9;
  const trail = new THREE.Mesh(new THREE.TubeGeometry(curve, segs, rad, 8, false), new THREE.MeshBasicMaterial({ color: new THREE.Color(COL3[o.sys] || 0xffffff).lerp(new THREE.Color(0xffffff), .45), transparent: true, opacity: .5, depthTest: false }));
  trail.renderOrder = 20; trail.geometry.setDrawRange(0, 0);
  const marker = new THREE.Mesh(new THREE.SphereGeometry(rad * 1.6 + .02, 20, 14), new THREE.MeshBasicMaterial({ color: 0xffffff, depthTest: false }));
  const halo = new THREE.Mesh(new THREE.SphereGeometry(rad * 2.4 + .03, 20, 14), new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: .16, depthTest: false }));
  marker.renderOrder = halo.renderOrder = 21;
  T3.scene.add(trail, marker, halo);
  // parameter of each step along the curve (nearest sample)
  const N = 400, cp = []; for (let i = 0; i <= N; i++) cp.push(curve.getPointAt(i / N));
  const steps = o.steps.map(s => {
    const r = to3D(s[0], s[1], depthOf(id, false), 1); if (!r) return 0;
    let bi = 0, bd = Infinity; cp.forEach((p, i) => { const d = p.distanceToSquared(r.p); if (d < bd) { bd = d; bi = i; } }); return bi / N;
  });
  for (let i = 1; i < steps.length; i++) if (steps[i] < steps[i - 1]) steps[i] = steps[i - 1];
  T3.trace = { id, curve, segs, trail, marker, halo, steps, nrm, pts, i: -1, u: 0, playing: false, timer: null, anim: null };
  goStep3D(0);
}
function goStep3D(i) {
  const tr = T3.trace; if (!tr) return;
  i = Math.max(0, Math.min(tr.steps.length - 1, i)); tr.i = i;
  const to = tr.steps[i], p = tr.curve.getPointAt(to);
  // camera from the outward normal near this point
  let bi = 0, bd = Infinity; tr.pts.forEach((q, k) => { const d = q.distanceToSquared(p); if (d < bd) { bd = d; bi = k; } });
  const n = tr.nrm[bi].clone(); n.y *= .4; n.normalize();
  const cam = p.clone().addScaledVector(n, 6.6).add(new THREE.Vector3(0, .7, 0));
  tr.anim = { from: tr.u, to, dur: reduceMotion ? 1 : 1300, cam };
  const s = S[tr.id].steps[i];
  T3.ctx = new Set([...(s[3] || []), ...relIds(tr.id, i)].filter(k => T3.S[k]));
  focus3D();
  setLabels3D([tr.id, ...T3.ctx], relTypes(tr.id, i));
  // pierce ring
  if (T3.ring) { T3.scene.remove(T3.ring); T3.ring = null; }
  const r = (REL[tr.id] || [])[i];
  if (r && r.p && r.p.length) {
    const tan = tr.curve.getTangentAt(to);
    const ring = new THREE.Mesh(new THREE.TorusGeometry(.11, .018, 10, 32), new THREE.MeshBasicMaterial({ color: 0xffe066, transparent: true, depthTest: false }));
    ring.position.copy(p); ring.quaternion.setFromUnitVectors(new THREE.Vector3(0, 0, 1), tan); ring.renderOrder = 22;
    T3.scene.add(ring); T3.ring = ring;
  }
  $("#t3now").innerHTML = `<div class="t3stepno">Step ${i + 1} of ${tr.steps.length}</div><p class="t3steptxt">${esc(s[2])}</p>${relHTML(tr.id, i)}`;
  $$("#t3now [data-go3]").forEach(b => b.onclick = () => select3D(b.dataset.go3, !!S[b.dataset.go3].steps));
  $("#t3count").textContent = `${i + 1} / ${tr.steps.length}`;
  $$("#t3steps li").forEach((li, k) => { li.classList.toggle("cur", k === i); li.classList.toggle("done", k < i); });
}
function play3D() {
  const tr = T3.trace; if (!tr) return;
  tr.playing = true; $("#t3play").textContent = "❚❚ Pause";
  if (tr.i >= tr.steps.length - 1) goStep3D(0);
  clearInterval(tr.timer);
  tr.timer = setInterval(() => { if (tr.i >= tr.steps.length - 1) pause3D(); else goStep3D(tr.i + 1); }, 5200);
}
function pause3D() { const tr = T3.trace; if (!tr) return; tr.playing = false; clearInterval(tr.timer); $("#t3play").textContent = "▶ Play"; }
function stopTrace3D() {
  const tr = T3.trace; if (!tr) return;
  clearInterval(tr.timer); T3.scene.remove(tr.trail, tr.marker, tr.halo);
  if (T3.ring) { T3.scene.remove(T3.ring); T3.ring = null; }
  T3.trace = null; $("#t3play").textContent = "▶ Play";
}
const VIEWS3 = { L: [9.5, 1.4, .8], F: [0, 1.2, 10], R: [-9.5, 1.4, .8], B: [0, 1.6, -10], T: [0, 11, .6] };
function view3D(k) {
  if (!T3.ready) return;
  const v = VIEWS3[k]; T3.controls.target.set(0, .9, .2); T3.camera.position.set(...v);
  if (k === "R" && !T3.side2) toggleSide3D(true);
}
function toggleSide3D(on) { T3.side2 = on; $("#t3side").setAttribute("aria-pressed", on); applyLayers3D(); }

function bind3DUI() {
  $("#t3skin").addEventListener("input", e => setSkin3D(e.target.value / 100));
  $("#t3prev").onclick = () => T3.trace ? goStep3D(T3.trace.i - 1) : null;
  $("#t3next").onclick = () => { if (!T3.trace && T3.sel && S[T3.sel].steps) startTrace3D(T3.sel); else if (T3.trace) goStep3D(T3.trace.i + 1); };
  $("#t3play").onclick = () => { if (!T3.trace && T3.sel && S[T3.sel].steps) { startTrace3D(T3.sel); play3D(); } else if (T3.trace) T3.trace.playing ? pause3D() : play3D(); };
  $$("#t3views button").forEach(b => b.onclick = () => view3D(b.dataset.v));
  $("#t3side").onclick = () => toggleSide3D(!T3.side2);
  $$("#t3layers .chip").forEach(b => b.onclick = () => {
    const k = b.dataset.l; T3.hide.has(k) ? T3.hide.delete(k) : T3.hide.add(k);
    b.setAttribute("aria-pressed", !T3.hide.has(k)); applyLayers3D();
  });
  // swipe the step bar on phones
  let sw = null; const bar = $(".t3bar");
  bar.addEventListener("touchstart", e => { sw = e.touches[0].clientX; }, { passive: true });
  bar.addEventListener("touchend", e => { if (sw == null || !T3.trace) return; const dx = e.changedTouches[0].clientX - sw; sw = null; if (Math.abs(dx) > 45) goStep3D(T3.trace.i + (dx < 0 ? 1 : -1)); }, { passive: true });
}
