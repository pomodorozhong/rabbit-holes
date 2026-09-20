import { Application, Container, Graphics, Sprite, Texture } from "pixi.js";
import type { FederatedPointerEvent } from "pixi.js";
import { useEffect, useRef, useState } from "react";
import { DemoToolbar } from "../components/DemoToolbar";
import { randomColor, scatter } from "../data/packages";
import { useFps } from "../hooks/useFps";
import { useSpaceKey } from "../hooks/useSpaceKey";

type Tool = "select" | "rect" | "ellipse" | "draw";

export function PixiDemo() {
  const fps = useFps();
  const space = useSpaceKey();
  const hostRef = useRef<HTMLDivElement>(null);
  const worldRef = useRef<Container | null>(null);
  const toolRef = useRef<Tool>("select");
  const spaceRef = useRef(space);
  const [tool, setTool] = useState<Tool>("select");
  const [count, setCount] = useState(0);
  const [ready, setReady] = useState(false);
  toolRef.current = tool;
  spaceRef.current = space;

  const refreshCount = () => {
    const world = worldRef.current;
    setCount(world ? world.children.length : 0);
  };

  useEffect(() => {
    const host = hostRef.current;
    if (!host) return;
    let destroyed = false;
    let inited = false;
    const app = new Application();
    const world = new Container();
    worldRef.current = world;
    const wheelOpts: AddEventListenerOptions = { passive: false };

    const destroyApp = () => {
      if (!inited) return;
      inited = false;
      app.destroy(true);
    };

    const makeDraggable = (g: Graphics) => {
      g.on("pointerdown", (e: FederatedPointerEvent) => {
        if (toolRef.current !== "select" || spaceRef.current) return;
        e.stopPropagation();
        const start = { x: g.x, y: g.y };
        const origin = { x: e.global.x, y: e.global.y };
        const move = (ev: FederatedPointerEvent) => {
          const scale = world.scale.x || 1;
          g.x = start.x + (ev.global.x - origin.x) / scale;
          g.y = start.y + (ev.global.y - origin.y) / scale;
        };
        const up = () => {
          app.stage.off("pointermove", move);
          app.stage.off("pointerup", up);
          app.stage.off("pointerupoutside", up);
        };
        app.stage.on("pointermove", move);
        app.stage.on("pointerup", up);
        app.stage.on("pointerupoutside", up);
      });
    };

    const onWheel = (ev: WheelEvent) => {
      ev.preventDefault();
      const scale = world.scale.x * (ev.deltaY > 0 ? 0.92 : 1.08);
      const next = Math.min(8, Math.max(0.1, scale));
      const rect = host.getBoundingClientRect();
      const local = { x: ev.clientX - rect.left, y: ev.clientY - rect.top };
      const wx = (local.x - world.x) / world.scale.x;
      const wy = (local.y - world.y) / world.scale.y;
      world.scale.set(next);
      world.x = local.x - wx * next;
      world.y = local.y - wy * next;
    };

    void app
      .init({
        background: 0x0c1017,
        antialias: true,
        autoDensity: true,
        resolution: Math.min(window.devicePixelRatio || 1, 2),
        resizeTo: host,
      })
      .then(() => {
        inited = true;
        if (destroyed) {
          destroyApp();
          return;
        }
        host.appendChild(app.canvas);
        app.stage.eventMode = "static";
        app.stage.hitArea = app.screen;
        app.stage.addChild(world);

        const seedRect = new Graphics()
          .roundRect(0, 0, 280, 140, 4)
          .fill({ color: 0x58a6ff, alpha: 0.35 })
          .stroke({ color: 0x58a6ff, width: 2 });
        seedRect.position.set(120, 80);
        seedRect.eventMode = "static";
        seedRect.cursor = "pointer";
        makeDraggable(seedRect);

        const seedEllipse = new Graphics()
          .ellipse(90, 90, 90, 90)
          .fill({ color: 0x3fb950, alpha: 0.35 })
          .stroke({ color: 0x3fb950, width: 2 });
        seedEllipse.position.set(460, 140);
        seedEllipse.eventMode = "static";
        seedEllipse.cursor = "pointer";
        makeDraggable(seedEllipse);

        world.addChild(seedRect, seedEllipse);
        refreshCount();
        setReady(true);

        let panning = false;
        let drawing: Graphics | null = null;
        let origin = { x: 0, y: 0 };
        let last = { x: 0, y: 0 };

        const worldPoint = (e: FederatedPointerEvent) => world.toLocal(e.global);

        app.stage.on("pointerdown", (e: FederatedPointerEvent) => {
          const pan = spaceRef.current || e.button === 1;
          if (pan) {
            panning = true;
            last = { x: e.global.x, y: e.global.y };
            return;
          }
          const current = toolRef.current;
          if (current === "select") return;
          const p = worldPoint(e);
          origin = p;
          drawing = new Graphics();
          drawing.eventMode = "none";
          world.addChild(drawing);
          if (current === "draw") {
            drawing.moveTo(p.x, p.y).stroke({ color: 0x7cb7ff, width: 3 });
          }
        });

        app.stage.on("pointermove", (e: FederatedPointerEvent) => {
          if (panning) {
            world.x += e.global.x - last.x;
            world.y += e.global.y - last.y;
            last = { x: e.global.x, y: e.global.y };
            return;
          }
          if (!drawing) return;
          const p = worldPoint(e);
          const current = toolRef.current;
          if (current === "draw") {
            drawing.lineTo(p.x, p.y).stroke({ color: 0x7cb7ff, width: 3 });
            return;
          }
          drawing.clear();
          const x = Math.min(origin.x, p.x);
          const y = Math.min(origin.y, p.y);
          const w = Math.abs(p.x - origin.x);
          const h = Math.abs(p.y - origin.y);
          if (current === "ellipse") {
            drawing
              .ellipse(x + w / 2, y + h / 2, w / 2, h / 2)
              .fill({ color: 0xd2a8ff, alpha: 0.35 })
              .stroke({ color: 0xd2a8ff, width: 2 });
          } else {
            drawing
              .roundRect(x, y, w, h, 4)
              .fill({ color: 0x58a6ff, alpha: 0.35 })
              .stroke({ color: 0x58a6ff, width: 2 });
          }
        });

        const endStroke = () => {
          if (drawing && toolRef.current !== "draw") {
            drawing.eventMode = "static";
            drawing.cursor = "pointer";
            makeDraggable(drawing);
          }
          drawing = null;
          panning = false;
          refreshCount();
        };
        app.stage.on("pointerup", endStroke);
        app.stage.on("pointerupoutside", endStroke);
        host.addEventListener("wheel", onWheel, wheelOpts);
      });

    return () => {
      destroyed = true;
      host.removeEventListener("wheel", onWheel, wheelOpts);
      worldRef.current = null;
      destroyApp();
    };
  }, []);

  const spawn = (n: number) => {
    const world = worldRef.current;
    if (!world) return;
    for (let i = 0; i < n; i++) {
      const p = scatter(i, n);
      const sprite = new Sprite(Texture.WHITE);
      sprite.tint = Number.parseInt(randomColor(i).slice(1), 16);
      sprite.alpha = 0.7;
      sprite.position.set(p.x, p.y);
      sprite.width = p.w;
      sprite.height = p.h;
      sprite.eventMode = "none";
      world.addChild(sprite);
    }
    refreshCount();
  };

  const clear = () => {
    worldRef.current?.removeChildren();
    refreshCount();
  };

  return (
    <div className="demo-page">
      <DemoToolbar
        objectCount={count}
        fps={fps}
        extra={ready ? "WebGL/WebGPU · spawn uses sprites" : "starting GPU…"}
        hint="Wheel zoom · Space/middle-mouse pan · drag in select. Renderer only: no transform handles, undo, or SVG."
        onSpawn={spawn}
        onClear={clear}
      />
      <div className="engine-tools">
        {(["select", "rect", "ellipse", "draw"] as const).map((id) => (
          <button key={id} type="button" className={tool === id ? "active" : ""} onClick={() => setTool(id)}>
            {id}
          </button>
        ))}
      </div>
      <div ref={hostRef} className="demo-stage engine-stage pixi-stage" />
    </div>
  );
}
