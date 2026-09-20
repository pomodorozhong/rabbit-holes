import { useEffect, useRef, useState } from "react";
import Konva from "konva";
import { Ellipse, Layer, Line, Rect, Stage, Transformer } from "react-konva";
import type { KonvaEventObject } from "konva/lib/Node";
import { DemoToolbar } from "../components/DemoToolbar";
import { randomColor, scatter } from "../data/packages";
import { useElementSize } from "../hooks/useElementSize";
import { useFps } from "../hooks/useFps";
import { useSpaceKey } from "../hooks/useSpaceKey";

type Tool = "select" | "rect" | "ellipse" | "draw";
type Shape = {
  id: string;
  type: "rect" | "ellipse";
  x: number;
  y: number;
  width: number;
  height: number;
  fill: string;
  stroke: string;
};
type Stroke = { id: string; points: number[]; color: string };

let seq = 0;
const nid = () => `k-${++seq}`;

export function KonvaDemo() {
  const fps = useFps();
  const space = useSpaceKey();
  const hostRef = useRef<HTMLDivElement>(null);
  const size = useElementSize(hostRef);
  const transformerRef = useRef<Konva.Transformer>(null);
  const selectedRef = useRef<Konva.Node | null>(null);
  const stressLayerRef = useRef<Konva.Layer>(null);
  const [tool, setTool] = useState<Tool>("select");
  const [shapes, setShapes] = useState<Shape[]>([
    { id: nid(), type: "rect", x: 120, y: 80, width: 280, height: 140, fill: "#58a6ff33", stroke: "#58a6ff" },
    { id: nid(), type: "ellipse", x: 460, y: 140, width: 180, height: 180, fill: "#3fb95033", stroke: "#3fb950" },
  ]);
  const [lines, setLines] = useState<Stroke[]>([]);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [draft, setDraft] = useState<Shape | Stroke | null>(null);
  const [camera, setCamera] = useState({ x: 0, y: 0, scale: 1 });
  const [stressCount, setStressCount] = useState(0);

  const objectCount = shapes.length + lines.length + (draft ? 1 : 0) + stressCount;

  useEffect(() => {
    const tr = transformerRef.current;
    const node = selectedRef.current;
    if (!tr) return;
    if (tool === "select" && node) {
      tr.nodes([node]);
    } else {
      tr.nodes([]);
    }
    tr.getLayer()?.batchDraw();
  }, [selectedId, tool, shapes]);

  const toWorld = (stage: Konva.Stage) => {
    const p = stage.getPointerPosition();
    if (!p) return { x: 0, y: 0 };
    return { x: (p.x - camera.x) / camera.scale, y: (p.y - camera.y) / camera.scale };
  };

  const onWheel = (e: KonvaEventObject<WheelEvent>) => {
    e.evt.preventDefault();
    const stage = e.target.getStage();
    if (!stage) return;
    const pointer = stage.getPointerPosition();
    if (!pointer) return;
    const oldScale = camera.scale;
    const next = e.evt.deltaY > 0 ? oldScale / 1.08 : oldScale * 1.08;
    const scale = Math.min(8, Math.max(0.1, next));
    setCamera({
      scale,
      x: pointer.x - ((pointer.x - camera.x) / oldScale) * scale,
      y: pointer.y - ((pointer.y - camera.y) / oldScale) * scale,
    });
  };

  const onMouseDown = (e: KonvaEventObject<MouseEvent>) => {
    const stage = e.target.getStage();
    if (!stage) return;
    if (space || e.evt.button === 1 || e.evt.altKey) return;
    const world = toWorld(stage);
    if (tool === "select") {
      if (e.target === stage) setSelectedId(null);
      return;
    }
    if (tool === "draw") {
      setDraft({ id: nid(), points: [world.x, world.y], color: "#7cb7ff" });
      return;
    }
    setSelectedId(null);
    setDraft({
      id: nid(),
      type: tool === "ellipse" ? "ellipse" : "rect",
      x: world.x,
      y: world.y,
      width: 1,
      height: 1,
      fill: tool === "ellipse" ? "#d2a8ff33" : "#58a6ff33",
      stroke: tool === "ellipse" ? "#d2a8ff" : "#58a6ff",
    });
  };

  const onMouseMove = (e: KonvaEventObject<MouseEvent>) => {
    if (!draft) return;
    const stage = e.target.getStage();
    if (!stage) return;
    const world = toWorld(stage);
    if ("points" in draft) {
      setDraft({ ...draft, points: [...draft.points, world.x, world.y] });
      return;
    }
    setDraft({
      ...draft,
      width: world.x - draft.x,
      height: world.y - draft.y,
    });
  };

  const onMouseUp = () => {
    if (!draft) return;
    if ("points" in draft) {
      setLines((xs) => [...xs, draft]);
    } else {
      const width = Math.abs(draft.width);
      const height = Math.abs(draft.height);
      if (width > 2 && height > 2) {
        setShapes((xs) => [
          ...xs,
          {
            ...draft,
            x: Math.min(draft.x, draft.x + draft.width),
            y: Math.min(draft.y, draft.y + draft.height),
            width,
            height,
          },
        ]);
      }
    }
    setDraft(null);
  };

  const spawn = (n: number) => {
    const layer = stressLayerRef.current;
    if (!layer) return;
    for (let i = 0; i < n; i++) {
      const p = scatter(i, n);
      const color = randomColor(i);
      if (i % 3 === 0) {
        layer.add(
          new Konva.Circle({
            x: p.x + p.w / 2,
            y: p.y + p.h / 2,
            radius: p.w / 2,
            fill: `${color}55`,
            stroke: color,
            strokeWidth: 1,
            listening: false,
          }),
        );
      } else {
        layer.add(
          new Konva.Rect({
            x: p.x,
            y: p.y,
            width: p.w,
            height: p.h,
            fill: `${color}55`,
            stroke: color,
            strokeWidth: 1,
            listening: false,
          }),
        );
      }
    }
    layer.batchDraw();
    setStressCount(layer.getChildren().length);
  };

  const clear = () => {
    setShapes([]);
    setLines([]);
    setDraft(null);
    setSelectedId(null);
    stressLayerRef.current?.destroyChildren();
    stressLayerRef.current?.batchDraw();
    setStressCount(0);
  };

  const allShapes = draft && !("points" in draft) ? [...shapes, draft] : shapes;
  const allLines = draft && "points" in draft ? [...lines, draft] : lines;

  return (
    <div className="demo-page">
      <DemoToolbar
        objectCount={objectCount}
        fps={fps}
        extra="stress layer is vanilla Konva (not React children)"
        hint="Wheel zoom · Space/Alt pan · Transformer on select. 5k spawn uses a native layer so you feel Konva, not React reconciling 5k nodes."
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
        <Stage
          width={size.width}
          height={size.height}
          x={camera.x}
          y={camera.y}
          scaleX={camera.scale}
          scaleY={camera.scale}
          draggable={space}
          onWheel={onWheel}
          onMouseDown={onMouseDown}
          onMouseMove={onMouseMove}
          onMouseUp={onMouseUp}
          onDragEnd={(e) => {
            if (e.target !== e.target.getStage()) return;
            setCamera((c) => ({ ...c, x: e.target.x(), y: e.target.y() }));
          }}
        >
          <Layer>
            {allLines.map((line) => (
              <Line key={line.id} points={line.points} stroke={line.color} strokeWidth={3} lineCap="round" lineJoin="round" />
            ))}
            {allShapes.map((shape) =>
              shape.type === "ellipse" ? (
                <Ellipse
                  key={shape.id}
                  x={shape.x + shape.width / 2}
                  y={shape.y + shape.height / 2}
                  radiusX={Math.abs(shape.width) / 2}
                  radiusY={Math.abs(shape.height) / 2}
                  fill={shape.fill}
                  stroke={shape.stroke}
                  strokeWidth={2}
                  draggable={tool === "select"}
                  onClick={() => setSelectedId(shape.id)}
                  onTap={() => setSelectedId(shape.id)}
                  onDragEnd={(e) => {
                    const node = e.target;
                    setShapes((xs) =>
                      xs.map((s) =>
                        s.id === shape.id
                          ? { ...s, x: node.x() - s.width / 2, y: node.y() - s.height / 2 }
                          : s,
                      ),
                    );
                  }}
                  ref={(node) => {
                    if (shape.id === selectedId) selectedRef.current = node;
                  }}
                />
              ) : (
                <Rect
                  key={shape.id}
                  x={shape.x}
                  y={shape.y}
                  width={shape.width}
                  height={shape.height}
                  fill={shape.fill}
                  stroke={shape.stroke}
                  strokeWidth={2}
                  draggable={tool === "select"}
                  onClick={() => setSelectedId(shape.id)}
                  onTap={() => setSelectedId(shape.id)}
                  onDragEnd={(e) => {
                    setShapes((xs) =>
                      xs.map((s) => (s.id === shape.id ? { ...s, x: e.target.x(), y: e.target.y() } : s)),
                    );
                  }}
                  ref={(node) => {
                    if (shape.id === selectedId) selectedRef.current = node;
                  }}
                />
              ),
            )}
            <Transformer ref={transformerRef} rotateEnabled />
          </Layer>
          <Layer ref={stressLayerRef} listening={false} />
        </Stage>
      </div>
    </div>
  );
}
