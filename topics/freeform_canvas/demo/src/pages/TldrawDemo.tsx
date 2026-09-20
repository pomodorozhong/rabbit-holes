import { useCallback, useState } from "react";
import { Tldraw, type Editor } from "tldraw";
import "tldraw/tldraw.css";
import { DemoToolbar } from "../components/DemoToolbar";
import { scatter } from "../data/packages";
import { useFps } from "../hooks/useFps";

const COLORS = ["blue", "green", "violet", "orange", "red", "light-blue"] as const;

export function TldrawDemo() {
  const fps = useFps();
  const [editor, setEditor] = useState<Editor | null>(null);
  const [count, setCount] = useState(0);

  const refreshCount = useCallback((next: Editor) => {
    setCount(next.getCurrentPageShapes().length);
  }, []);

  const onMount = useCallback(
    (next: Editor) => {
      setEditor(next);
      next.createShapes([
        {
          type: "geo",
          x: 120,
          y: 80,
          props: { geo: "rectangle", w: 280, h: 140, color: "blue", fill: "semi" },
        },
        {
          type: "geo",
          x: 460,
          y: 140,
          props: { geo: "ellipse", w: 180, h: 180, color: "green", fill: "solid" },
        },
      ]);
      next.zoomToFit({ animation: { duration: 0 } });
      refreshCount(next);
      next.store.listen(() => refreshCount(next));
    },
    [refreshCount],
  );

  const spawn = (n: number) => {
    if (!editor) return;
    editor.createShapes(
      Array.from({ length: n }, (_, i) => {
        const p = scatter(i, n);
        return {
          type: "geo" as const,
          x: p.x,
          y: p.y,
          props: {
            geo: i % 3 === 0 ? "ellipse" : "rectangle",
            w: p.w,
            h: p.h,
            color: COLORS[i % COLORS.length],
            fill: "solid" as const,
          },
        };
      }),
    );
    refreshCount(editor);
  };

  const clear = () => {
    if (!editor) return;
    editor.deleteShapes(editor.getCurrentPageShapes().map((s) => s.id));
    refreshCount(editor);
  };

  return (
    <div className="demo-page">
      <DemoToolbar
        objectCount={count}
        fps={fps}
        extra="SDK · production needs a tldraw license"
        hint="Full tldraw editor. Draw, select, frames, arrows. Then spawn shapes and pan — this is the SDK you'd ship."
        onSpawn={spawn}
        onClear={clear}
      />
      <div className="demo-stage tldraw-stage">
        <Tldraw onMount={onMount} />
      </div>
    </div>
  );
}
