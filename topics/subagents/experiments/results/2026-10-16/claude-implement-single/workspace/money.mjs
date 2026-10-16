export function discountedTotal(cents, percent) {
  return Math.round(cents * (100 - percent) / 100);
}

export function splitCents(total, people) {
  const share = Math.floor(total / people);
  const remainder = total - share * people;
  return Array.from({ length: people }, (_, i) => share + (i < remainder ? 1 : 0));
}
