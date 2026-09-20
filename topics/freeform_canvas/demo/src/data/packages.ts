export const STRESS_COUNTS = [500, 2000, 5000] as const;

export const PALETTE = ["#58a6ff", "#3fb950", "#d2a8ff", "#f0883e", "#f85149", "#79c0ff"];

export function randomColor(i: number): string {
  return PALETTE[i % PALETTE.length];
}

export function scatter(index: number, total: number, spread = 2800) {
  const gold = 2.399963229728653;
  const r = Math.sqrt((index + 1) / total) * spread;
  const a = index * gold;
  return {
    x: 120 + r * Math.cos(a),
    y: 120 + r * Math.sin(a),
    w: 18 + (index % 5) * 6,
    h: 18 + ((index * 3) % 5) * 6,
  };
}

export type CanvasPackage = {
  id: string;
  path: string;
  name: string;
  npm: string;
  layer: "Whiteboard SDK" | "Scene engine";
  renderer: string;
  license: string;
  stars: string;
  monthlyDownloads: string;
  framework: string;
  undo: string;
  svg: string;
  collab: string;
  customShapes: string;
  bestFor: string;
  watchOut: string;
};

export const PACKAGES: CanvasPackage[] = [
  {
    id: "tldraw",
    path: "/tldraw",
    name: "tldraw",
    npm: "tldraw",
    layer: "Whiteboard SDK",
    renderer: "Canvas 2D + HTML overlays",
    license: "tldraw license (paid in production)",
    stars: "50k",
    monthlyDownloads: "SDK (lower than engines)",
    framework: "React only",
    undo: "Built-in",
    svg: "Export",
    collab: "Official sync kit",
    customShapes: "First-class",
    bestFor: "Product-quality infinite canvas inside an app",
    watchOut: "Production needs a license key; watermark/hobby terms",
  },
  {
    id: "excalidraw",
    path: "/excalidraw",
    name: "Excalidraw",
    npm: "@excalidraw/excalidraw",
    layer: "Whiteboard SDK",
    renderer: "Canvas 2D (hand-drawn / rough)",
    license: "MIT",
    stars: "131k",
    monthlyDownloads: "Whiteboard component",
    framework: "React (no SSR)",
    undo: "Built-in",
    svg: "PNG / SVG / JSON",
    collab: "Room protocol, E2E optional",
    customShapes: "Limited (libraries)",
    bestFor: "Engineering sketches, docs, embeddable whiteboard",
    watchOut: "Sketch aesthetic is opinionated; not a design-tool SDK",
  },
  {
    id: "fabric",
    path: "/fabric",
    name: "Fabric.js",
    npm: "fabric",
    layer: "Scene engine",
    renderer: "Canvas 2D",
    license: "MIT",
    stars: "31k",
    monthlyDownloads: "~3.7M",
    framework: "Vanilla (community React)",
    undo: "Built-in object stack",
    svg: "Import + export",
    collab: "DIY",
    customShapes: "Object subclasses",
    bestFor: "Design / photo editors, SVG round-trip",
    watchOut: "Heavier object model; slower than Konva/Pixi at huge counts",
  },
  {
    id: "konva",
    path: "/konva",
    name: "Konva",
    npm: "konva + react-konva",
    layer: "Scene engine",
    renderer: "Canvas 2D (multi-layer)",
    license: "MIT",
    stars: "15k",
    monthlyDownloads: "~10.1M",
    framework: "Vanilla + official React/Vue/Svelte/Angular",
    undo: "DIY",
    svg: "Can draw SVG; no first-class export",
    collab: "DIY",
    customShapes: "Scene-graph nodes",
    bestFor: "Interactive apps: annotation, dashboards, seat maps",
    watchOut: "You build the editor chrome; Canvas 2D ceiling vs WebGL",
  },
  {
    id: "pixi",
    path: "/pixi",
    name: "PixiJS",
    npm: "pixi.js",
    layer: "Scene engine",
    renderer: "WebGL / WebGPU",
    license: "MIT",
    stars: "48k",
    monthlyDownloads: "~3.8M",
    framework: "Vanilla + community React",
    undo: "DIY",
    svg: "No (texture/sprites)",
    collab: "DIY",
    customShapes: "Display objects / shaders",
    bestFor: "Thousands of moving objects, games, particle UIs",
    watchOut: "Renderer, not an editor — selection, snap, text, SVG are on you",
  },
];
