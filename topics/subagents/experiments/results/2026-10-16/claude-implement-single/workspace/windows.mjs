export function overlaps(a, b) {
  return a.start < b.end && b.start < a.end;
}

export function mergeWindows(windows) {
  const sorted = [...windows].sort((a, b) => a.start - b.start);
  const merged = [];
  for (const window of sorted) {
    const previous = merged.at(-1);
    if (previous && window.start <= previous.end) {
      previous.end = Math.max(previous.end, window.end);
    } else {
      merged.push({ ...window });
    }
  }
  return merged;
}
