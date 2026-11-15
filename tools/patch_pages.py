from pathlib import Path

page = Path('index.html')
html = page.read_text(encoding='utf-8')

def replace_once(old, new, label):
    global html
    if old not in html:
        raise SystemExit(f'Patch failed: could not find {label}')
    html = html.replace(old, new, 1)

replace_once("""  :root{
    --pbg:#1c2b33; --pbg2:#17323d; --bg:#0b1a22; --ink:#eaf6fb; --ink2:#9fbdc9;
    --q-prim:#0064e0; --q-hi:#31a9ff; --line:#274553; --ok:#31c48d; --warn:#e2a33b; --bad:#e5484d;
    --r-panel:20px; --r-chip:12px;
  }""", """  :root{
    --pbg:#202024; --pbg2:#29292e; --bg:#09090c; --ink:#f7f7f8; --ink2:#b5b5bd;
    --q-prim:#1684ff; --q-hi:#67b7ff; --line:#414148; --ok:#42d69b; --warn:#f2b84b; --bad:#ff6268;
    --r-panel:28px; --r-chip:18px;
  }""", 'landing theme')
replace_once("""  .card{width:min(760px,100%);background:linear-gradient(180deg,var(--pbg),var(--pbg2));
    border:1px solid var(--line);border-radius:var(--r-panel);padding:22px;box-shadow:0 18px 60px #0008}""", """  .card{width:min(760px,100%);background:linear-gradient(160deg,#29292ff2,#1b1b20f5);
    border:1px solid #ffffff1c;border-radius:30px;padding:28px;box-shadow:0 24px 80px #000a}""", 'landing card')
replace_once('background:var(--q-prim);color:#fff}', 'background:var(--q-prim);color:#fff;border-radius:999px;padding:13px 22px}', 'primary button')
replace_once('background:#ffffff14;color:var(--ink);border:1px solid var(--line)}', 'background:#ffffff0d;color:var(--ink);border:1px solid #ffffff24}', 'secondary button')

replace_once("""  dark:     { panel: '#1c2b33', panel2: '#17323d', ink: '#eaf6fb', ink2: '#9fbdc9', line: '#2c4c5c', accent: '#0064e0', accent2: '#31a9ff', ok: '#31c48d', warn: '#e2a33b', bad: '#e5484d', scrim: 'rgba(8,20,27,0.92)' },
  dim:      { panel: '#131f26', panel2: '#0f1a20', ink: '#cfe4ec', ink2: '#7fa3b1', line: '#223d49', accent: '#0a5cb8', accent2: '#2b8fd6', ok: '#2aa877', warn: '#c8902f', bad: '#c93f44', scrim: 'rgba(5,13,18,0.94)' },
  contrast: { panel: '#000000', panel2: '#0a0a0a', ink: '#ffffff', ink2: '#c9d6db', line: '#6f8892', accent: '#2f9bff', accent2: '#7fd0ff', ok: '#3fe0a0', warn: '#ffc45e', bad: '#ff6b70', scrim: 'rgba(0,0,0,0.96)' },""", """  dark:     { panel: '#202024', panel2: '#29292e', ink: '#f7f7f8', ink2: '#b5b5bd', line: '#414148', accent: '#1684ff', accent2: '#67b7ff', ok: '#42d69b', warn: '#f2b84b', bad: '#ff6268', scrim: 'rgba(22,22,26,0.96)' },
  dim:      { panel: '#18181c', panel2: '#222228', ink: '#ededf0', ink2: '#a0a0aa', line: '#36363e', accent: '#1478e8', accent2: '#5aaaff', ok: '#35c98e', warn: '#dba943', bad: '#e95a62', scrim: 'rgba(16,16,20,0.97)' },
  contrast: { panel: '#101014', panel2: '#1c1c22', ink: '#ffffff', ink2: '#d2d2d8', line: '#666670', accent: '#3999ff', accent2: '#8acbff', ok: '#4de5a6', warn: '#ffd16b', bad: '#ff747a', scrim: 'rgba(8,8,12,0.98)' },""", 'VR palette')

replace_once('panel: null, group: null, rows: 1, cols: 9, page: 0, pages: 1,', 'panel: null, group: null, rows: 1, cols: 8, page: 0, pages: 1,', 'dock columns')
replace_once('const g = this.panel.begin({ bg: T.scrim, round: 34 });', 'const g = this.panel.begin({ bg: T.scrim, round: 48 });', 'dock surface')
replace_once('const padX = 26, gap = 14;', 'const padX = 34, gap = 18;', 'dock spacing')
replace_once("g.text('Quest VR Launcher', 24, top + 22, { size: 22, weight: 700, color: T.ink2 });", "g.text('Apps', 28, top + 23, { size: 22, weight: 700, color: T.ink });", 'dock title')

replace_once("""    this.box(x, y, w, h, 16, hot ? (o.badge ? T.accent : '#ffffff1c') : (o.badge ? '#ffffff14' : '#00000030'), hot ? T.accent2 : null, 2);
    const isz = Math.round(h * 0.5);
    drawIcon(c, icon, x + (w - isz) / 2, y + h * 0.16, isz, hot ? '#fff' : (o.badge ? T.accent2 : T.ink), 0.085);
    this.text(label, x + w / 2, y + h - 12, { size: Math.max(13, Math.round(h * 0.15)), color: hot ? '#fff' : T.ink2, align: 'center', maxW: w - 8 });""", """    this.box(x + 3, y + 2, w - 6, h - 4, 22, hot ? '#ffffff18' : '#ffffff00', hot ? '#ffffff35' : null, 1.5);
    const isz = Math.round(Math.min(w * 0.52, h * 0.50));
    const ix = x + (w - isz) / 2, iy = y + h * 0.10;
    this.box(ix - 9, iy - 7, isz + 18, isz + 18, 22, o.badge ? '#1684ff2c' : '#ffffff12', null, 0);
    drawIcon(c, icon, ix, iy, isz, hot ? '#ffffff' : (o.badge ? T.accent2 : T.ink), 0.085);
    this.text(label, x + w / 2, y + h - 10, { size: Math.max(14, Math.round(h * 0.15)), weight: 600, color: hot ? '#fff' : T.ink2, align: 'center', maxW: w - 8 });""", 'app tiles')

replace_once("""    h.holder.add(h.laserPivot);
    h.gripObj.add(h.holder);""", """    h.gripObj.add(h.holder);
    h.rayObj.add(h.laserPivot);""", 'laser target ray parent')

replace_once("""    // laser placement: start at the ring front in model space, point along targetRay
    const originModel = CTRL.sides[h.side] && CTRL.sides[h.side].cfg.rayOrigin;
    if (originModel) {
      RAY_M.copy(host.matrixWorld).multiply(h.holder.matrix).multiply(TMP_M.makeTranslation(originModel.x, originModel.y, originModel.z));
      const o = originModel.clone().applyMatrix4(TMP_M.copy(h.holder.matrix)).applyMatrix4(host.matrixWorld);
      h.laserPivot.position.copy(h.holder.position).add(TMP_V.copy(originModel).applyQuaternion(h.holder.quaternion));
      h.laserPivot.quaternion.copy(h.holder.quaternion);
      if (!useGrip) { h.laserPivot.position.copy(originModel); h.laserPivot.quaternion.identity(); }
    }
    h.rayOrigin = new THREE.Vector3().setFromMatrixPosition(h.rayObj.matrixWorld);
    h.rayDir = new THREE.Vector3(0, 0, -1).applyQuaternion(new THREE.Quaternion().setFromRotationMatrix(h.rayObj.matrixWorld));""", """    // Exact WebXR target-ray pose: independent from grip-space model transforms.
    h.rayObj.updateWorldMatrix(true, false);
    h.laserPivot.position.set(0, 0, 0);
    h.laserPivot.quaternion.identity();
    h.laserPivot.scale.set(1, 1, 1);
    h.rayOrigin = new THREE.Vector3().setFromMatrixPosition(h.rayObj.matrixWorld);
    h.rayDir = new THREE.Vector3(0, 0, -1).transformDirection(h.rayObj.matrixWorld).normalize();""", 'target ray pose')

replace_once("""    let preferred = S.handedness === 'both' || S.handedness === h.side;
    if (!h.input) return;
    R.pointers.push({ h, ray });
    for (let i = 0; i < panels.length; i++) {
      const hit = panels[i].panel.intersect(ray.o, ray.d);
      if (!hit) continue;
      const score = hit.dist - (panels[i].win ? 0 : 0.02) - (preferred ? 0 : 0.05);
      if (!best || score < best.score) best = { score, hit, win: panels[i].win, h, panel: panels[i].panel };
    }
    // laser length + reticle
    const to = best ? best.hit.dist : 3.0;
    if (h.laser) {
      h.laser.visible = true;
      h.laser.scale.set(1, Math.max(0.05, to), 1);
    }
    if (h.reticle) {
      if (best && best.h === h) {
        best.hit.panel.mesh.getWorldPosition(TMP_V);
        const p = ray.o.clone().add(ray.d.clone().multiplyScalar(best.hit.dist));
        h.reticle.visible = true;
        h.reticle.position.copy(p);
        h.reticle.quaternion.copy(best.hit.panel.mesh.getWorldQuaternion(new THREE.Quaternion()));
      } else if (best && best.h !== h) { h.reticle.visible = false; }
      else h.reticle.visible = false;
    }""", """    const preferred = S.handedness === 'both' || S.handedness === h.side;
    if (!h.input) return;
    R.pointers.push({ h, ray });
    let ownHit = null;
    for (let i = 0; i < panels.length; i++) {
      const hit = panels[i].panel.intersect(ray.o, ray.d);
      if (!hit) continue;
      const score = hit.dist - (panels[i].win ? 0 : 0.02) - (preferred ? 0 : 0.05);
      const candidate = { score, hit, win: panels[i].win, h, panel: panels[i].panel };
      if (!ownHit || score < ownHit.score) ownHit = candidate;
      if (!best || score < best.score) best = candidate;
    }
    const to = ownHit ? ownHit.hit.dist : 3.0;
    if (h.laser) {
      h.laser.visible = true;
      h.laser.scale.set(1, Math.max(0.05, to), 1);
    }
    if (h.reticle) {
      if (ownHit) {
        const p = ray.o.clone().add(ray.d.clone().multiplyScalar(ownHit.hit.dist));
        h.reticle.visible = true;
        h.reticle.position.copy(p);
        h.reticle.quaternion.copy(ownHit.hit.panel.mesh.getWorldQuaternion(new THREE.Quaternion()));
      } else h.reticle.visible = false;
    }""", 'per-hand ray endpoints')

replace_once("""    h.holder.add(h.laserPivot);
    h.gripObj.add(h.holder);
    // laser: a tapered quad pointing along -Z of targetRaySpace""", """    h.gripObj.add(h.holder);
    h.rayObj.add(h.laserPivot);
    const fallback = new THREE.Group();
    const shell = new THREE.Mesh(new THREE.CylinderGeometry(0.018, 0.025, 0.13, 14), new THREE.MeshStandardMaterial({ color: 0x263b49, roughness: 0.62 }));
    shell.rotation.x = Math.PI / 2; shell.position.set(0, -0.03, -0.07); fallback.add(shell);
    const palm = new THREE.Mesh(new THREE.BoxGeometry(0.064, 0.074, 0.052), new THREE.MeshStandardMaterial({ color: 0x344f60, roughness: 0.65 }));
    palm.position.set(0, -0.005, -0.045); fallback.add(palm);
    const ring = new THREE.Mesh(new THREE.TorusGeometry(0.043, 0.005, 8, 24), new THREE.MeshBasicMaterial({ color: 0x67b7ff }));
    ring.rotation.x = Math.PI / 2; ring.position.set(0, 0.02, -0.015); fallback.add(ring);
    fallback.scale.setScalar(0.9); fallback.visible = true; h.fallback = fallback; h.holder.add(fallback);
    // laser: a tapered quad pointing along -Z of targetRaySpace""", 'fallback Touch controller')

replace_once("""    if (model) model.visible = !CTRL.displayMode;
    animateRig(CTRL.sides[h.side], h.input, h.prev, dt, h);""", """    if (model) model.visible = !CTRL.displayMode;
    if (h.fallback) h.fallback.visible = !model || !model.visible;
    animateRig(CTRL.sides[h.side], h.input, h.prev, dt, h);""", 'fallback visibility')

# WebXR's xr-standard layout exposes the thumbstick at axes 2 and 3.
replace_once(
    "out.sx = A[sa[0]] || 0; out.sy = A[sa[1]] || 0;",
    "const stickAxes = gp.mapping === 'xr-standard' && A.length >= 4 ? [2, 3] : sa;\\n  out.sx = A[stickAxes[0]] || 0; out.sy = A[stickAxes[1]] || 0;",
    'Quest thumbstick axes'
)

# The controller beam is a plane rotated into the target-ray direction (-Z).
replace_once("const geo = new THREE.PlaneGeometry(0.012, 1, 1, 8);",
             "const geo = new THREE.PlaneGeometry(0.004, 1, 1, 8);", 'pointer beam width')
replace_once("h.laser.rotation.x = -Math.PI / 2;",
             "h.laser.rotation.x = Math.PI / 2;", 'forward pointer direction')
replace_once("depthWrite: false, toneMapped: false, fog: false }));",
             "depthWrite: false, depthTest: false, toneMapped: false, fog: false }));", 'pointer visibility')

page.write_text(html, encoding='utf-8')
