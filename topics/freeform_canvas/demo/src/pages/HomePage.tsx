import { Link } from "react-router-dom";
import { PACKAGES } from "../data/packages";

export function HomePage() {
  return (
    <div className="home">
      <section className="hero">
        <p className="eyebrow">Feel it yourself · Sep 2026</p>
        <h1>Popular freeform canvas packages, side by side</h1>
        <p className="lede">
          Two layers, five libraries. <strong>Whiteboard SDKs</strong> (tldraw, Excalidraw) ship tools,
          undo, and export. <strong>Scene engines</strong> (Fabric, Konva, Pixi) give you an object
          model and a renderer — you build the editor. Each demo uses the same spawn-stress HUD so
          you can pan, zoom, draw, then dump 500 / 2k / 5k shapes and watch FPS.
        </p>
      </section>

      <section className="card-grid">
        {PACKAGES.map((pkg) => (
          <Link key={pkg.id} to={pkg.path} className="pkg-card">
            <div className="pkg-card-top">
              <h2>{pkg.name}</h2>
              <span className="pill">{pkg.layer}</span>
            </div>
            <p>{pkg.bestFor}</p>
            <dl>
              <div>
                <dt>Renderer</dt>
                <dd>{pkg.renderer}</dd>
              </div>
              <div>
                <dt>License</dt>
                <dd>{pkg.license}</dd>
              </div>
            </dl>
            <span className="open">Open demo →</span>
          </Link>
        ))}
      </section>

      <section>
        <h2>Comparison</h2>
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th></th>
                {PACKAGES.map((pkg) => (
                  <th key={pkg.id}>{pkg.name}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              <Row label="Layer" values={PACKAGES.map((p) => p.layer)} />
              <Row label="Renderer" values={PACKAGES.map((p) => p.renderer)} />
              <Row label="License" values={PACKAGES.map((p) => p.license)} />
              <Row label="GitHub stars" values={PACKAGES.map((p) => p.stars)} />
              <Row label="npm / month" values={PACKAGES.map((p) => p.monthlyDownloads)} />
              <Row label="Framework" values={PACKAGES.map((p) => p.framework)} />
              <Row label="Undo" values={PACKAGES.map((p) => p.undo)} />
              <Row label="SVG" values={PACKAGES.map((p) => p.svg)} />
              <Row label="Collaboration" values={PACKAGES.map((p) => p.collab)} />
              <Row label="Custom shapes" values={PACKAGES.map((p) => p.customShapes)} />
              <Row label="Watch out" values={PACKAGES.map((p) => p.watchOut)} />
            </tbody>
          </table>
        </div>
      </section>

      <section className="how">
        <h2>How to compare them</h2>
        <ol>
          <li>Open each demo and use the native tools (or the mini-editor on the engines).</li>
          <li>Pan / zoom a bit. On Fabric, Konva, and Pixi: mouse wheel zooms; hold Space to pan.</li>
          <li>Hit <strong>Spawn 2k</strong>, then pan. If it still feels fine, try 5k.</li>
          <li>Watch the FPS readout — it measures main-thread frames, so React reconciling 5k nodes counts.</li>
        </ol>
        <p>
          Full write-up, sources, and “what I would pick” live in{" "}
          <code>topics/freeform_canvas/README.md</code>.
        </p>
      </section>
    </div>
  );
}

function Row({ label, values }: { label: string; values: string[] }) {
  return (
    <tr>
      <th scope="row">{label}</th>
      {values.map((value, i) => (
        <td key={`${label}-${i}`}>{value}</td>
      ))}
    </tr>
  );
}
