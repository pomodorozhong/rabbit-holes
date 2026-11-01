# Clearing YouTube playlists with a Chrome Snippet

*Draft, 2026-11-01.*

**Main finding:** A saved Chrome Snippet makes a playlist cleaner easier to edit and debug. Reliability comes from waiting for each menu and checking progress after each removal. The [companion script](09-youtube-playlist-cleanup.js) implements that sequence for Watch Later and other editable playlists, but its compatibility with the live YouTube page still needs checking.

**Was the bookmarklet the problem?**

- The starting problem was a bookmarklet that sometimes stopped clicking while the tab remained responsive. Sometimes the list went blank and showed videos again after a refresh. These observations establish that the cleanup was unreliable, but do not identify its cause. The [session record](sessions/2026-10-31-youtube-playlist-cleanup.md) preserves the observations and code findings.
- A bookmarklet launches JavaScript through a [`javascript:` URL](https://developer.mozilla.org/en-US/docs/Web/URI/Reference/Schemes/javascript). The inspected script used `setInterval(..., 2000)` to open a menu and immediately search for removal options. The [two-second interval](https://developer.mozilla.org/en-US/docs/Web/API/Window/setInterval) separates attempts; it does not insert a wait between opening the menu and searching it. That creates a possible timing failure when the menu appears asynchronously.
- The script also assumed a button existed, matched broad removal text across the document, and never checked whether a removal worked. Moving that logic into Console would preserve those weaknesses. The supplied bookmark URL parsed successfully; a reported length limit affecting an earlier version remains unverified.

**Why use Console and Snippets?**

- [Chrome Console](https://developer.chrome.com/docs/devtools/console/javascript) lets us test an expression before putting it in a loop and inspect errors when something fails. In this session, querying the action-menu selector returned a button; the replacement loop has not yet been tested on the user's page.
- [Chrome Snippets](https://developer.chrome.com/docs/devtools/javascript/snippets) save editable JavaScript with access to the current page. This was the user's chosen workflow. Refreshing ends the running cleanup, so the saved snippet must be run again afterward.

**Can the same script clean other playlists?**

- The companion captures the current playlist ID when each run starts and stops if navigation changes it. It derives an exact English removal label from the playlist title, following YouTube's documented [Remove from playlist-name action](https://support.google.com/youtube/answer/6083634?hl=en). It uses only removal controls available to the account.
- If the title cannot be read, the script stops before opening a removal menu. Supply the exact English label with an option such as `removeLabel: 'Remove from Study queue'`. It does not fall back to matching every option containing removal text.
- The loop waits for the intended menu item, clicks it, waits for the displayed row to disappear or change video, and then continues. A timeout reports the failed step. A change to a link's playlist index alone does not count as removal.

**How to use the companion**

- Open the intended, fully loaded `youtube.com/playlist?list=...` page. Select **All** if content-filter chips are present; [YouTube's filters](https://support.google.com/youtube/answer/6083634?hl=en) can otherwise hide Shorts or long-form videos.
- Copy the entire [JavaScript file](09-youtube-playlist-cleanup.js) into **DevTools → Sources → Snippets**, save it, and press **⌘Enter** on macOS. This installs the commands and previews loaded rows without removing anything. The preview reports the target and button matches; it does not test opening menus.
- Keep the playlist tab in the foreground and let the script operate the menus. The removal commands below target watched and unwatched entries, in displayed order. First try three entries, then refresh to check persistence before continuing.

```js
playlistCleaner.start({ preview: false, limit: 3 })
```

- After the refresh check, run the saved snippet again. To clear the remaining entries, use this separate command:

```js
playlistCleaner.start({ preview: false })
```

- To interrupt the run, use the stop command. An already-clicked removal may still finish. The status command reports the current phase, target, counter, and last message.

```js
playlistCleaner.stop()
playlistCleaner.status()
```

- The counter records changes in the displayed list, not server-confirmed removals. If the page becomes blank, the script scrolls and waits for more entries, then requests a manual refresh check. It does not claim the saved playlist is empty just because no rows are displayed.

**Open**

- The generalized script passed 19 simulated-page checks, including delayed menus, exact labels, stop behavior, switching playlists, loading entries, and stalled removals. No live YouTube run has verified the remaining selectors or persistence after refresh.
- The causes of the original silent stops and blank lists remain unresolved. Scheduled execution, continued operation across refreshes, and rules for removing only selected videos were not explored.
