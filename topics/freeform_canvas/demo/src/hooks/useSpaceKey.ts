import { useEffect, useState } from "react";

/** Hold Space to pan, like Figma / tldraw. */
export function useSpaceKey() {
  const [space, setSpace] = useState(false);

  useEffect(() => {
    const isTyping = (el: EventTarget | null) => {
      if (!(el instanceof HTMLElement)) return false;
      const tag = el.tagName;
      return tag === "INPUT" || tag === "TEXTAREA" || el.isContentEditable;
    };

    const down = (e: KeyboardEvent) => {
      if (e.code !== "Space" || isTyping(e.target) || e.repeat) return;
      e.preventDefault();
      setSpace(true);
    };
    const up = (e: KeyboardEvent) => {
      if (e.code !== "Space") return;
      setSpace(false);
    };
    window.addEventListener("keydown", down, { capture: true });
    window.addEventListener("keyup", up, { capture: true });
    return () => {
      window.removeEventListener("keydown", down, { capture: true });
      window.removeEventListener("keyup", up, { capture: true });
    };
  }, []);

  return space;
}
