# Freeform canvas packages (web) — comparison + runnable demos

Date: 2026-09-04

This note compares the packages people actually reach for when they want a **freeform / infinite canvas** in the browser: a surface you pan, zoom, draw on, and drop objects onto — not a spreadsheet, and not a chart.

There are two different products hiding under that phrase:

| Layer | What you buy | Packages in this bake-off |
|---|---|---|
| **Whiteboard SDK** | Tools, selection, undo, export, often collab. You embed it. | **tldraw**, **Excalidraw** |
| **Scene engine** | Renderer + object/scene graph. You build the editor. | **Fabric.js**, **Konva**, **PixiJS** |

Runnable playground (same spawn-stress HUD on every demo):

```bash
cd topics/freeform_canvas/demo
npm ci
npm run dev
```

Requires Node.js `20.19+` or `22.12+` (the Vite version used here). Open http://localhost:5173 — the home page has the comparison table, and the top navigation opens one demo per library. On each demo: draw / select, then **Spawn 2k** (then 5k) and pan. FPS is main-thread frames, so React reconciling a huge tree counts.

`npm ci` uses the committed lockfile. To verify a production build instead, run:

```bash
npm run build
```

The build is a compile/bundle check; the FPS readout in the playground is an intentionally qualitative, interactive comparison rather than a benchmark.

---

## How to read this

Stars and download counts are popularity, not quality. Performance claims below are **qualitative**, meant to be checked in the demos on *your* machine. I did not publish a synthetic fps.csv — those lie once you add hit-testing, text, and React.

Sources: GitHub (stars pulled 2026-09-04), npm current versions, [tldraw license docs](https://tldraw.dev/sdk-features/license-key), [Excalidraw integration](https://docs.excalidraw.com/docs/@excalidraw/excalidraw/integration), [Konva “which library” guide](https://konvajs.org/docs/guides/best-canvas-library.html) (Anton Lavrenov, Aug 2026 download figures).

---

## Snapshot (Sep 2026)

| | tldraw | Excalidraw | Fabric.js | Konva | PixiJS |
|---|---|---|---|---|---|
| npm | `tldraw` **5.4.0** | `@excalidraw/excalidraw` **0.18.1** | `fabric` **7.4.0** | `konva` **10.3.2** + `react-konva` | `pixi.js` **8.20.1** |
| GitHub stars | 50k | **131k** | 31k | 15k | 48k |
| npm / month (engines) | SDK (not comparable) | SDK (not comparable) | ~3.7M | **~10.1M** | ~3.8M |
| License | tldraw license — **paid in production** | **MIT** | MIT | MIT | MIT |
| Renderer | Canvas 2D + HTML overlays | Canvas 2D (rough / hand-drawn) | Canvas 2D | Canvas 2D, **multi-layer** | **WebGL / WebGPU** |
| Framework | React only | React, **no SSR** | Vanilla | Vanilla + official React/Vue/Svelte/Angular | Vanilla (+ community React) |
| You get | Whole editor | Whole whiteboard | Object model, handles, SVG, brushes | Scene graph, events, Transformer | GPU display list |
| You still build | Persistence, license, maybe sync | Persistence / rooms | Pan-zoom chrome, app UI | Undo, SVG export, editor chrome | **Everything editor-shaped** |

Konva’s own guide is unusually honest: use **tldraw / Excalidraw** if you want a whiteboard; **Fabric** if you need SVG written back out; **Pixi** if you need game-like object counts; **Konva** if you need an interactive app and own the model.

---

## Performance

What “fast” means here is: *can I pan a busy board at 60 Hz, and does picking still work?*

| | Typical ceiling (interactive objects) | Why |
|---|---|---|
| **PixiJS** | Tens of thousands of sprites if you keep them dumb | GPU. The demo’s 5k spawn uses `Sprite` + `Texture.WHITE`, which is the honest Pixi path. `Graphics` per object is heavier. |
| **Konva** | Low thousands comfortably; more if you skip listening / use layers | Canvas 2D, but static layers don’t redraw when the active layer moves. **react-konva children do not scale to 5k** — the demo therefore dumps stress shapes onto a native `Konva.Layer`. |
| **Fabric.js** | Hundreds to low thousands before pan hitch | Rich object model (controls, caching, coords). Excellent for an editor; not a particle engine. |
| **tldraw** | Designed around “thousands of shapes” | Store + viewport culling, not React-per-shape. Spawn 2k and pan; 5k is the interesting test. |
| **Excalidraw** | Fine for sketches; 5k rough boxes is a stress test | Every element is a sketched path. Beautiful, not cheap. |

**Portable rule:** if the hot path is *many moving primitives*, Pixi. If it is *a few hundred editable objects with handles*, Fabric or Konva. If it is *a document the user draws*, tldraw / Excalidraw — and you should not re-implement their viewport.

The HUD FPS number is a feel meter, not a benchmark: it drops when the main thread janks, including during the spawn itself.

---

## Features

| Capability | tldraw | Excalidraw | Fabric | Konva | Pixi |
|---|---|---|---|---|---|
| Infinite pan / zoom | Yes | Yes | DIY (demo has it) | DIY (demo has it) | DIY (demo has it) |
| Select / move / resize / rotate | Yes | Yes | **Built-in controls** | `Transformer` | DIY |
| Freehand | Yes | Yes | `PencilBrush` | DIY lines | DIY |
| Text | Rich text | Yes | `IText` inline edit | Limited / DIY | DIY (bitmap / SDF) |
| Images / assets | Yes | Yes | First-class + filters | `Konva.Image` | Textures |
| Frames / grouping | Frames, groups | Groups | Groups | Groups | Containers |
| Arrows / bindings | Smart arrows | Bindable arrows | DIY | DIY | DIY |
| Undo / redo | Yes | Yes | Object stack | DIY | DIY |
| JSON document | Yes | `.excalidraw` | `toJSON` | `toJSON` | DIY |
| SVG import | — | — | **Yes** | Draw SVG, not a round-trip | No |
| SVG / PNG export | Yes | Yes | Yes | PNG (`toDataURL`); SVG not native | Render texture |
| Multiplayer | Official sync | Rooms + optional E2E | DIY | DIY | DIY |
| Custom shape types | **SDK feature** | Libraries, not a full shape protocol | Subclass `FabricObject` | Custom `Shape` | DisplayObject / shaders |
| Animation / particles | Not the point | Not the point | Basic | Use GSAP etc. | **Ticker, particles, filters** |

Aesthetic: Excalidraw is *intentionally* sketchy (signals “working note”). tldraw is geometric and product-like. The engines have no default look.

---

## Portability

| | tldraw | Excalidraw | Fabric | Konva | Pixi |
|---|---|---|---|---|---|
| **License to ship** | Production **requires a license key**. Dev on localhost is free. Hobby keeps a watermark. Unlicensed production stops rendering. | MIT, embed anywhere | MIT | MIT | MIT |
| **Self-host the editor** | Client is yours; sync/assets are extra | Easiest whiteboard to self-host | N/A (library) | N/A | N/A |
| **React 19** | Yes (`^18.2 \|\| ^19.2.1`) | Yes (client only) | Vanilla | `react-konva` 19.x | Vanilla |
| **Vue / Svelte / Angular** | No | No | Yes | **Official bindings** | Community |
| **SSR** | Don’t render the editor on the server | Explicitly unsupported | Node via `fabric/node` + node-canvas (export) | Possible with a canvas impl | Limited |
| **Touch / tablet** | Strong | Strong | OK | Strong | Strong (you wire gestures) |
| **Bundle** | Large (whole product) | Large (whole product) | Large | Medium | Medium–large (GPU stack) |
| **TypeScript** | First-class | First-class | Yes (v6+) | Yes | Yes |
| **WebGPU** | No | No | No | No | **Yes (v8)** |

The license is the whole plot for tldraw: source-available SDK, not MIT. Evaluate on localhost without a key; do not plan a production deploy until [tldraw.dev/pricing](https://tldraw.dev/pricing) works for you. Excalidraw is the MIT “just ship it” whiteboard.

---

## DX (what it feels like to build with)

- **tldraw** — `import { Tldraw } from 'tldraw'` plus CSS. Custom shapes, tools, and the editor API are documented as an SDK. Fastest path to a *polished* canvas product if React + license are OK.
- **Excalidraw** — one component, `excalidrawAPI`, JSON scene. Trivial embed. Extending the *look* or the *element model* is not the point.
- **Fabric** — most “Photoshop-like” engine: controls, image filters, SVG in/out, drawing modes. v7 is ESM (`import { Canvas, Rect } from 'fabric'`).
- **Konva** — best engine DX for app UI. Layers, event bubbling, `Transformer`, and official React. The trap is putting 5k items in React state.
- **Pixi** — best engine DX for *rendering*. Worst DX if you thought you were buying an editor. The demo’s tiny tool palette is already more code than the tldraw page.

---

## What I would pick

| If you need… | Pick |
|---|---|
| A whiteboard in the product this week, MIT, sketchy is fine | **Excalidraw** |
| The canvas *is* the product (design tool, lesson planner, spatial doc) and you can pay | **tldraw** |
| Same, but license must stay MIT / you own the file format | **Konva** (or Fabric if SVG round-trip matters) |
| Photo / mockup editor, SVG import-export, built-in handles | **Fabric.js** |
| 5k–50k moving nodes, particles, filters, games | **PixiJS** |
| Node/edge graph (flowcharts, pipelines) | **Not these** — use `@xyflow/react` (React Flow) |

Many teams run two: Excalidraw for engineering notes, something else for the product canvas.

---

## Also considered (no demo)

| Package | Why it didn’t get a playground |
|---|---|
| **Paper.js** | Vector math / Bézier / boolean ops. Creative coding, not an editor SDK. ~15k stars. |
| **p5.js** | Sketches and teaching. |
| **@xyflow/react** | Dominant *node graph* canvas, not freeform drawing. |
| **JointJS / Rappid, GoJS, mxGraph** | Diagram vendors; different problem. |
| **Penpot** | Full design *app*, not an embeddable package. |
| **perfect-freehand, rough.js** | Stroke / style libraries you compose into the engines above. |

---

## Demo map

| Route | Package | What to try |
|---|---|---|
| `/tldraw` | tldraw 5 | Native tools, then spawn 2k |
| `/excalidraw` | Excalidraw 0.18 | Sketch style, spawn 2k rough boxes |
| `/fabric` | Fabric 7 | Wheel zoom, Space pan, built-in handles |
| `/konva` | Konva 10 + react-konva | Transformer on select; 5k goes to a native layer |
| `/pixi` | Pixi 8 | Same mini-editor; 5k sprites on the GPU |

Engine demos share a tiny tool strip (select / rect / ellipse / draw) so you can feel the *absence* of a whiteboard SDK.

---

## Versions pinned by the demo

See `demo/package.json`. Resolved at first install; bump deliberately, this space moves quickly (tldraw 5.x, Fabric 7, Konva 10, Pixi 8, React 19).
