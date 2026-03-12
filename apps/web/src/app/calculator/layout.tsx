import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Incentive Calculator",
  description:
    "Calculate your personalized car incentives and savings. Find state rebates, manufacturer cash, utility rebates, and affinity discounts you qualify for.",
  openGraph: {
    title: "Incentive Calculator - IncentiveDrive",
    description:
      "Calculate your personalized car incentives and savings.",
  },
};

export default function CalculatorLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return children;
}
