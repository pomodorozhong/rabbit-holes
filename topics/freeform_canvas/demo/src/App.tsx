import { lazy, Suspense } from "react";
import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import { Shell } from "./components/Shell";
import { HomePage } from "./pages/HomePage";

const TldrawDemo = lazy(async () => {
  const m = await import("./pages/TldrawDemo");
  return { default: m.TldrawDemo };
});
const ExcalidrawDemo = lazy(async () => {
  const m = await import("./pages/ExcalidrawDemo");
  return { default: m.ExcalidrawDemo };
});
const FabricDemo = lazy(async () => {
  const m = await import("./pages/FabricDemo");
  return { default: m.FabricDemo };
});
const KonvaDemo = lazy(async () => {
  const m = await import("./pages/KonvaDemo");
  return { default: m.KonvaDemo };
});
const PixiDemo = lazy(async () => {
  const m = await import("./pages/PixiDemo");
  return { default: m.PixiDemo };
});

function Fallback() {
  return <div className="fallback">Loading canvas…</div>;
}

export function App() {
  return (
    <BrowserRouter>
      <Suspense fallback={<Fallback />}>
        <Routes>
          <Route element={<Shell />}>
            <Route path="/" element={<HomePage />} />
            <Route path="/tldraw" element={<TldrawDemo />} />
            <Route path="/excalidraw" element={<ExcalidrawDemo />} />
            <Route path="/fabric" element={<FabricDemo />} />
            <Route path="/konva" element={<KonvaDemo />} />
            <Route path="/pixi" element={<PixiDemo />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Route>
        </Routes>
      </Suspense>
    </BrowserRouter>
  );
}
