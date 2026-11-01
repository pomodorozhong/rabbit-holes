// Save this entire file in Chrome DevTools > Sources > Snippets.
// Running it installs the commands and previews loaded entries; it removes nothing.
// Remove up to 3 entries: playlistCleaner.start({ preview: false, limit: 3 })
// Clear the list:        playlistCleaner.start({ preview: false })
// Stop:                 playlistCleaner.stop()
// Inspect progress:     playlistCleaner.status()
// Use a loaded /playlist?list=... page where you can remove videos.
// Defaults to the exact English label "Remove from <playlist name>".
// If the title cannot be detected, supply the exact removal label:
// playlistCleaner.start({ preview: false, limit: 3, removeLabel: 'Remove from My list' })
// Keep the playlist tab in the foreground, with its All filter selected.
// Counts changes in the displayed list, not server-confirmed deletions.
(() => {
  if ([window.playlistCleaner, window.watchLaterCleaner].some(api => api?.status?.().running)) {
    console.warn('[Playlist Cleaner] Already running. Stop it before replacing it.');
    return;
  }

  const prefix = '[Playlist Cleaner]';
  const rowSelector = 'ytd-playlist-video-renderer';
  const menuSelector = 'ytd-popup-container ytd-menu-popup-renderer';
  const state = {
    running: false, phase: 'idle', playlistId: '', playlistName: '', removeLabel: '',
    observedRemovals: 0, lastTitle: '', message: '',
  };
  let controller;
  let target;

  const normalize = text => text.replace(/\s+/g, ' ').trim();
  const visible = element => element.isConnected && element.getClientRects().length > 0 &&
    getComputedStyle(element).visibility !== 'hidden';
  const rows = () => [...document.querySelectorAll(`#primary ${rowSelector}`)].filter(visible);
  const menus = () => [...document.querySelectorAll(menuSelector)].filter(visible);
  const titleOf = row => row.querySelector('#video-title')?.textContent.trim() || '(unavailable video)';
  const videoOf = row => {
    const href = row.querySelector('a[href*="/watch?"]')?.getAttribute('href');
    return href ? new URL(href, location.href).searchParams.get('v') || '' : '';
  };
  const buttonOf = row => row.querySelector('button[aria-label="Action menu"]');

  function playlistId() {
    const url = new URL(location.href);
    if (!['www.youtube.com', 'youtube.com'].includes(url.hostname) ||
        url.pathname !== '/playlist' || !url.searchParams.get('list')) {
      throw new Error('Open the loaded YouTube playlist page: https://www.youtube.com/playlist?list=...');
    }
    return url.searchParams.get('list');
  }

  function captureTarget(removeLabel) {
    const id = playlistId();
    const titleSelectors = [
      'ytd-playlist-header-renderer h1',
      'yt-page-header-renderer h1',
      'ytd-playlist-sidebar-primary-info-renderer #title',
      'ytd-browse[page-subtype="playlist"] h1',
    ];
    let name = id === 'WL' ? 'Watch later' : '';
    for (const selector of titleSelectors) {
      if (name) break;
      const element = [...document.querySelectorAll(selector)].find(visible);
      if (element) name = normalize(element.textContent);
    }
    const label = removeLabel === undefined ? (name ? `Remove from ${name}` : '') : normalize(removeLabel);
    if (label && !/^Remove from .+/.test(label)) {
      throw new Error('removeLabel must be an exact English removal label beginning with "Remove from ".');
    }
    return { id, name, label };
  }

  function check() {
    controller.signal.throwIfAborted();
    if (playlistId() !== target.id) throw new Error('Playlist changed. Stopped before taking another action.');
    if (document.hidden) throw new Error('Tab is hidden. Return to the playlist and start again.');
  }

  function sleep(ms) {
    const signal = controller.signal;
    signal.throwIfAborted();
    return new Promise((resolve, reject) => {
      const onAbort = () => {
        clearTimeout(timer);
        reject(signal.reason);
      };
      const timer = setTimeout(() => {
        signal.removeEventListener('abort', onAbort);
        resolve();
      }, ms);
      signal.addEventListener('abort', onAbort, { once: true });
    });
  }

  async function waitFor(read, description, timeout = 10000) {
    const deadline = Date.now() + timeout;
    while (true) {
      check();
      const result = read();
      if (result) return result;
      if (Date.now() >= deadline) throw new Error(`Timed out waiting for ${description}.`);
      await sleep(150);
    }
  }

  function removalItem() {
    const matches = new Set();
    for (const menu of menus()) {
      for (const label of menu.querySelectorAll('yt-formatted-string, span')) {
        if (normalize(label.textContent) !== target.label || !visible(label)) continue;
        const item = label.closest('ytd-menu-service-item-renderer, [role="menuitem"]');
        if (item && menu.contains(item) && visible(item) &&
            item.getAttribute('aria-disabled') !== 'true' && !item.hasAttribute('disabled')) {
          matches.add(item);
        }
      }
    }
    if (matches.size > 1) throw new Error('Multiple matching removal items appeared; close menus and retry.');
    return [...matches][0];
  }

  async function findRow() {
    let row = rows()[0];
    if (row) return row;
    state.phase = 'loading';
    console.info(prefix, 'No displayed entries. Waiting and scrolling to look for more…');
    for (let attempt = 0; attempt < 2; attempt++) {
      check();
      window.scrollTo(0, 0);
      await sleep(400);
      window.scrollTo(0, document.documentElement.scrollHeight);
      try {
        row = await waitFor(() => rows()[0], 'more playlist entries', 6000);
        return row;
      } catch (error) {
        if (error.message !== 'Timed out waiting for more playlist entries.') throw error;
      }
    }
    return null;
  }

  async function start({ preview = true, limit = Infinity, removeLabel } = {}) {
    if (state.running) {
      console.warn(prefix, 'Already running. Use playlistCleaner.stop() first.');
      return { ...state };
    }
    if (typeof preview !== 'boolean' || !(limit === Infinity || (Number.isInteger(limit) && limit > 0))) {
      throw new Error('Use preview: true/false and a positive integer limit (or Infinity).');
    }
    if (removeLabel !== undefined && (typeof removeLabel !== 'string' || !normalize(removeLabel))) {
      throw new Error('removeLabel must be a nonempty string.');
    }
    controller = new AbortController();
    Object.assign(state, {
      running: true, phase: 'starting', playlistId: '', playlistName: '', removeLabel: '',
      observedRemovals: 0, lastTitle: '', message: '',
    });
    try {
      target = captureTarget(removeLabel);
      Object.assign(state, { playlistId: target.id, playlistName: target.name, removeLabel: target.label });
      check();
      console.info(prefix, 'Target for this run:', {
        playlistId: target.id, playlistName: target.name || '(not detected)',
        removeLabel: target.label || '(not detected; supply removeLabel before removal)',
      });
      if (preview) {
        const loaded = rows();
        console.table(loaded.slice(0, 10).map(row => ({
          title: titleOf(row), menuButtonFound: Boolean(buttonOf(row)),
        })));
        state.phase = 'preview';
        state.message = `${loaded.length} loaded entries found. Nothing removed. Preview does not test opening menus.`;
      } else {
        if (!target.label) {
          throw new Error('Could not detect the playlist title. Supply its exact menu text using removeLabel: "Remove from YOUR PLAYLIST NAME".');
        }
        if (menus().length) throw new Error('Close the open video menu, then start again.');
        while (state.observedRemovals < limit) {
          check();
          const row = await findRow();
          if (!row) {
            state.phase = 'needs-recheck';
            state.message = 'No more displayed entries found. Refresh manually to verify the saved list; rerun if videos return.';
            break;
          }
          state.lastTitle = titleOf(row);
          const video = videoOf(row);
          const button = buttonOf(row);
          if (!button || !visible(button) || button.disabled) {
            throw new Error(`No usable Action menu button for: ${state.lastTitle}`);
          }
          state.phase = 'opening-menu';
          row.scrollIntoView({ block: 'center', behavior: 'instant' });
          check();
          button.click();
          const item = await waitFor(removalItem, `the exact menu item "${target.label}"`);
          // Stop if the row changed while its menu was opening.
          if (!visible(row) || videoOf(row) !== video) throw new Error('Target row changed before removal; stopped.');
          check();
          state.phase = 'removing';
          item.click();
          await waitFor(() => !row.isConnected || !visible(row) || videoOf(row) !== video,
            `the displayed row to disappear: ${state.lastTitle}`);
          state.observedRemovals++;
          console.info(prefix, `Observed removal ${state.observedRemovals}: ${state.lastTitle}`);
          await waitFor(() => menus().length === 0, 'the menu to close');
          // Give the page time to settle before selecting another row.
          state.phase = 'settling';
          await sleep(1200);
        }
        if (state.observedRemovals >= limit) {
          state.phase = 'limit-reached';
          state.message = `Stopped at the requested limit of ${limit}. Refresh to check that removals persisted.`;
        }
      }
      console.info(prefix, state.message);
    } catch (error) {
      state.phase = controller.signal.aborted ? 'stopped' : 'error';
      state.message = error.message || String(error);
      console[state.phase === 'error' ? 'error' : 'info'](prefix, state.message, { ...state });
    } finally {
      state.running = false;
    }
    return { ...state };
  }

  const api = {
    start,
    stop() {
      if (state.running) controller.abort(new DOMException('Stopped by you. An already-clicked removal may still finish.', 'AbortError'));
      return { ...state };
    },
    status: () => ({ ...state }),
  };
  window.playlistCleaner = api;
  window.watchLaterCleaner = api; // Keep commands from the earlier Watch Later snippet working.
  console.info(prefix, 'Installed. Previewing loaded entries. Commands: playlistCleaner.start({preview:false, limit:3}), .stop(), .status()');
  void start();
})();
