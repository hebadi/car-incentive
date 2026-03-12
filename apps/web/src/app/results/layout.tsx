import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Your Savings Results",
  description:
    "See your personalized car incentive savings breakdown. State rebates, manufacturer cash, utility rebates, and more.",
};

export default function ResultsLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return children;
}
