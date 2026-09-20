import { useEffect, useRef, useState } from "react";
import {
  Canvas,
  Circle,
  PencilBrush,
  Point,
  Rect,
  type Canvas as FabricCanvas,
  type TPointerEvent,
} from "fabric";
import { DemoToolbar } from "../components/DemoToolbar";
import { randomColor, scatter } from "../data/packages";
import { useElementSize } from "../hooks/useElementSize";
import { useFps } from "../hooks/useFps";
import { useSpaceKey } from "../hooks/useSpaceKey";

type Tool = "select" | "rect" | "ellipse" | "draw";

export function FabricDemo() {
  const fps = useFps();
  const space = useSpaceKey();
  const hostRef = useRef<HTMLDivElement>(null);
  const canvasElRef = useRef<HTMLCanvasElement>(null);
  const canvasRef = useRef<FabricCanvas | null>(null);
  const size = useElementSize(hostRef);
  const [tool, setTool] = useState<Tool>("select");
  const [count, setCount] = useState(0);
  const toolRef = useRef(tool);
  const spaceRef = useRef(space);
  toolRef.current = tool;
  spaceRef.current = space;

  const refreshCount = () => {
    const canvas = canvasRef.current;
    setCount(canvas ? canvas.getObjects().length : 0);
  };

  useEffect(() => {
    if (!canvasElRef.current) return;
    const canvas = new Canvas(canvasElRef.current, {
      backgroundColor: "#0c1017",
      selection: true,
      preserveObjectStacking: true,
      fireRightClick: true,
      stopContextMenu: true,
    });
    canvas.freeDrawingBrush = new PencilBrush(canvas);
    canvas.freeDrawingBrush.color = "#7cb7ff";
    canvas.freeDrawingBrush.width = 3;
    canvasRef.current = canvas;

    canvas.add(
      new Rect({
        left: 120,
        top: 80,
        width: 280,
        height: 140,
        fill: "#58a6ff33",
        stroke: "#58a6ff",
        strokeWidth: 2,
      }),
      new Circle({
        left: 460,
        top: 140,
        radius: 90,
        fill: "#3fb95033",
        stroke: "#3fb950",
        strokeWidth: 2,
      }),
    );
    refreshCount();

    let drawing: Rect | Circle | null = null;
    let origin = { x: 0, y: 0 };
    let panning = false;
    let last = { x: 0, y: 0 };

    const clientXY = (e: TPointerEvent) => {
      if ("clientX" in e) return { x: e.clientX, y: e.clientY };
      const t = e.touches[0] ?? e.changedTouches[0];
      return { x: t?.clientX ?? 0, y: t?.clientY ?? 0 };
    };

    canvas.on("mouse:wheel", (opt) => {
      const e = opt.e;
      let zoom = canvas.getZoom() * 0.999 ** e.deltaY;
      zoom = Math.min(8, Math.max(0.1, zoom));
      canvas.zoomToPoint(new Point(e.offsetX, e.offsetY), zoom);
      e.preventDefault();
      e.stopPropagation();
    });

    canvas.on("mouse:down", (opt) => {
      const e = opt.e;
      const middle = "button" in e && e.button === 1;
      const alt = "altKey" in e && e.altKey;
      if (spaceRef.current || middle || alt) {
        panning = true;
        canvas.selection = false;
        last = clientXY(e);
        return;
      }
      const current = toolRef.current;
      if (current === "select" || current === "draw") return;
      const p = canvas.getScenePoint(e);
      origin = { x: p.x, y: p.y };
      drawing =
        current === "ellipse"
          ? new Circle({
              left: p.x,
              top: p.y,
              radius: 1,
              fill: "#d2a8ff33",
              stroke: "#d2a8ff",
              strokeWidth: 2,
              originX: "center",
              originY: "center",
            })
          : new Rect({
              left: p.x,
              top: p.y,
              width: 1,
              height: 1,
              fill: "#58a6ff33",
              stroke: "#58a6ff",
              strokeWidth: 2,
            });
      canvas.add(drawing);
      canvas.setActiveObject(drawing);
    });

    canvas.on("mouse:move", (opt) => {
      const e = opt.e;
      if (panning) {
        const v = canvas.viewportTransform;
        if (!v) return;
        const now = clientXY(e);
        v[4] += now.x - last.x;
        v[5] += now.y - last.y;
        last = now;
        canvas.requestRenderAll();
        return;
      }
      if (!drawing) return;
      const p = canvas.getScenePoint(e);
      if (drawing instanceof Circle) {
        drawing.set({
          radius: Math.max(2, Math.hypot(p.x - origin.x, p.y - origin.y) / 2),
          left: (p.x + origin.x) / 2,
          top: (p.y + origin.y) / 2,
        });
      } else {
        drawing.set({
          left: Math.min(p.x, origin.x),
          top: Math.min(p.y, origin.y),
          width: Math.abs(p.x - origin.x),
          height: Math.abs(p.y - origin.y),
        });
      }
      drawing.setCoords();
      canvas.requestRenderAll();
    });

    const end = () => {
      panning = false;
      canvas.selection = toolRef.current === "select";
      if (drawing) refreshCount();
      drawing = null;
    };
    canvas.on("mouse:up", end);
    canvas.on("object:added", refreshCount);
    canvas.on("object:removed", refreshCount);

    return () => {
      canvas.dispose();
      canvasRef.current = null;
    };
  }, []);

  useEffect(() => {
    canvasRef.current?.setDimensions({ width: size.width, height: size.height });
  }, [size]);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const drawing = tool === "draw";
    canvas.isDrawingMode = drawing;
    canvas.selection = tool === "select" && !space;
    canvas.defaultCursor = space ? "grab" : drawing ? "crosshair" : tool === "select" ? "default" : "crosshair";
  }, [tool, space]);

  const spawn = (n: number) => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    for (let i = 0; i < n; i++) {
      const p = scatter(i, n);
      const color = randomColor(i);
      canvas.add(
        i % 3 === 0
          ? new Circle({
              left: p.x,
              top: p.y,
              radius: p.w / 2,
              fill: `${color}55`,
              stroke: color,
              strokeWidth: 1,
              originX: "center",
              originY: "center",
            })
          : new Rect({
              left: p.x,
              top: p.y,
              width: p.w,
              height: p.h,
              fill: `${color}55`,
              stroke: color,
              strokeWidth: 1,
            }),
      );
    }
    canvas.requestRenderAll();
    refreshCount();
  };

  const clear = () => {
    canvasRef.current?.clear();
    canvasRef.current?.set({ backgroundColor: "#0c1017" });
    refreshCount();
  };

  return (
    <div className="demo-page">
      <DemoToolbar
        objectCount={count}
        fps={fps}
        extra="engine · built-in handles + SVG DNA"
        hint="Wheel zoom · Space/Alt/middle-mouse pan · drag handles to resize. Spawn 2k and pan to feel the object model."
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
      <div ref={hostRef} className="demo-stage engine-stage">
        <canvas ref={canvasElRef} />
      </div>
    </div>
  );
}
