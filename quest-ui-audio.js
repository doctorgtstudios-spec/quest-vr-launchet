/* Quest-style UI sound feedback for controller and desktop interactions.
   Original synthesized tones; not copied Meta/Oculus audio assets. */
(function () {
  'use strict';
  if (window.__questUiAudioInstalled) return;
  window.__questUiAudioInstalled = true;

  const KEY = 'quest-vr-ui-sounds';
  let enabled = true;
  try { enabled = localStorage.getItem(KEY) !== 'off'; } catch (_) {}
  let ctx = null;
  let master = null;
  let lastHover = 0;

  function audio() {
    if (!enabled) return null;
    const Ctx = window.AudioContext || window.webkitAudioContext;
    if (!Ctx) return null;
    if (!ctx) {
      ctx = new Ctx();
      master = ctx.createGain();
      master.gain.value = 0.22;
      master.connect(ctx.destination);
    }
    if (ctx.state === 'suspended') ctx.resume().catch(function () {});
    return ctx;
  }

  function tone(freq, endFreq, duration, volume, wave, delay) {
    const c = audio();
    if (!c) return;
    const start = c.currentTime + (delay || 0);
    const osc = c.createOscillator();
    const gain = c.createGain();
    osc.type = wave || 'sine';
    osc.frequency.setValueAtTime(freq, start);
    if (endFreq && endFreq !== freq) {
      osc.frequency.exponentialRampToValueAtTime(Math.max(30, endFreq), start + duration);
    }
    gain.gain.setValueAtTime(0.0001, start);
    gain.gain.exponentialRampToValueAtTime(Math.max(0.0002, volume), start + 0.008);
    gain.gain.exponentialRampToValueAtTime(0.0001, start + duration);
    osc.connect(gain);
    gain.connect(master);
    osc.start(start);
    osc.stop(start + duration + 0.015);
  }

  const sounds = {
    hover: function () {
      const now = performance.now();
      if (now - lastHover < 85) return;
      lastHover = now;
      tone(980, 760, 0.045, 0.12, 'sine');
    },
    click: function () {
      tone(620, 430, 0.075, 0.20, 'triangle');
      tone(1120, 840, 0.045, 0.055, 'sine', 0.012);
    },
    confirm: function () {
      tone(520, 660, 0.10, 0.16, 'sine');
      tone(780, 980, 0.13, 0.12, 'sine', 0.075);
    },
    back: function () {
      tone(470, 310, 0.11, 0.14, 'sine');
    },
    grab: function () {
      tone(360, 520, 0.07, 0.10, 'triangle');
    }
  };

  function play(name) {
    if (!enabled || !sounds[name]) return;
    sounds[name]();
  }

  // Enable audio on the first genuine user gesture.
  ['pointerdown', 'keydown', 'touchstart'].forEach(function (type) {
    window.addEventListener(type, function () { audio(); }, { passive: true, once: true, capture: true });
  });

  // Desktop/browser landing UI feedback.
  document.addEventListener('pointerover', function (event) {
    if (event.target && event.target.closest && event.target.closest('button,a,[role="button"],.app-tile')) play('hover');
  }, true);
  document.addEventListener('click', function (event) {
    if (event.target && event.target.closest && event.target.closest('button,a,[role="button"],.app-tile')) play('click');
  }, true);

  // Hook the WebXR session created by the launcher. These events come directly
  // from the Touch controller trigger/grip, not from a simulated mouse.
  function attachSession(session) {
    if (!session || session.__questUiSoundsAttached) return;
    session.__questUiSoundsAttached = true;
    session.addEventListener('selectstart', function () { play('click'); });
    session.addEventListener('squeezestart', function () { play('grab'); });
    session.addEventListener('inputsourceschange', function () { audio(); });
  }

  function hookXR() {
    if (!navigator.xr || navigator.xr.__questUiSoundsHooked) return;
    const xr = navigator.xr;
    try {
      const original = xr.requestSession.bind(xr);
      Object.defineProperty(xr, 'requestSession', {
        configurable: true,
        value: async function () {
          const session = await original.apply(xr, arguments);
          attachSession(session);
          return session;
        }
      });
      Object.defineProperty(xr, '__questUiSoundsHooked', { value: true });
    } catch (_) {
      // If the browser locks the XR object, DOM sound feedback still works.
    }
  }

  hookXR();
  if (!navigator.xr) {
    window.addEventListener('load', hookXR, { once: true });
  }

  window.QuestUISounds = {
    play: play,
    setEnabled: function (value) {
      enabled = !!value;
      try { localStorage.setItem(KEY, enabled ? 'on' : 'off'); } catch (_) {}
      if (enabled) audio();
      return enabled;
    },
    isEnabled: function () { return enabled; }
  };
})();