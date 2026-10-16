export function discountedTotal(cents, percent) {
  return Math.round(cents * (1 - percent));
}

export function splitCents(total, people) {
  const share = Math.floor(total / people);
  return Array(people).fill(share);
}
