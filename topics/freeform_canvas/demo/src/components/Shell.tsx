import { NavLink, Outlet } from "react-router-dom";
import { PACKAGES } from "../data/packages";

export function Shell() {
  return (
    <div className="shell">
      <header className="topnav">
        <NavLink to="/" className="brand">
          Canvas bake-off
        </NavLink>
        <nav>
          {PACKAGES.map((pkg) => (
            <NavLink key={pkg.id} to={pkg.path}>
              {pkg.name}
            </NavLink>
          ))}
        </nav>
      </header>
      <main className="shell-main">
        <Outlet />
      </main>
    </div>
  );
}
