// Keep tool evidence and usage; omit internal reasoning and its signatures.
export function publicEvents(stdout) {
  return stdout.split('\n').map(line => {
    if (!line) return line;
    let event;
    try { event = JSON.parse(line); } catch { return line; }
    if (Array.isArray(event.message?.content)) {
      event.message.content = event.message.content.filter(block => !['thinking', 'redacted_thinking'].includes(block.type));
    }
    return JSON.stringify(event);
  }).join('\n');
}
