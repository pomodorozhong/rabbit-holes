export function discountedTotal(cents, percent) {
  return Math.round(cents * (1 - percent / 100));
}

export function splitCents(total, people) {
  const share = Math.floor(total / people);
  const remainder = total % people;
  return Array.from({ length: people }, (_, index) => share + (index < remainder ? 1 : 0));
}
