// Shared with the backend's disclaimer text (incentive_matcher.py), which computes
// days_left via Python's `timedelta.days` — a floor, not a round/ceil. Using ceil
// here caused the "Expires in 4 days" badge vs. "expires in 3 days" banner mismatch.
export function getDaysUntil(endDateIso: string): number {
  const now = new Date();
  const end = new Date(endDateIso);
  const diffMs = end.getTime() - now.getTime();
  return Math.floor(diffMs / (1000 * 60 * 60 * 24));
}

const COLORS = {
  light: {
    urgent: "text-red-700 bg-red-50 font-semibold",
    soon: "text-yellow-700 bg-yellow-50",
    expired: "text-red-700 bg-red-50",
    ok: "text-green-700 bg-green-50",
  },
  dark: {
    urgent: "text-red-400 bg-red-400/10 font-semibold",
    soon: "text-yellow-400 bg-yellow-400/10",
    expired: "text-red-400 bg-red-400/10",
    ok: "text-green-400 bg-green-400/10",
  },
};

export function getExpirationInfo(
  endDateIso: string,
  theme: "light" | "dark" = "light"
): { label: string; color: string } {
  const daysLeft = getDaysUntil(endDateIso);
  const colors = COLORS[theme];

  if (daysLeft < 0) {
    return { label: "Expired", color: colors.expired };
  }
  if (daysLeft < 7) {
    return { label: `Expires in ${daysLeft} day${daysLeft !== 1 ? "s" : ""}!`, color: colors.urgent };
  }
  if (daysLeft <= 30) {
    return { label: `Expires in ${daysLeft} days`, color: colors.soon };
  }
  const end = new Date(endDateIso);
  return {
    label: `Expires ${end.toLocaleDateString("en-US", { month: "short", day: "numeric" })}`,
    color: colors.ok,
  };
}
