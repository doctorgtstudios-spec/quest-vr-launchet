/* Quest VR Launcher: robust Touch tracking + visible target-ray pointer.
   Injected by the Pages build; the original app remains otherwise unchanged. */
(function () {
  'use strict';
  if (window.__questTrackingFixInstalled) return;
  window.__questTrackingFixInstalled = true;

  function addFallbackController(h) {
    if (h.fallbackRoot) return;
    const root = new THREE.Group();
    const shell = new THREE.Mesh(
      new THREE.CylinderGeometry(0.019, 0.026, 0.13, 14),
      new THREE.MeshStandardMaterial({ color: 0x263b49, metalness: 0.25, roughness: 0.55 })
    );
    shell.rotation.x = Math.PI / 2;
    shell.position.set(0, -0.035, -0.075);
    root.add(shell);

    const palm = new THREE.Mesh(
      new THREE.BoxGeometry(0.064, 0.075, 0.052),
      new THREE.MeshStandardMaterial({ color: 0x344f60, metalness: 0.18, roughness: 0.6 })
    );
    palm.position.set(0, -0.006, -0.045);
    root.add(palm);

    const ring = new THREE.Mesh(
      new THREE.TorusGeometry(0.045, 0.006, 8, 28),
      new THREE.MeshBasicMaterial({ color: 0x66d9ff })
    );
    ring.rotation.x = Math.PI / 2;
    ring.position.set(0, 0.022, -0.018);
    root.add(ring);

    const trigger = new THREE.Mesh(
      new THREE.BoxGeometry(0.032, 0.012, 0.025),
      new THREE.MeshStandardMaterial({ color: 0x8ba9b8, roughness: 0.45 })
    );
    trigger.position.set(0, 0.033, -0.073);
    root.add(trigger);

    root.scale.setScalar(0.9);
    h.fallbackRoot = root;
    h.fallbackTrigger = trigger;
  }

  function addPointer(h) {
    if (h.pointerBeam) return;
    const geometry = new THREE.BufferGeometry().setFromPoints([
      new THREE.Vector3(0, 0, -0.025),
      new THREE.Vector3(0, 0, -3)
    ]);
    const material = new THREE.LineBasicMaterial({
      color: 0x70dcff, transparent: true, opacity: 0.92,
      depthTest: false, depthWrite: false
    });
    const beam = new THREE.Line(geometry, material);
    beam.frustumCulled = false;
    beam.renderOrder = 1000;
    h.rayObj.add(beam);
    h.pointerBeam = beam;
  }

  const originalSync = syncControllers;
  syncControllers = function (session, dt) {
    originalSync(session, dt);
    Object.keys(CTRL.holders).forEach(function (key) {
      const h = CTRL.holders[key];
      if (!h || !h.rayObj) return;
      addPointer(h);
      addFallbackController(h);

      const sideData = CTRL.sides[h.side];
      const detailed = sideData && sideData.root;
      const showFallback = !detailed || !detailed.visible;
      const fallbackHost = h.useGrip && h.gripObj ? h.gripObj : h.rayObj;
      if (h.fallbackRoot.parent !== fallbackHost) fallbackHost.add(h.fallbackRoot);
      h.fallbackRoot.visible = !!h.input && showFallback;
      if (h.fallbackTrigger && h.input) {
        h.fallbackTrigger.position.y = 0.033 - 0.008 * Math.min(1, h.input.trigger || 0);
      }

      // WebXR's xr-standard layout puts the thumbstick on axes 2/3.
      const gp = h.input && h.input.gp;
      if (gp && gp.mapping === 'xr-standard' && gp.axes && gp.axes.length >= 4) {
        let sx = gp.axes[2] || 0;
        let sy = gp.axes[3] || 0;
        if (S.invertStickY) sy = -sy;
        const dz = S.deadzone || 0;
        h.input.sx = Math.abs(sx) < dz ? 0 : sx;
        h.input.sy = Math.abs(sy) < dz ? 0 : sy;
      }
    });
  };

  const originalHover = updateHoverAndActions;
  updateHoverAndActions = function (dt) {
    originalHover(dt);
    Object.keys(CTRL.holders).forEach(function (key) {
      const h = CTRL.holders[key];
      if (!h || !h.pointerBeam) return;
      const active = R.mode === 'vr' && !!h.input && !!h.rayOrigin && !!h.rayDir;
      h.pointerBeam.visible = active;
      // The original beam was parented to the grip/model and could point away
      // from the target ray. Use the tracked targetRaySpace directly instead.
      if (h.laser) h.laser.visible = false;
      if (!active) return;
      let distance = 3;
      if (R.hover && R.hover.h === h && R.hover.hit && Number.isFinite(R.hover.hit.dist)) {
        distance = Math.max(0.08, Math.min(8, R.hover.hit.dist));
      }
      h.pointerBeam.geometry.setFromPoints([
        new THREE.Vector3(0, 0, -0.025),
        new THREE.Vector3(0, 0, -distance)
      ]);
      h.pointerBeam.geometry.computeBoundingSphere();
    });
  };

  if (R && R.diagLog) R.diagLog.push('tracking fix active: target-ray pointer + fallback controller');
})();