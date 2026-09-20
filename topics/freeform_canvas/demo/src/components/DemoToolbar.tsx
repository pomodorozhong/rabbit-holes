import { STRESS_COUNTS } from "../data/packages";

type Props = {
  objectCount: number;
  fps: number;
  hint: string;
  extra?: string;
  onSpawn: (count: number) => void;
  onClear: () => void;
};

export function DemoToolbar({ objectCount, fps, hint, extra, onSpawn, onClear }: Props) {
  const fpsClass = fps >= 50 ? "ok" : fps >= 30 ? "warn" : "bad";

  return (
    <div className="demo-toolbar">
      <div className="toolbar-stats">
        <span>
          FPS <strong className={fpsClass}>{fps || "—"}</strong>
        </span>
        <span>
          Objects <strong>{objectCount.toLocaleString()}</strong>
        </span>
        {extra ? <span className="toolbar-extra">{extra}</span> : null}
      </div>
      <div className="toolbar-actions">
        {STRESS_COUNTS.map((n) => (
          <button key={n} type="button" onClick={() => onSpawn(n)}>
            Spawn {n >= 1000 ? `${n / 1000}k` : n}
          </button>
        ))}
        <button type="button" className="danger" onClick={onClear}>
          Clear
        </button>
      </div>
      <p className="toolbar-hint">{hint}</p>
    </div>
  );
}
