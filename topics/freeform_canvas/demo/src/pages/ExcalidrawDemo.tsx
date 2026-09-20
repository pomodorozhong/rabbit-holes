import { useCallback, useState } from "react";
import { Excalidraw, convertToExcalidrawElements } from "@excalidraw/excalidraw";
import type { ExcalidrawImperativeAPI } from "@excalidraw/excalidraw/types";
import "@excalidraw/excalidraw/index.css";
import { DemoToolbar } from "../components/DemoToolbar";
import { scatter } from "../data/packages";
import { useFps } from "../hooks/useFps";

const STROKES = ["#58a6ff", "#3fb950", "#d2a8ff", "#f0883e", "#f85149", "#79c0ff"];

export function ExcalidrawDemo() {
  const fps = useFps();
  const [api, setApi] = useState<ExcalidrawImperativeAPI | null>(null);
  const [count, setCount] = useState(0);

  const syncCount = useCallback((next: ExcalidrawImperativeAPI) => {
    setCount(next.getSceneElements().length);
  }, []);

  const spawn = (n: number) => {
    if (!api) return;
    const sketched = convertToExcalidrawElements(
      Array.from({ length: n }, (_, i) => {
        const p = scatter(i, n);
        return {
          type: i % 3 === 0 ? ("ellipse" as const) : ("rectangle" as const),
          x: p.x,
          y: p.y,
          width: p.w,
          height: p.h,
          strokeColor: STROKES[i % STROKES.length],
          backgroundColor: `${STROKES[i % STROKES.length]}33`,
        };
      }),
    );
    api.updateScene({
      elements: [...api.getSceneElements(), ...sketched],
    });
    syncCount(api);
  };

  const clear = () => {
    if (!api) return;
    api.updateScene({ elements: [] });
    syncCount(api);
  };

  return (
    <div className="demo-page">
      <DemoToolbar
        objectCount={count}
        fps={fps}
        hint="Hand-drawn whiteboard. Use the top tools, then spawn 2k boxes and pan. Sketch style is the product."
        onSpawn={spawn}
        onClear={clear}
      />
      <div className="demo-stage">
        <Excalidraw
          excalidrawAPI={(next) => {
            setApi(next);
            syncCount(next);
          }}
          onChange={(elements) => setCount(elements.length)}
          theme="dark"
          UIOptions={{ canvasActions: { toggleTheme: true } }}
          initialData={{
            appState: { currentItemStrokeColor: "#58a6ff" },
            elements: convertToExcalidrawElements([
              {
                type: "rectangle",
                x: 120,
                y: 80,
                width: 280,
                height: 140,
                strokeColor: "#58a6ff",
                backgroundColor: "#58a6ff22",
              },
              {
                type: "ellipse",
                x: 460,
                y: 140,
                width: 180,
                height: 180,
                strokeColor: "#3fb950",
                backgroundColor: "#3fb95033",
              },
              {
                type: "text",
                x: 120,
                y: 250,
                text: "Excalidraw — sketch, then spawn 2k",
                fontSize: 24,
              },
            ]),
          }}
        />
      </div>
    </div>
  );
}
